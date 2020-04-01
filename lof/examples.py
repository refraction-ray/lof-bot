import xalpha as xa
import requests
import os
import datetime as dt

from .predict import get_qdii_t
from .holdings import holdings, infos
from .notification import notify
from .exceptions import NonAccurate
from .gh import render_template, render


def pred_ntf_oil(*codes, **kws):
    higher = kws.get("h", 1.05)
    lower = kws.get("l", 0.96)
    title = kws.get("title", "基金溢价提示")
    _type = kws.get("ntf_type", "pb")
    rstr = ""
    for code in codes:
        daily_holdings = kws.get("daily_holdings", holdings[code[2:]])
        rt_holdings = kws.get("rt_holdings", holdings["oil_rt"])
        try:
            ddprice, dprice = get_qdii_t(code, daily_holdings, rt_holdings)
        except NonAccurate as e:
            print(e.reason)
            continue
        print(code, dprice, ddprice)
        r = xa.get_rt(code)
        cprice = r["current"]

        if cprice / dprice > higher or cprice / dprice < lower:
            rstr += "溢价率已达到 %s%%。T-1 日净值预估 %s, T 日净值实时预估 %s，实时价格 %s。\n" % (
                round((cprice / dprice - 1) * 100, 1),
                round(ddprice, 3),
                round(dprice, 3),
                round(cprice, 3),
            )

    if rstr:
        notify(
            title, rstr, token=kws.get("token"), _type=_type,
        )


def render_github(
    *codes, tmpl="qdii.html", date="2020-03-09", cols="4c", refresh=False
):
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates", tmpl
        ),
        "r",
    ) as f:
        t = f.read()
    nversion = t.split("\n")[2].split(":")[1]
    print(nversion)
    for code in codes:
        if not refresh:
            r = requests.get(
                "https://raw.githubusercontent.com/refraction-ray/lof-bot/gh-pages/%s.html"
                % code
            )
            sc = r.status_code
        else:  # 强制刷新
            sc = 404
        if sc == 200:
            version_line = r.text.split("\n")[2]
            if len(version_line.split(":")) > 1:
                version = version_line.split(":")[1]
            else:
                version = "-0.0.1"
            # if version == nversion:
            if True:
                with open(
                    os.path.join(
                        os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))
                        ),
                        "%s.html" % code,
                    ),
                    "w",
                ) as f:
                    f.writelines([render(r.text, code=code)])
            else:
                _new_render_github(code, tmpl, date, cols)
        elif sc == 404:
            _new_render_github(code, tmpl, date, cols)
        else:
            print("get weird http code from github %s" % sc)


def _new_render_github(code, tmpl, date, cols="4c"):
    if code in infos:
        name = infos[code].name
    else:
        name = xa.get_rt(code)["name"]
    once = render_template(
        tmpl=tmpl, code=code, name=name, date=date, cols=cols
    )
    prev = (dt.datetime.now() - dt.datetime.strptime(date, "%Y-%m-%d")).days + 2
    for _ in range(prev):
        once = render(once, code)
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "%s.html" % code,
        ),
        "w",
    ) as f:
        f.writelines([once])
