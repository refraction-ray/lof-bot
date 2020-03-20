import datetime as dt
import xalpha as xa
import re
from jinja2 import Environment, PackageLoader

from .predict import get_qdii_tt, get_qdii_t, get_newest_netvalue, get_nonqdii_t
from .holdings import holdings
from .exceptions import NonAccurate
from .utils import next_onday, last_onday, tz_bj


def render(text, code=None):
    r = ""
    s = 0
    ls = [
        (m.start(0), m.end(0), text[m.start(0) : m.end(0)])
        for m in re.finditer(r"<!--update[^>]*>[^<]*<!--end-->", text)
    ]
    for l in ls:
        r += text[s : l[0]]
        r += replace_text(l[2], code)
        s = l[1]
    r += text[s:]
    return r


def replace_text(otext, code=None, est_holdings=None, rt_holdings=None):
    print(otext)
    dtstr = otext.split(":")[1].split(";")[0]
    dtobj = dt.datetime.strptime(dtstr, "%Y-%m-%d-%H-%M")
    now = dt.datetime.now(tz=tz_bj)
    now = now.replace(tzinfo=None)
    if now >= dtobj:
        v = otext.split(">")[0].split(";")[1].split("-")[-3]
        vdtstr = otext.split(";")[1][:10]  # -
        if not est_holdings:
            est_holdings = holdings[code[2:]]
        today = now.strftime("%Y-%m-%d")
        if v == "value1":
            if not rt_holdings and not holdings.get(code[2:] + "rt"):
                rt_holdings = holdings["oil_rt"]  # 默认石油基金预测
            elif not rt_holdings:
                rt_holdings = holdings[code[2:] + "rt"]
            # 实时净值
            if today == vdtstr and now.hour < 18:  # 晚于下午6点就不再更新实时净值（暂定）
                try:
                    _, rtvalue = get_qdii_t(code, est_holdings, rt_holdings)
                    ntext = str(round(rtvalue, 3))
                    now_value = xa.get_rt(code)["current"]
                    prate = round((now_value / rtvalue - 1) * 100, 1)
                    ntext += f" ({now.strftime('%H:%M')})"
                    if prate > 0:
                        ntext += f'<p style="color: red;display: inline"> [{prate}%]</p>'
                    else:
                        ntext += f'<p style="color: green;display: inline"> [{prate}%]</p>'
                    ntext = (
                        otext.split(">")[0]
                        + ">"
                        + ntext
                        + "<"
                        + otext.split("<")[-1]
                    )
                except NonAccurate as e:
                    print(e.reason)
                    ntext = otext
            else:
                # 新的一天，不再预测实时
                ntext = otext.split(">")[1].split("<")[0]
        elif v == "value2":
            try:
                if last_onday(now).strftime("%Y-%m-%d") == vdtstr:
                    ntext = str(round(get_qdii_tt(code, est_holdings), 3))
                else:
                    ntext = str(
                        round(get_qdii_tt(code, est_holdings, date=vdtstr), 3)
                    )
            except NonAccurate as e:
                print(e.reason)
                ntext = otext
        elif v == "value3":
            # 真实净值
            fund_price = xa.get_daily(code="F" + code[2:], end=vdtstr)
            fund_line = fund_price[fund_price["date"] == vdtstr]
            if len(fund_line) == 0:
                value, date = get_newest_netvalue(
                    "F" + code[2:]
                )  # incase get_daily -1 didn't get timely update
            else:
                value = fund_line.iloc[0]["close"]
                date = fund_line.iloc[0]["date"].strftime("%Y-%m-%d")
            if date != vdtstr:
                ntext = otext
            else:
                ntext = str(value)
        elif v == "value4":  # non qdii 同日 qdii lof 的实时净值
            try:
                if today == vdtstr:
                    if now.hour > 9 and now.hour < 15:
                        v = get_nonqdii_t(code, est_holdings)
                        ntext = str(round(v, 3))
                        ntext += f" ({now.strftime('%H:%M')})"
                        ntext = (
                            otext.split(">")[0]
                            + ">"
                            + ntext
                            + "<"
                            + otext.split("<")[-1]
                        )
                    else:
                        ntext = otext
                else:
                    v = get_nonqdii_t(code, est_holdings, date=vdtstr)
                    ntext = str(round(v, 3))

            except NonAccurate as e:
                print(e.reason)
                ntext = otext

        elif v == "4c":
            ntext = f"""<!--update:{next_onday(dtobj).strftime("%Y-%m-%d-%H-%M")};{next_onday(dtobj).strftime("%Y-%m-%d")}-4c--><!--end-->
<tr>
<td style='text-align:center;' >{dtobj.strftime("%Y-%m-%d")}</td>
<td style='text-align:center;' ><!--update:{(dtobj + dt.timedelta(hours=1)).strftime("%Y-%m-%d-%H-%M")};{dtobj.strftime("%Y-%m-%d")}-value1-->&nbsp;<!--end--></td>
<td style='text-align:center;' ><!--update:{(dtobj + dt.timedelta(days=1, hours=1)).strftime(
        "%Y-%m-%d-%H-%M"
    )};{dtobj.strftime("%Y-%m-%d")}-value2-->&nbsp;<!--end--></td>
<td style='text-align:center;' ><!--update:{next_onday(next_onday(dtobj)).strftime("%Y-%m-%d-%H-%M")};{dtobj.strftime("%Y-%m-%d")}-value3-->&nbsp;<!--end--></td>
</tr>
            """
        elif v == "3c":
            ntext = f"""<!--update:{next_onday(dtobj).strftime("%Y-%m-%d-%H-%M")};{next_onday(dtobj).strftime("%Y-%m-%d")}-3c--><!--end-->
<tr>
<td style='text-align:center;' >{dtobj.strftime("%Y-%m-%d")}</td>
<td style='text-align:center;' ><!--update:{(dtobj + dt.timedelta(days=1, hours=1)).strftime(
        "%Y-%m-%d-%H-%M"
    )};{dtobj.strftime("%Y-%m-%d")}-value2-->&nbsp;<!--end--></td>
<td style='text-align:center;' ><!--update:{next_onday(next_onday(dtobj)).strftime("%Y-%m-%d-%H-%M")};{dtobj.strftime("%Y-%m-%d")}-value3-->&nbsp;<!--end--></td>
</tr>
                        """
        elif v == "3crt":
            ntext = f"""<!--update:{next_onday(dtobj).strftime("%Y-%m-%d-%H-%M")};{next_onday(dtobj).strftime("%Y-%m-%d")}-3crt--><!--end-->
<tr>
<td style='text-align:center;' >{dtobj.strftime("%Y-%m-%d")}</td>
<td style='text-align:center;' ><!--update:{(dtobj + dt.timedelta(hours=1, minutes=30)).strftime(
        "%Y-%m-%d-%H-%M"
    )};{dtobj.strftime("%Y-%m-%d")}-value4-->&nbsp;<!--end--></td>
<td style='text-align:center;' ><!--update:{next_onday(dtobj).strftime("%Y-%m-%d-%H-%M")};{dtobj.strftime("%Y-%m-%d")}-value3-->&nbsp;<!--end--></td>
</tr>
                        """

    else:
        ntext = otext
    print("replaced as %s" % ntext)
    return ntext


env = Environment(loader=PackageLoader("lof", "templates"))


def render_template(tmpl="qdii.html", **kws):

    template = env.get_template(tmpl)
    return template.render(**kws)
