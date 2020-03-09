import xalpha as xa

from .predict import get_qdii_t
from .holdings import holdings
from .notification import notify


def pred_ntf_oil(code, **kws):
    daily_holdings = kws.get("daily_holdings", holdings[code[2:]])
    rt_holdings = kws.get("rt_holdings", holdings["oil_rt"])
    ddprice, dprice = get_qdii_t(code, daily_holdings, rt_holdings)
    print(code, dprice, ddprice)
    r = xa.get_rt(code)
    cprice = r["current"]
    higher = kws.get("h", 1.04)
    lower = kws.get("l", 0.97)
    _type = kws.get("ntf_type", "pb")
    if cprice / dprice > higher or cprice / dprice < lower:
        notify(
            r["name"],
            "溢价率已达到 %s%%。T-1 日净值预估 %s, T 日净值实时预估 %s，实时价格 %s。"
            % (
                round((cprice / dprice - 1) * 100, 1),
                round(ddprice, 3),
                round(dprice, 3),
                round(cprice, 3),
            ),
            token=kws.get("token"),
            _type=_type,
        )
