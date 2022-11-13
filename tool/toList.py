# 本脚本用于 GFWlist 文件转IOS版 Shadowrocket 配置文件
import requests,base64,datetime,random,re

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

def is_valid_domain(value):
    ''' 校验域名是否合法 '''
    pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(value) else False

def domainList(urlList):
    ''' 被墙名单域名与广告域名处理 '''
    domain = []
    print("开始匹配域名")
    for i in range(0, len(urlList)):
        nowUrl = urlList[i]
        # 第一层过滤
        if ('@' not in nowUrl) and ( '.'  in nowUrl) and ('#' not in nowUrl) and ('!' not in nowUrl) and ('$' not in nowUrl):
            # 去除|，去除协议头
            url = nowUrl.replace("|","").replace("https://","").replace("http://","")
            # 去除第一个.
            if len(url) and url[0] == '.':
                url = url.replace(".", "", 1)
            # 去除*.
            if len(url) >2 and url[:2] == '*.':
                url = url.replace("*.", "", 1)
            # 去除^
            url = url.replace("^", "")
            # 去重以及做最后过滤
            url = url.split('/')[0]
            if is_valid_domain(url) and (url not in domain):
                print("添加域名 " + url)
                domain.append(url)
    if len(domain) == 0:
        print("未获取到任何规则")
        exit()
    domain.sort()
    return domain

def domainList2(urlList):
    ''' 白名单域名处理 '''
    domain = []
    print("开始匹配域名")
    for i in range(0, len(urlList)):
        url=urlList[i]
        if len(url):
            url = url.split("/")[1]
            if is_valid_domain(url) and (url not in domain):
                print("添加域名 " + url)
                domain.append(url)
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
    print("开始写入文件")
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
    ad= txtContent('https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt') + txtContent('https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt')
    con = conConfig(domainList(ad), 'Reject')
    con = '# ADBlock Start' + con + '\n' + '# ADBlock End'
    # 只去广告
    con2 = con + '\n' + '# Final' + '\n' + 'FINAL,DIRECT'
    writeToConf('ADBlock.conf', con2)
    # 全局代理 + 去广告
    con3 = con + '\n' + '# Final' + '\n' + 'FINAL,PROXY'
    writeToConf('ADBlock.conf', con3)
    return con

def CFWlistAndADBlock():
    # 代理墙外域名 + 去广告
    writeToConf('CFWlistAndADBlock.conf', onlyCFWlist() + '\n' + onlyADBlock())

def onlyWhitelist():
    print("Whitelist")
    con = conConfig(domainList2(txtContent('https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf')),"DIRECT")
    # 国内直连，国外代理
    con = '# Whitelist Start' + con + '\n' + '# Whitelist End' + '\n' + '# China' + '\n' + 'GEOIP,CN,DIRECT' + '\n' + '# Final' + '\n' + 'FINAL,PROXY'
    writeToConf('Whitelist.conf', con)
    return con

def WhitelistAndADBlock():
    # 国内直连，国外代理 + 去广告
    writeToConf('WhitelistAndADBlock.conf', onlyWhitelist() + '\n' + onlyADBlock())

CFWlistAndADBlock()
WhitelistAndADBlock()