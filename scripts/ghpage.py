import sys
import os

here = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, project_dir)

from lof.gh import render


def main():
    fs = [
        f
        for f in os.listdir(project_dir)
        if f.startswith("SH") or f.startswith("SZ")
    ]
    for f in fs:
        with open(os.path.join(project_dir, f), "r") as fh:
            text = fh.read()
        with open(os.path.join(project_dir, f), "w") as fh:
            fh.writelines([render(text, code=f.split(".")[0])])


if __name__ == "__main__":
    main()
