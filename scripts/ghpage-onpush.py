import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)
sys.path.insert(0, here)

from lof.examples import render_github
from ghpage import main

if __name__ == "__main__":
    main()
    ## extras
    # render_github("SZ162411", date="2020-03-16")
