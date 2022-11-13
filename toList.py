# 本脚本用于 GFWlist 文件转IOS版 Shadowrocket 配置文件
import requests,base64,datetime

# 获取 GFWlist 文件
try:
    # GFWlist 由 https://github.com/gfwlist/gfwlist 提供
    content=requests.get("https://pagure.io/gfwlist/raw/master/f/gfwlist.txt",  headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}).content
    decoder = base64.b64decode(content)
    urlList = decoder.decode('utf-8').split("\n")
except Exception as err:
    print("获取GFWlist错误")
    print(err)
    exit()

# 获取 GFWlist 更新时间
try:
    timestamp=urlList[5].split(": ")[1]
    timef=timestamp[-5:]
    lastModified = datetime.datetime.strptime(timestamp[:-6], '%a, %d %b %Y %H:%M:%S')
    timei=int(timef[:3])
    if timei >8:
        lastModified -= datetime.timedelta(hours = timei - 8)
    else :
        lastModified += datetime.timedelta(hours = abs(8 - timei))
    lastModified = '\n'+ '# 列表更新时间: ' + str(lastModified)
except:
    lastModified =""

# 获取主域名
domain = []
for i in range(0, len(urlList)):
    # 过滤
    if '@' not in urlList[i] and '.' in urlList[i] and '!' not in urlList[i]:
        # 去除|，去除协议头
        url = urlList[i].replace("|","").replace("https://","").replace("http://","")
        # 去除第一个.
        if len(url) and url[0] == '.':
            url = url.replace(".", "", 1)
        # 去除*.
        if len(url) >2 and url[:2] == '*.':
            url = url.replace("*.", "", 1)
        # 获取主域名
        url = url.split('/')[0]
        # 去重以及做最后过滤
        if (url not in domain) and  ('*' not in url) and len(url):
            domain.append(url)
if len(domain) == 0:
    print("未获取到任何规则")
    print("反馈: https://github.com/wildonchen/shadowrocket-GFWlist/issues")
    exit()

# 域名通过 0-9a-Z 排序
domain.sort()

# 拼接成 DOMAIN-SUFFIX,t.me,PROXY 这样的格式
con = ''
for i in range(0, len(domain)):
    con += '\n' + 'DOMAIN-SUFFIX,' +domain[i] + ',PROXY'

# 拼接文件，最终写入 GFWlist.conf
try:
    ff = open('GFWlist.conf','w')
    with open('template.conf','r') as f:
        for line_list in f.readlines():
            # 在 [Rule] 下面新增规则
            if line_list == '[Rule]\n':
                line_list = '[Rule]' + '\n' + '# GFWlist Start' + lastModified + con + '\n' + '# GFWlist End' + '\n'
            ff.write(line_list)
    print('共写入 ' + str(len(domain)) + ' 个被墙域名规则')
except Exception as err:
    print("写入文件错误")
    print(err)
    exit()