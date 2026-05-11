@echo off
REM Use this if "adb" or "appium" is not found in a new Command Prompt.
set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
set "PATH=%ANDROID_HOME%\platform-tools;%APPDATA%\npm;%PATH%"
echo ANDROID_HOME=%ANDROID_HOME%
where adb
where appium
appium
