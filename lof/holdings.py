from collections import namedtuple
from .utils import scale_dict

# 南方原油持仓及基准
# 38335 WisdomTree WTI Crude Oil
# 44793 United States 12 Month Oil Fund LP
# 995771 UBS ETF CHCMCI Oil SF USD A-dis https://cn.investing.com/etfs/ubs-cmci-oil-sf-usd
# 44794 United States Oil Fund LP
# 44792 Invesco DB Oil Fund
# 38324 WisdomTree Brent Crude Oil
# 44634 United States Brent Oil Fund LP
# 37450 WisdomTree Brent Crude Oil 1mth
# 1014132 iPath S&P GSCI Crude Oil Total Return Index ETN

# 8833 brent oil
# 8849 wti oil

Info = namedtuple("Info", ["name", "url", "currency"])

infos = {
    "38335": Info(
        "WisdomTree WTI Crude Oil (CRUD)", "etfs/etfs-crude-oil", "USD"
    ),
    "44793": Info(
        "United States 12 Month Oil Fund, LP (USL)",
        "etfs/united-states-12-month-oil",
        "USD",
    ),
    "995771": Info(
        "UBS CMCI Oil SF (OILUSA)", "etfs/ubs-cmci-oil-sf-usd", "USD"
    ),
    "44794": Info(
        "United States Oil Fund, LP (USO)", "etfs/united-states-oil-fund", "USD"
    ),
    "44792": Info(
        "Invesco DB Oil Fund (DBO)", "etfs/powershares-db-oil-fund", "USD"
    ),
    "38324": Info(
        "WisdomTree Brent Crude Oil (BRNT)", "etfs/etfs-brent-crude", "USD"
    ),
    "44634": Info(
        "United States Brent Oil Fund, LP (BNO)",
        "etfs/united-states-brent-oil-fund-lp",
        "USD",
    ),
    "37450": Info(
        "WisdomTree Brent Crude Oil 1 month (OILB)",
        "etfs/etfs-brent-1mth-uk",
        "USD",
    ),
    "1014132": Info(
        "iPath® S&P GSCI® Crude Oil Total Return Index ETN (OIL)",
        "etfs/ipath-series-b-sp-gsci-crd-oil-tr",
        "USD",
    ),
    "8833": Info("伦敦布伦特原油期货", "commodities/brent-oil", "USD"),
    "8849": Info("WTI原油期货", "commodities/crude-oil", "USD"),
    "38284": Info(
        "SPDR® S&P Oil & Gas Exploration & Production ETF (XOP)",
        "etfs/spdr-s-p-oil--gas-explor---product",
        "USD",
    ),
    "1010825": Info(
        "S&P Oil & Gas Exploration & Production Select Industry TR (SPSIOPTR)",
        "indices/s-p-oil-gas-exploration-product-tr",
        "USD",
    ),
    # no valid realtime data and historical data update is not immediate. 9.00am BJ time is not enough to check yesterday value
    "14218": Info(
        "ProShares Ultra Bloomberg Crude Oil (UCO)",
        "etfs/proshares-ultra-dj-ubs-crude-oil",
        "USD",
    ),
    "37471": Info(
        "Invesco DB US Dollar Index Bullish Fund (UUP)",
        "etfs/powershares-db-usd-index-bullish",
        "USD",
    ),
    "44798": Info(
        "VelocityShares 3x Long Crude Oil ETNs linked to the S&P GSCI® Crude Oil Index ER New (UWT)",
        "etfs/velocityshares-3x-long-crude-oil",
        "USD",
    ),
    "44718": Info(
        "Invesco DB Precious Metals Fund (DBP)",
        "etfs/powershares-db-precious-metals",
        "USD",
    ),
    "9236": Info(
        "iShares Silver Trust (SLV)", "etfs/ishares-silver-trust", "USD"
    ),
    "1122426": Info(
        "S&P GSCI Crude Oil Index Excess Return (SPGSCLP)",
        "indices/s-p-gsci-crude-oil-er-historical-data",
        "USD",
    ),  # no valid realtime data
    "953362": Info("Simplex WTI (1671)", "etfs/simplex-wti", "100JPY"),
    "953293": Info(
        "NEXT FUNDS Nomura Crude Oil Long (1699)",
        "etfs/next-funds-nomura-crude-oil-long",
        "100JPY",
    ),
    "172": Info("德国DAX30指数 (GDAXI)", "indices/germany-30", "EUR"),
    "954528": Info(
        "Dow Jones US Select Oil Exploration & Production (DJSOEP)",
        "indices/dj-us-select-oil-exploration-prod",
        "USD",
    ),
    "998951": Info(
        "S&P GSCI Crude Oil Total Return (SPGSCLTR)",
        "indices/sp-gsci-crude-oil-tr-historical-data",
        "USD",
    ),
    # not the one for huaanbiaopushiyou
    "166": Info("美国标准普尔500指数 (SPX)", "indices/us-spx-500", "USD"),
    "178": Info("日经225指数 (N225)", "indices/japan-ni225", "100JPY"),
    "20": Info("纳斯达克100指数 (NDX)", "indices/nq-100", "USD"),
    "954018": Info(
        "中证海外中国互联网美元指数 (H11137)",
        "indices/csi-overseas-china-internet-usd",
        "USD",
    ),
    "8839": Info("美国标普500指数期货", "indices/us-spx-500-futures", "USD"),
    "8874": Info("纳斯达克100指数期货 ", "indices/nq-100-futures", "USD"),
    "8826": Info("德国DAX指数期货", "indices/germany-30-futures", "EUR"),
    "27": Info("英国富时100指数 (FTSE)", "indices/uk-100", "GBP"),
    "8838": Info("英国富时100指数期货", "indices/uk-100-futures", "GBP"),
    ".SPHCMSHP": Info("标普香港上市中国中小盘指数", ".SPHCMSHP", "USD"),
    "CSIH11136": Info("中国互联网", "CSIH11136", "CNY"),
    ".SPSIOP": Info("标普石油天然气上游股票指数", ".SPSIOP", "USD"),
    "40657": Info(
        "Energy Select Sector SPDR® Fund (XLE)",
        "etfs/spdr-energy-select-sector-fund",
        "USD",
    ),
    "520": Info(
        "iShares Global Energy ETF (IXC)",
        "etfs/ishares-s-p-global-energy",
        "USD",
    ),
    "40673": Info(
        "iShares U.S. Energy ETF (IYE)",
        "etfs/ishares-dj-us-energy-sector-fund",
        "USD",
    ),
    "45405": Info(
        "Vanguard Energy Index Fund ETF Shares (VDE)",
        "etfs/vanguard-energy",
        "USD",
    ),
    "45707": Info("ETFS Natural Gas (NGAS)", "etfs/etfs-natural-gas", "USD"),
    "962670": Info("标普500指数能源板块 (SPNY)", "indices/s-p-500-energy", "USD"),
    "996734": Info(
        "Silver Futures - (SAGc1)", "commodities/silver?cid=996734", "CNY"
    ),  # 上海期货交易所白银期货
    "HK00700": Info("腾讯控股", "HK00700", "HKD"),
    "BABA": Info("阿里巴巴", "BABA", "USD"),
    "HK03690": Info("美团点评", "HK03690", "HKD"),
    "BIDU": Info("百度", "BIDU", "USD"),
    "JD": Info("京东", "JD", "USD"),
    "TAL": Info("好未来", "TAL", "USD"),
    "NTES": Info("网易", "NTES", "USD"),
    "TCOM": Info("携程", "TCOM", "USD"),
    "PDD": Info("拼多多", "PDD", "USD"),
    "WUBA": Info("58同城", "WUBA", "USD"),
    "SP5475707.2": Info("S&P Global Oil Index", "SP5475707.2", "USD"),
    "959519": Info(
        "iShares Commodities Select Strategy ETF (COMT)",
        "etfs/ishares-commodities-strategy",
        "USD",
    ),
    "959523": Info(
        "Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF (PDBC)",
        "etfs/powershares-db-optimum-yield-divers",
        "USD",
    ),
    "515": Info(
        "iShares S&P GSCI Commodity-Indexed Trust (GSG)",
        "etfs/ishares-s-p-gsci-commod",
        "USD",
    ),
    "40684": Info(
        "Invesco DB Agriculture Fund (DBA)",
        "etfs/powershares-db-agriculture-fund",
        "USD",
    ),
    "44715": Info(
        "Invesco DB Base Metals Fund (DBB)",
        "etfs/powershares-db-base-metals-fund",
        "USD",
    ),
    "1155647": Info(
        "iPath® Series B Bloomberg Livestock Subindex Total Return (COW)",
        "etfs/ipath-b-bloomberg-lvstk-subndx-tr",
        "USD",
    ),
    # 这代码真的合适
    "44901": Info(
        "United States Gasoline Fund, LP (UGA)",
        "etfs/united-states-gasoline-fund-lp",
        "USD",
    ),
    "9227": Info("SPDR® Gold Shares (GLD)", "etfs/spdr-gold-trust", "USD"),
    "14178": Info(
        "Invesco DB Commodity Index Tracking Fund (DBC)",
        "etfs/powershares-db-commodity-index",
        "USD",
    ),
    "959572": Info("安硕A50 (2823)", "etfs/ishares-ftse-a50-china", "HKD"),
    "BB-FGERBIU:ID": Info(
        "FGS - Backwardated Basket E-roll Commodities Trust",
        "BB-FGERBIU:ID",
        "USD",
    ),
    "BB-FLDIVBK:FP": Info(
        "FSP - MS Diversified Backwardated Fund", "BB-FLDIVBK:FP", "CHF"
    ),  # 瑞士法郎666
    "1088675": Info(
        "标普高盛商品指数 (SPGSCI)", "indices/s-p-goldman-sachs-commodity-index", "USD"
    ),
}


