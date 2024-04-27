# e0e1-abroad

### 简介

> 用于收集国外众测项目内容，如项目其中的url、根域、app对应的内容等
> 可用于联结自动化工具，进行扫描、信息收集、漏扫、fuzz等

> 当前支持的国外众测系统：Intigriti、Hackerone、Bugcrowd、Openbugbounty、immunefi、inspectiv

### config配置

> 需要进行配置的有：intigriti、hackerone、bugcrowd、inspectiv





### 使用方法

```
1.单纯获取Intigriti 所有程序内容
python3 e0e1-abroad.py -it

2.获取Intigriti 所有程序内容，且额外提取url、app的内容出来
python3 e0e1-abroad.py -it --url --app

3.获取Intigriti 所有程序内容，且额外提取url、app的内容出来，并且将url的内容进行优化
python3 e0e1-abroad.py -it --url --app --url-op
```
