import requests,base64,datetime
# 获取 GFWlist 文件
urlList="Last Modified: Sat, 05 Nov 2022 15:00:57 +0400"


timestamp=urlList.split(": ")[1]
timef=timestamp[-5:]
if '-' in timef:
    timeb=abs(int(timef[:3])) + 8
else:
    timeb=abs(int(timef[:3]) - 8)
lastModified = datetime.datetime.strptime(timestamp[:-6], '%a, %d %b %Y %H:%M:%S') + datetime.timedelta(hours=timeb)
print(lastModified)