import sys
import os

here = os.path.abspath(__file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(here)))

from lof.examples import pred_ntf_oil
from lof.utils import is_cn_trading


def main(*argv):
    if not is_cn_trading():
        print("非交易时间")
        return
    codes = ["SH501018", "SZ160216", "SZ162411", "SZ161129", "SZ160723"]
    pred_ntf_oil(*codes, token=argv[1])


if __name__ == "__main__":
    main(*sys.argv)
