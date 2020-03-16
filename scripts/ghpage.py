import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)

from lof.examples import render_github


def main():
    render_github(
        "SH501018",
        "SZ160216",
        "SZ162411",
        "SZ160723",
        "SZ161129",
        "SZ162719",
        "SH513030",
        "SH513500",
        "SZ161130",
    )
    render_github("SZ164906", cols="3c")
    render_github("SH513880", "SH513520", "SH513000", cols="3crt")


if __name__ == "__main__":
    main()
