# 本脚本用于 GFWlist 文件转IOS版 Shadowrocket 配置文件
import requests,base64,random,re

def txtContent(url,type=""):
    ''' 获取远程文件 '''
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]
    headers={
        'User-Agent':random.choice(user_agent_list),'Connection':'close'
    }
    print("开始获取远程文件")
    try:
        content=requests.get(url,  headers=headers).content
        if type == "base64":
            content=base64.b64decode(content)
        textList = content.decode('utf-8').split("\n")
        return textList
    except Exception as err:
        print("获取远程文件失败")
        print(err)
        exit()

def domainList(urlList):
    ''' 域名处理 '''
    domain = []
    print("开始匹配域名")
    for i in range(0, len(urlList)):
        nowUrl = urlList[i]
        # 基本过滤
        if ('@' not in nowUrl)  and ('#' not in nowUrl) and ('!' not in nowUrl) and ('$' not in nowUrl):
            # 正则匹配
            pattern = re.compile(r"(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}")
            url = pattern.findall(nowUrl)
            if len(url) and url[0] not in domain:
                print('匹配到域名 ' + url[0])
                domain.append(url[0])
    if len(domain) == 0:
        print("未获取到任何规则")
        exit()
    domain.sort()
    return domain

def conConfig(domain, type="PROXY"):
    ''' 拼接成配置 '''
    con = ''
    for i in range(0, len(domain)):
        con += '\n' + 'DOMAIN-SUFFIX,' +domain[i] + ',' + type
    return con

def writeToConf(filename,con):
    ''' 合并模板写入 conf 文件 '''
    print("开始写入 " + filename)
    try:
        ff = open('../'+filename,'w')
        with open('template.conf','r') as f:
            for line_list in f.readlines():
                # 在 [Rule] 下面新增规则
                if line_list == '[Rule]\n':
                    line_list = '[Rule]' + '\n'  + con + '\n'
                ff.write(line_list)
        print("写入完成")
        return True
    except Exception as err:
        print("写入文件错误")
        print(err)
        exit()

def onlyCFWlist():
    print("GFWlist")
    con = conConfig(domainList(txtContent('https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt', 'base64')))
    # 代理墙外域名
    con = '# GFWlist Start' + con + '\n' + '# GFWlist End' + '\n' + '# Final' + '\n' + 'FINAL,DIRECT'
    writeToConf('GFWlist.conf', con)
    return con

def onlyADBlock():
    print("ADBlock")
    #ad= txtContent('https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt') + txtContent('https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt')
    ad = txtContent('https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt')
    con = conConfig(domainList(ad), 'Reject')
    con = '# ADBlock Start' + con + '\n' + '# ADBlock End'
    # 只去广告
    con2 = con + '\n' + '# Final' + '\n' + 'FINAL,DIRECT'
    writeToConf('ADBlock.conf', con2)
    # 全局代理 + 去广告
    con3 = con + '\n' + '# Final' + '\n' + 'FINAL,PROXY'
    writeToConf('ADBlockAndProxy.conf', con3)
    return con

def CFWlistAndADBlock():
    # 代理墙外域名 + 去广告
    writeToConf('CFWlistAndADBlock.conf', onlyCFWlist() + '\n' + onlyADBlock())

def onlyWhitelist():
    print("Whitelist")
    con = conConfig(domainList(txtContent('https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf')),"DIRECT")
    # 国内直连，国外代理
    con = '# Whitelist Start' + con + '\n' + '# Whitelist End' + '\n' + '# China' + '\n' + 'GEOIP,CN,DIRECT' + '\n' + '# Final' + '\n' + 'FINAL,PROXY'
    writeToConf('Whitelist.conf', con)
    return con

def WhitelistAndADBlock():
    # 国内直连，国外代理 + 去广告
    writeToConf('WhitelistAndADBlock.conf', onlyWhitelist() + '\n' + onlyADBlock())

CFWlistAndADBlock()
WhitelistAndADBlock()