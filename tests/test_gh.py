import sys
import os

here = os.path.abspath(__file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(here)))

from lof.gh import render_template, render
from lof.examples import render_github


def test_render_template():
    with open(os.path.join(os.path.dirname(here), "test.html"), "w") as f:
        once = render_template(
            code="SH501018", name="南方原油", date="2020-03-09", new="4c"
        )
        twice = render(once, "SH501018")
        third = render(twice, "SH501018")
        fourth = render(third, "SH501018")
        f.writelines([fourth])


def test_render_template_3c():
    with open(os.path.join(os.path.dirname(here), "test.html"), "w") as f:
        once = render_template(
            code="SH513030", name="德国30", date="2020-03-09", cols="3c"
        )
        twice = render(once, "SH513030")
        third = render(twice, "SH513030")
        fourth = render(third, "SH513030")
        f.writelines([fourth])


def test_render_github():
    render_github("SH501018")
