import sys
import os

here = os.path.abspath(__file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(here)))

import lof.predict as lp
from lof.holdings import holdings


def test_qdii():
    print(lp.get_qdii_t("SH501018", holdings["501018"], holdings["oil_rt"]))
