import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)

import requests
from lof.gh import render

codes = ["SH501018"]


def main():
    # fs = [
    #     f
    #     for f in os.listdir(project_dir)
    #     if f.startswith("SH") or f.startswith("SZ")
    # ]
    for code in codes:
        r = requests.get(
            "https://raw.githubusercontent.com/refraction-ray/lof-bot/gh-pages/%s.html"
            % code
        )

        with open(os.path.join(project_dir, code + ".html"), "w") as fh:
            fh.writelines([render(r.text, code=code)])


if __name__ == "__main__":
    main()
