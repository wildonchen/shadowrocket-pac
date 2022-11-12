# 本脚本用于SSR GFWlist pac文件转IOS版shadowrocket配置文件
import re

try:
    # 打开SSR pac文件，请确保有安装SSR软件，以及生成了GFWlist pac文件
    file_object = open('D:\Portable Application\ShadowsocksR-win-4.9.2\pac.txt','r')
except:
    print("pac.txt 文件不存在或路径错误")
    exit()
all_the_text = file_object.read()
# 格式化文件并将rules存为进数组
all_the_text = all_the_text.replace("\t","").replace("\n","")
text = re.findall('(?<=var rules = \[).*?(?=\];)', all_the_text)
text = text[0].replace("\"","")
urlList = text.split(",")
# 对rules做处理
domain = []
for i in range(0, len(urlList)):
    # 删除过滤
    if '@' not in urlList[i] and '.' in urlList[i]:
        # 去除|，去除协议头
        domain1 = urlList[i].replace("|","").replace("https://","").replace("http://","")
        # 去除第一个.
        if len(domain1) and domain1[0] == '.':
            domain1 = domain1.replace(".", "", 1)
        # 获取主域名
        domain1 = domain1.split('/')[0]
        if domain1 not in domain:
            domain.append(domain1)
file_object.close()

if len(domain) == 0:
    print("未能正确识别文件")
    exit()
con = ''
for i in range(0, len(domain)):
    # 拼接成 DOMAIN-SUFFIX,t.me,PROXY 这样的格式
    con += '\n' + 'DOMAIN-SUFFIX,' +domain[i] + ',PROXY'

try:
    # 拼接文件，最终写入 GFWlist.conf
    ff = open('GFWlist.conf','w')
    with open('template.conf','r') as f:
        line = f.readlines()
        for line_list in line:
            line_new =line_list.replace('\n','')
            if line_new == '[Rule]':
                line_new = line_new + '\n' + '# GFWlist' +  con
            line_new = line_new  +'\n'
            ff.write(line_new)
except:
    print("写入文件错误")
    exit()