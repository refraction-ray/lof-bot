import xalpha as xa
import datetime as dt

tz_bj = dt.timezone(dt.timedelta(hours=8))


def is_cn_trading(dtobj=None):
    tz_bj = dt.timezone(dt.timedelta(hours=8))
    if not dtobj:
        dtobj = dt.datetime.now(tz=tz_bj)
    ison = xa.cons.caldate[
        xa.cons.caldate["cal_date"] == dtobj.strftime("%Y-%m-%d")
    ].iloc[0]["is_open"]
    if ison == 0:
        return False
    else:  # 交易日 # 9:00-9:30 也包括，用于盘前获取信息
        if (
            dtobj.hour < 9
            or dtobj.hour >= 15
            or (dtobj.hour == 12)
            or (dtobj.hour == 11 and dtobj.minute > 30)
        ):
            return False
        else:  # 交易日交易时间
            return True


def month_ago():
    now = dt.datetime.now()
    before = now - dt.timedelta(30)
    return before.strftime("%Y%m%d")


def next_onday(dtobj):
    dtobj += dt.timedelta(1)
    while dtobj.strftime("%Y-%m-%d") not in xa.cons.opendate:
        dtobj += dt.timedelta(1)
    return dtobj


def last_onday(dtobj):
    dtobj -= dt.timedelta(1)
    while dtobj.strftime("%Y-%m-%d") not in xa.cons.opendate:
        dtobj -= dt.timedelta(1)
    return dtobj


def scale_dict(d, scale=1, ulimit=100, dlimit=50, aim=None):
    t = sum([v for _, v in d.items()])
    if t * scale > ulimit:
        scale = ulimit / t
    elif t * scale < dlimit:
        scale = dlimit / t
    if aim:
        scale = aim / t
    for k, v in d.items():
        d[k] = v * scale
    return d
