import sys
import xalpha as xa
import datetime as dt
from xalpha.universal import cached
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from .holdings import infos
from .utils import month_ago, last_onday
from .exceptions import DateMismatch, NonAccurate


def set_cache_start(date=None):
    """
    If you realy have the idea of what you are doing, do it before any other imports,
    otherwise ``get_daily`` cannot change the cache behavior.

    :param date: str.
    :return:
    """
    thismodule = sys.modules[__name__]
    if not date:
        date = getattr(thismodule, "cache_start", month_ago())
    get_daily = cached(date)(xa.get_daily)
    setattr(thismodule, "get_daily", get_daily)
    setattr(thismodule, "cache_start", date)
    xa.universal.reset_cache()


set_cache_start()


def daily_increment(code, date, lastday=None, _check=None):
    tds = get_daily(code=code, end=date, prev=20)
    tds = tds[tds["date"] <= date]
    if _check:
        if tds.iloc[-1]["date"] < dt.datetime.strptime(
            _check, "%Y-%m-%d"
        ):  # in case data is not up to date
            raise DateMismatch(
                code, reason="%s has no data upto %s" % (code, _check)
            )
    if not lastday:
        ratio = tds.iloc[-1]["close"] / tds.iloc[-2]["close"]
    else:
        tds2 = tds[tds["date"] <= lastday]
        ratio = tds.iloc[-1]["close"] / tds2.iloc[-1]["close"]
    return ratio


def evaluate_fluctuation(hdict, date, lastday=None, _check=None):
    price = 0
    tot = 0
    for k, v in hdict.items():
        tot += v
    remain = 100 - tot
    for fundid, percent in hdict.items():
        ratio = daily_increment(fundid, date, lastday, _check)
        exchange = 1
        if infos.get(fundid):
            if infos[fundid].currency != "CNY":
                exchange = daily_increment(
                    infos[fundid].currency + "/CNY", date, lastday, _check
                )
        price += ratio * percent / 100 * exchange
    price += remain / 100
    return (price - 1) * 100


def estimate_table(start, end, *cols):
    """

    :param cols: Tuple[str, Dict]. (colname, holding_dict).
    """
    compare_data = {
        "date": [],
    }
    for col in cols:
        compare_data[col[0]] = []
    dl = pd.Series(pd.date_range(start=start, end=end))
    dl = dl[dl.isin(xa.cons.opendate)]
    for i, d in enumerate(dl):
        if i == 0:
            continue

        dstr = d.strftime("%Y%m%d")
        lstdstr = dl.iloc[i - 1].strftime("%Y%m%d")
        compare_data["date"].append(d)
        for col in cols:
            compare_data[col[0]].append(
                evaluate_fluctuation(col[1], dstr, lstdstr)
            )
    cpdf = pd.DataFrame(compare_data)
    col0 = cols[0]
    for col in cols[1:]:
        cpdf["diff_" + col0[0] + "_" + col[0]] = cpdf[col0[0]] - cpdf[col[0]]
    return cpdf


def get_newest_netvalue(code):
    """

    :param code: six digits string for fund.
    :return: netvalue, %Y-%m-%d
    """
    code = code[1:]
    r = xa.universal.rget(f"http://fund.eastmoney.com/{code}.html")
    s = BeautifulSoup(r.text, "lxml")
    return (
        float(
            s.findAll("dd", class_="dataNums")[1]
            .find("span", class_="ui-font-large")
            .string
        ),
        str(s.findAll("dt")[1]).split("(")[1].split(")")[0][7:],
    )


def get_qdii_tt(code, hdict, date=None):
    # predict d-1 netvalue of qdii funds
    try:
        if date is None:  # 此时预测上个交易日净值
            tz_bj = dt.timezone(dt.timedelta(hours=8))
            today = (
                dt.datetime.now(tz=tz_bj)
                .replace(tzinfo=None)
                .replace(hour=0, minute=0, second=0, microsecond=0)
            )
            yesterday = last_onday(today)
            yesterday_str = yesterday.strftime("%Y%m%d")
            last_value, last_date = get_newest_netvalue("F" + code[2:])
            last_date_obj = dt.datetime.strptime(last_date, "%Y-%m-%d")
            if last_date_obj < last_onday(yesterday):  # 前天净值数据还没更新
                raise DateMismatch(
                    code,
                    reason="%s netvalue has not been updated to the day before yesterday"
                    % code,
                )
            elif last_date_obj > last_onday(yesterday):  # 昨天数据已出，不需要再预测了
                print(
                    "no need to predict t-1 value since it has been out for %s"
                    % code
                )
                return last_value
        else:
            yesterday_str = date.replace("-", "").replace("/", "")
            fund_price = get_daily("F" + code[2:])
            fund_last = fund_price[fund_price["date"] < date].iloc[-1]
            # 注意实时更新应用 date=None 传入，否则此处无法保证此数据是前天的而不是大前天的
            last_value = fund_last["close"]
            last_date = fund_last["date"].strftime("%Y-%m-%d")

        net = last_value * (
            1
            + evaluate_fluctuation(hdict, yesterday_str, _check=last_date) / 100
        )
    except DateMismatch as e:
        error_msg = e.reason
        error_msg += ", therefore %s cannot predict correctly" % code
        raise NonAccurate(code=code, reason=error_msg)
    return net


