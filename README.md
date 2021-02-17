# Tool
瞎写的一点小脚本小工具什么的,此处的工具功能文档不完善或者规模较小，不予建立新的项目，统一放这里

## JsonpProxy
一个基于mitmproxy的jsonp漏洞挖掘辅助工具
能够匹配简单的JSONP以及通过检查关键字进行简单粗暴的匹配
## beef-python
由Python封装的beef API,并用python写了一个自动化攻击的demo
## custom_script
放置在/usr/share/beef-xss/modules/browser/hooked_domain/custom_script/的beef模块。
它可以通过eval的形式在受害者浏览器上执行自定义脚本，由于使用了base64编码所以空行或者单双引号不影响攻击，最后会把执行结果返回回来。
之所以要开发这个小玩意是因为我在尝试攻击某内嵌IE浏览器应用的时候发现调不开调试工具，于是写这个beef模块配合中间人攻击进行“远程调试”
## thinkphp5.0.24-popchain
ThinkPHP5.0.24 反序列化POP链，不适用于Windows
## addwhitelist
点击BypassUAC.exe,执行BAT，调用WMI把整个C盘添加到Windows Defender的病毒扫描白名单中
