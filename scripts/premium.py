import sys
import os

here = os.path.abspath(__file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(here)))

import lof.predict as lp
from lof.holdings import holdings
from lof.notification import notify
import xalpha as xa


def main(*argv):
    ddprice, dprice = lp.get_qdii_t(
        "SH501018", holdings["501018"], holdings["oil_rt"]
    )
    cprice = xa.get_rt("SH501018")["current"]
    if cprice / dprice > 1.05:
        notify(
            "南方原油",
            "溢价率已达到 %s。T-1 日净值预估 %s, T 日净值实时预估 %s"
            % (
                round((cprice / dprice - 1) * 100, 1),
                round(ddprice, 3),
                round(dprice, 3),
            ),
            token=argv[1],
        )


if __name__ == "__main__":
    main(*sys.argv)