def get_qdii_t(
    code, ttdict, tdict,
):
    # predict realtime netvalue for d day, only possible for oil related lof
    nettt = get_qdii_tt(code, ttdict)
    t = 0
    n = 0
    today_str = dt.datetime.now().strftime("%Y%m%d")
    for k, v in tdict.items():
        t += v
        r = xa.get_rt(k)
        c = v / 100 * (1 + r["percent"] / 100)
        c = c * daily_increment(r["currency"] + "/CNY", today_str)
        n += c
    n += (100 - t) / 100
    nett = n * nettt
    return nettt, nett


def get_nonqdii_t(code, tdict, date=None):
    if not date:  # 今日实时净值
        last_value, last_date = get_newest_netvalue("F" + code[2:])
        tz_bj = dt.timezone(dt.timedelta(hours=8))
        today = dt.datetime.now(tz=tz_bj).replace(tzinfo=None)
        today_str = today.strftime("%Y-%m-%d")
        yesterday = last_onday(today)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        last_value, last_date = get_newest_netvalue("F" + code[2:])
        if last_date != yesterday_str:
            raise DateMismatch(
                code, "%s netvalue has not been updated to yesterday" % code
            )
        t = 0
        r = 100
        for k, v in tdict.items():
            if infos.get(k):
                url = infos[k].url
            else:
                url = k
            aim_current = xa.get_rt(url)
            delta1 = aim_current["percent"] / 100
            currency = aim_current["currency"]
            ## 关于当日货币换算的部分，1. 当日中间价涨幅 2. 当日汇率市价实时涨幅 3.1+2 哪个更合适待研究
            if currency == "JPY":
                delta2 = daily_increment(
                    "100JPY/CNY", today_str, yesterday_str, _check=today_str
                )
                # delta2 = xa.get_rt("currencies/jpy-cny")["percent"] / 100
            elif currency == "USD":
                delta2 = daily_increment(
                    "USD/CNY", today_str, yesterday_str, _check=today_str
                )
                # delta2 = xa.get_rt("currencies/usd-cny")["percent"] / 100
            elif currency == "EUR":
                delta2 = daily_increment(
                    "EUR/CNY", today_str, yesterday_str, _check=today_str
                )
            elif currency == "CNY":
                delta2 = 0
            else:
                raise NonAccurate(
                    "%s transformation have not been implemented" % currency
                )

            r -= v
            t += v * (1 + delta1) * delta2 / 100

        t += r / 100
        return last_value * t
    # 过去净值同日预测 date 日, date 日一定是交易日
    date_str = date.replace("-", "").replace("/", "")
    funddf = xa.get_daily("F" + code[2:])
    last_value = funddf[funddf["date"] < date_str].iloc[-1]["close"]
    net = last_value * (1 + evaluate_fluctuation(tdict, date_str) / 100)
    return net


def analyse_ud(cpdf, col1, col2):
    """


    :param cpdf: pd.DataFrame, with col1 as real netvalue and col2 as prediction difference
    :param col1: str.
    :param col2: str.
    :return:
    """
    uu, ud, dd, du, count = 0, 0, 0, 0, 0
    # uu 实际上涨，real-est>0 (预测涨的少)
    # ud 预测涨的多
    # du 预测跌的多
    # dd 预测跌的少
    for i, row in cpdf.iterrows():
        if row[col1] >= 0 and row[col2] > 0:
            uu += 1
        elif row[col1] >= 0 >= row[col2]:
            ud += 1
        elif row[col1] < 0 < row[col2]:
            du += 1
        else:
            dd += 1
        count += 1
    print(
        "\n涨跌偏差分析:",
        "\n预测涨的比实际少: ",
        round(uu / count, 2),
        "\n预测涨的比实际多: ",
        round(ud / count, 2),
        "\n预测跌的比实际多: ",
        round(du / count, 2),
        "\n预测跌的比实际少: ",
        round(dd / count, 2),
    )


def analyse_percentile(cpdf, col):
    percentile = [1, 5, 25, 50, 75, 95, 99]
    r = [round(d, 3) for d in np.percentile(list(cpdf[col]), percentile)]
    print(
        "\n预测偏差分位:",
        "\n1% 分位: ",
        r[0],
        "\n5% 分位: ",
        r[1],
        "\n25% 分位: ",
        r[2],
        "\n50% 分位: ",
        r[3],
        "\n75% 分位: ",
        r[4],
        "\n95% 分位: ",
        r[5],
        "\n99% 分位: ",
        r[6],
    )


def analyse_deviate(cpdf, col):
    l = np.array(cpdf[col])
    d1, d2 = np.mean(np.abs(l)), np.sqrt(np.mean(l ** 2))
    print("\n平均偏离: ", d1, "\n标准差偏离： ", d2)


def analyse_all(cpdf, col, reference="real"):
    print("净值预测回测分析:\n")
    analyse_deviate(cpdf, col)
    analyse_percentile(cpdf, col)
    analyse_ud(cpdf, reference, col)