future_now = {"8839": "166", "8874": "20", "8826": "172"}

holdings = {}

# 南方原油
# 2019 第四季度季报披露
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001191374337197_1.pdf
holdings_501018_19s3 = {
    "37450": 15.31,
    "44792": 13.64,
    "44794": 13.46,
    "44634": 12.48,
    "38335": 11.73,
    "38324": 9.45,
    "995771": 6.53,
    "44793": 6.02,
    "1014132": 5.42,
}
# 2019 第三季度季报披露
# reference: http://pdf.dfcfw.com/pdf/H2_AN201910241369695857_1.pdf
holdings_501018_19s4 = {
    "38335": 7.34,
    "44793": 8.14,
    "995771": 8.68,
    "44794": 9.63,
    "44792": 11.6,
    "38324": 15.04,
    "44634": 15.42,
    "37450": 17.51,
    "1014132": 0.06,
}
holdings_501018_bc_cash = {"8849": 52.8, "8833": 35.2}
# holdings_bc = {"8849": 60, "8833": 40}

# 国泰商品
# 2019 第四季度季报披露
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001161374256079_1.pdf
holdings_160216_19s4 = {
    "44794": 16.9,
    "14218": 14.03,
    "44634": 11.77,
    "37471": 10.98,
    "44792": 9.1,
    "44798": 7.82,
    "1014132": 7.76,
    "44793": 2.25,
    "44718": 0.01,
    "9236": 0,
}

