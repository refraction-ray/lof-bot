import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)

from lof.examples import render_github


if __name__ == "__main__":
    render_github("SH513880", "SH513520", "SH513000", cols="3crt", refresh=True)
    # render_github("SZ162411", cols="4c", refresh=True)
    # render_github("SZ164906", cols="3c", refresh=True)
    print("placeholder")
