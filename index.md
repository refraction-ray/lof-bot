LOF-BOT
======
作者：[**refraction-ray**](https://github.com/refraction-ray/)

项目地址：[**lof-bot**](https://github.com/refraction-ray/lof-bot)

🎉 You need a 🤖, not a 👻.

## 净值预测基金列表：

<p align="center">
<a href="https://github.com/refraction-ray/lof-bot/actions"><img alt="Actions Status" src="https://github.com/refraction-ray/lof-bot/workflows/gh/badge.svg"></a>
</p>

#### 原油类基金

* [南方原油](/lof-bot/SH501018.html) (501018)
* [华宝油气](/lof-bot/SZ162411.html) (162411)
* [国泰商品](/lof-bot/SZ160216.html) (160216)
* [嘉实原油](/lof-bot/SZ160723.html) (160723)
* [诺安油气](/lof-bot/SZ163208.html) (163208)
* [易方达原油](/lof-bot/SZ161129.html) (161129)
* [广发道琼斯石油](/lof-bot/SZ162719.html) (162719)

#### 其他 QDII 基金

* [华安德国30](/lof-bot/SH513030.html) (513030/000614)
* [博时标普500](/lof-bot/SH513500.html) (513500/050025)
* [易方达纳斯达克100](/lof-bot/SZ161130.html) (161130)
* [交银中国互联](/lof-bot/SZ164906.html) (164906)
* [华宝香港中小](/lof-bot/SH501021.html) (501021)
* 日经225:
  * [513880](/lof-bot/SH513880.html)
  * [513520](/lof-bot/SH513520.html)
  * [513000](/lof-bot/SH513000.html)

More funds are coming soon.

* 因回测可预测性极差，而没有列入的标的：161226
* 因未找到可靠的跟踪标的数据源，而暂未列入的标的：513050，160416

*净值预估的页面更新机制可能还存在问题，数据仅供参考，如果预测数据过于离谱，可能是有 bug 待捉。*

## 场内实时溢价提醒

<p align="center">
<a href="https://github.com/refraction-ray/lof-bot/actions"><img alt="Actions Status" src="https://github.com/refraction-ray/lof-bot/workflows/pb/badge.svg"></a>
</p>

场内跟踪基金溢价阈值超过一定限度，自动通过 pushbullet 通知。如果你也想获取该提醒通知功能，请 fork 该项目，并且在 forked 项目 setting 中 secrets 添加自己 pushbullet 的 token 作为 ``PB_TOKEN`` 即可。

## 基金相关研究

比起 [xalpha](https://github.com/refraction-ray/xalpha) 项目，这里的研究更侧重于基金溢价行为和净值预测等。

亮点研究：

* [不同 QDII 基金净值可预测性](https://nbviewer.jupyter.org/github/refraction-ray/lof-bot/blob/master/studies/qdii_lof_prediction.ipynb)
* [不同 QDII 基金对基准的追踪情况和购买建议分析](https://nbviewer.jupyter.org/github/refraction-ray/lof-bot/blob/master/studies/compwithbenchmark.ipynb)

Stay tuned for more.