# 华宝油气直接按持仓跟踪指数模拟，实际其直接持仓成分股
holdings_162411_19s4 = {".SPSIOP": 91}  # 1010825

# 华安标普全球石油指数
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001201374395365_1.pdf
holdings_160416_19s4_alt = {"520": 88}
# couldn't find the benchmark index as investing.com: S&P Global Oil Index Net Total Return
# 使用 IXC 代替
holdings_160416_19s4 = {"SP5475707.2": 90}

# 易方达原油
# reference http://pdf.dfcfw.com/pdf/H2_AN202001171374296729_1.pdf
holdings_161129_19s4 = {
    "38335": 18.96,
    "44794": 18.81,
    "44634": 18.63,
    "44792": 18.39,
    "953362": 10.26,
    "44793": 4.18,
    "953293": 3.6,
    "37450": 1.64,
}
holdings_161129_bc_cash = {"1122426": 90.92}

# 嘉实原油
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001201374377449_1.pdf
# 一个跟踪基准100% WTI 的基金为何买了这么多跟踪 brent 的基金。。。
holdings_160723_19s4 = {
    "38324": 18.96,
    "44792": 16.65,
    "37450": 14.87,
    "44793": 14.48,
    "44634": 13.79,
    "38335": 13.32,
    "44794": 6.47,
}
holdings_160723_bc_cash = {"8849": 93.55}

# 广发道琼斯美国石油开发与生产指数
# reference: 广发道琼斯美国石油开发与生产指数
holdings_162719_19s4 = {"954528": 88.81}

