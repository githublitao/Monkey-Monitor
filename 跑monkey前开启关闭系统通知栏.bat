@echo off
cls
title 别忘了跑monkey啊
:menu
cls
color 0A
echo.
echo 1.禁用systemui并重启
echo.
echo 2.启用systemui并重启
echo.
echo q.退出
echo.
:cho
set choice=
set /p choice=          请选择:
IF NOT "%choice%"=="" SET choice=%choice:~0,1%
if /i "%choice%"=="1" goto disable
if /i "%choice%"=="2" goto enable
if /i "%choice%"=="Q" exit
echo 选择无效，请重新输入
echo.
goto cho
:disable
adb shell "su -c" pm disable com.android.systemui
adb shell reboot
pause&exit
:enable
adb shell "su -c" pm enable com.android.systemui
adb shell reboot
pause&exit