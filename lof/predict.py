import xalpha as xa
import datetime as dt
from xalpha.universal import cached
import pandas as pd

from .holdings import infos


@cached("20200101")
def get_daily(*args, **kws):
    return xa.get_daily(*args, **kws)


def daily_increment(code, date, lastday=None):
    tds = get_daily(code=code, end=date, prev=20)
    tds = tds[tds["date"] <= date]
    if not lastday:
        ratio = tds.iloc[-1]["close"] / tds.iloc[-2]["close"]
    else:
        tds2 = tds[tds["date"] <= lastday]
        ratio = tds.iloc[-1]["close"] / tds2.iloc[-1]["close"]
    return ratio


def evaluate_fluctuation(hdict, date, lastday=None):
    price = 0
    tot = 0
    for k, v in hdict.items():
        tot += v
    remain = 100 - tot
    for fundid, percent in hdict.items():
        ratio = daily_increment(fundid, date, lastday)
        price += (
            ratio
            * percent
            / 100
            * daily_increment(infos[fundid].currency + "/CNY", date, lastday)
        )
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
    #     print(yesterday_str)
    net = get_daily("F" + code[2:]).iloc[-1]["close"] * (
        1 + evaluate_fluctuation(hdict, yesterday_str) / 100
    )
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
