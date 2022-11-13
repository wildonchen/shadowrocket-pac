# GFWlist

根据 [GFWlist](https://github.com/gfwlist/gfwlist) 生成的 Shadowrocket 配置文件，用于IOS端。这和默认的配置文件有什么区别？这就需要知道什么是 PAC 了。

> PAC就是让代理软件通过PAC代理规则文件 进行上网流量分流，比如让国内IP、域名的流量直连，让国外的IP、域名通过SSR代理连接。

GFWlist.conf 是为了只让被墙域名使用代理，尽可能的避免使用代理，减少代理流量，间接提升个人隐私安全。

如果你不知道这几个文件是什么。那么你只需要知道 GFWlist.conf 怎么用。

## 怎么使用

你需要先复制这个URL：https://raw.githubusercontent.com/wildonchen/shadowrocket-GFWlist/main/GFWlist.conf

再打开IOS 端的 Shadowrocket 软件，然后按照下图步骤操作即可：

![demo](tool/images/demo.gif)

至此好好享受吧。如果你单纯只是使用，下面的内容就不用再看。

如果提示错误的URL，请连接上机场后尝试。

## toList.py

如果你有这方便的兴趣，我想你能看懂里面的注释，这是一个转换脚本。用于 GFWlist 转  Shadowrocket 配置文件。

```shell
# 如果没有 requests 库则执行安装命令
pip install requests

# 如果没有 pybase64 库则执行安装命令
pip install pybase64

# 执行转换脚本
python toList.py
```

即可在同目录生成最新的 GFWlist.conf 文件。

template.conf 文件是一个 Shadowrocket 配置模板，用于合并生成新的 GFWlist.conf 文件。当然你也可以编辑它进行自定义，合并后依然会存在。

## 最后想说

根据 GFWlist 得到的被墙域名，只能涵盖大部分常用域名，但依然会有被墙的域名没有收录，如果有需要，欢迎提出反馈，用于及时更新到 GFWlist.conf，谢谢。