# 诺安油气
# 季报里写上基金全称不麻烦吧。。。
holdings_163208_19s4 = {
    "38284": 17.78,
    "40657": 15.96,
    "520": 15.88,
    "40673": 15.46,
    "45405": 14.55,
    "44634": 6.36,
    "44794": 4.38,
    "45707": 1.41,
}

holdings_163208_bc = {"962670": 90}

# 信诚商品

holdings_165513_19s4 = {
    "959519": 18.39,
    "959523": 15.1,
    "515": 14.3,
    "44634": 14.02,
    "40684": 8.54,
    "44715": 5.41,
    "14218": 5.36,
    "1155647": 3.79,
    "44794": 2.97,
    "44901": 2.12,
}

# 银华通胀

holdings_161815_19s4 = {
    "9227": 17.75,
    "14178": 13.87,
    "44792": 12.52,
    "44634": 11.85,
    "959572": 11.33,
    "BB-FLDIVBK:FP": 9.17,
    "BB-FGERBIU:ID": 6.77,
    "40684": 3.27,
    "515": 2.68,
}

holdings_161815_bc = {"1088675": 70}

# 华安德国
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001211374413094_1.pdf
# http://pdf.dfcfw.com/pdf/H2_AN202001201374397836_1.pdf 华安联接现在有个超级大户。。。
holdings_513030_19s4 = {"172": 94.81}

# 博时标普500
# reference: http://pdf.dfcfw.com/pdf/H2_AN202001171374274630_1.pdf
holdings_513500_19s4 = {"166": 99.5}  # 这一仓位经过调整，比较符合实际的预测
holdings_161125_19s4 = {"166": 99}

# 日经225
holdings_513880_19s4 = {"178": 95}

# 易方达 nasdaq 100
holdings_161130_19s4 = {"20": 94}

# 交银中国互联
holdings_164906_19s4 = {"CSIH11136": 95}  # 954018

## 国泰纳斯达克
holdings_513100_19s4 = {"20": 99}

# couldn't find 互联网50 for 中概互联 at investing.com
# 易方达中概
holdings_513050_19s4 = {
    "HK00700": 31.15,
    "BABA": 30.17,
    "HK03690": 6.95,
    "BIDU": 5.84,
    "JD": 5.45,
    "TAL": 3.28,
    "NTES": 3.15,
    "TCOM": 2.47,
    "PDD": 2.33,
    "WUBA": 0.99,
}

# 建信富时100
holdings_539003_19s4 = {"27": 95}  # 跟踪非常不准

# 华宝中小
holdings_501021_19s4 = {".SPHCMSHP": 92}

holdings["oil_rt"] = {
    "commodities/brent-oil": 40 * 0.9,
    "commodities/crude-oil": 60 * 0.9,
}

holdings["501018"] = holdings_501018_19s4
holdings["160216"] = holdings_160216_19s4
holdings["160416"] = holdings_160416_19s4
holdings["162411"] = holdings_162411_19s4
holdings["161129"] = holdings_161129_19s4
holdings["160723"] = holdings_160723_19s4
holdings["162719"] = holdings_162719_19s4
holdings["163208"] = holdings_163208_19s4
holdings["165513"] = holdings_165513_19s4
holdings["161815"] = holdings_161815_bc

holdings["513030"] = holdings_513030_19s4
holdings["513030rt"] = {"8826": 95}
holdings["513500"] = holdings_513500_19s4
holdings["513500rt"] = {"8839": 99}
holdings["161125"] = holdings_161125_19s4
holdings["161125rt"] = {"8839": 99}
holdings["161130"] = holdings_161130_19s4
holdings["161130rt"] = {"8874": 94}
holdings["513100"] = holdings_513100_19s4
holdings["513100rt"] = {"8874": 99}

holdings["513880"] = holdings_513880_19s4
holdings["513520"] = holdings_513880_19s4
holdings["513000"] = holdings_513880_19s4
holdings["164906"] = holdings_164906_19s4
holdings["501021"] = holdings_501021_19s4
holdings["513050"] = holdings_513050_19s4

# 雪球和英为都没找到的金融产品合集：中证中国互联网50

# 本着比国内多出的休市日，有一个记一个的 workaround
no_trading_days = {"JPY": ["2020-03-20"]}

no_trading_days["100JPY"] = no_trading_days["JPY"]
