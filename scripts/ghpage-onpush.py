import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)
sys.path.insert(0, here)

from lof.examples import render_github
import xalpha as xa
from ghpage import main


if __name__ == "__main__":
    main()
    ## extras
    # xa.set_backend(backend="csv", path="./data", precached="20200301")
    render_github(
        "SZ163208", refresh=True,
    )
