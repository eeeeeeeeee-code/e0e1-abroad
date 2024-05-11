# e0e1-abroad

### 简介

> 用于收集国外众测项目内容，如项目其中的url、根域、app对应的内容等
> 可用于联结自动化工具，进行扫描、信息收集、漏扫、fuzz等

> 当前支持的国外众测系统：Intigriti、Hackerone、Bugcrowd、Openbugbounty、immunefi、inspectiv、yeswehack

### config配置

> 需要进行配置的有：intigriti、hackerone、bugcrowd、inspectiv、yeswehack

intigriti api-key配置：[key获取地址](https://app.intigriti.com/researcher/personal-access-tokens)

hackerone 配置：[key获取地址](https://hackerone.com/settings/api_token/edit)   和 自己的名字

Bugcrowd 配置：登录以后，获取cookie中 _bugcrowd_session的值

inspectiv 配置：登录以后，获取Authorization：Token后面的值

yeswehack 配置：登录以后，获取Authorization: Bearer后面的值

### 使用方法

```
1.单纯获取Intigriti 所有程序内容
python3 e0e1-abroad.py -it

2.获取Intigriti 所有程序内容，且额外提取url、app的内容出来
python3 e0e1-abroad.py -it --url --app

3.获取Intigriti 所有程序内容，且额外提取url、app的内容出来，并且将url的内容进行优化
python3 e0e1-abroad.py -it --url --app --url-op
```
### 效果展示
![image](https://github.com/eeeeeeeeee-code/e0e1-abroad/assets/115862499/069ecfa2-ba08-4044-bedf-793106f715cc)


![0482e1b53827cb22e5407b3608551c6](https://github.com/eeeeeeeeee-code/e0e1-abroad/assets/115862499/e1a514d9-07d1-4e24-8509-171b380f090b)
