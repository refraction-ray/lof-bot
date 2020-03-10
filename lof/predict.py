import xalpha as xa
import datetime as dt
from xalpha.universal import cached
import pandas as pd
from collections import namedtuple
import numpy as np

from .holdings import infos
from .exceptions import DateMismatch, NonAccurate


@cached("20200101")
def get_daily(*args, **kws):
    return xa.get_daily(*args, **kws)


def daily_increment(code, date, lastday=None, _check=None):
    tds = get_daily(code=code, end=date, prev=20)
    tds = tds[tds["date"] <= date]
    if _check:
        if tds.iloc[-1]["date"] <= dt.datetime.strptime(
            _check, "%Y-%m-%d"
        ):  # in case data is not up to date
            raise DateMismatch(code)
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
                    infos[fundid].currency + "/CNY", date, lastday
                )
        price += ratio * percent / 100 * exchange
    price += remain / 100  # currency part
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


def get_qdii_tt(code, hdict):
    # predict d-1 netvalue of qdii funds
    tz_bj = dt.timezone(dt.timedelta(hours=8))
    yesterday = dt.datetime.now(tz=tz_bj) - dt.timedelta(1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    fund_last = get_daily("F" + code[2:]).iloc[-1]
    last_date = fund_last["date"].strftime("%Y-%m-%d")
    try:
        net = fund_last["close"] * (
            1
            + evaluate_fluctuation(hdict, yesterday_str, _check=last_date) / 100
        )
    except DateMismatch as e:
        error_msg = "%s has no data up to %s" % (e.code, yesterday_str)
        print(error_msg)
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


涨跌偏差分析 = namedtuple("涨跌偏差分析", ["预测涨的比实际少", "预测涨的比实际多", "预测跌的比实际多", "预测跌的比实际少"])


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
    return 涨跌偏差分析(
        round(uu / count, 2),
        round(ud / count, 2),
        round(du / count, 2),
        round(dd / count, 2),
    )


预测偏差百分位 = namedtuple(
    "预测偏差百分位",
    ["百分之1分位", "百分之5分位", "百分之25分位", "百分之50分位", "百分之75分位", "百分之95分位", "百分之99分位"],
)


def analyse_percentile(cpdf, col):
    percentile = [1, 5, 25, 50, 75, 95, 99]
    return 预测偏差百分位(
        *[round(d, 3) for d in np.percentile(list(cpdf[col]), percentile)]
    )
