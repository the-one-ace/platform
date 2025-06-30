@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

:: 获取当前脚本所在目录
set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

:: 设置路径和工具
set "NODE_EXE=%ROOT_DIR%\runtime\nodejs\node.exe"
set "YARN_EXE=%ROOT_DIR%\runtime\yarn\bin\yarn.js"
set "FRONTEND_DIR=%ROOT_DIR%\frontend\qa-platform-frontend"

:: 检查目录和文件
if not exist "%FRONTEND_DIR%" (
    echo [ERROR] frontend 目录不存在: "%FRONTEND_DIR%"
    pause
    exit /b 1
)
if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERROR] package.json 文件不存在: "%FRONTEND_DIR%\package.json"
    pause
    exit /b 1
)

:: 启动前端服务
echo [FRONTEND] 正在启动服务...
pushd "%FRONTEND_DIR%"

:: 检查Node.js和Yarn
if not exist "%NODE_EXE%" (
    echo [ERROR] node.exe 文件不存在: "%NODE_EXE%"
    popd
    pause
    exit /b 1
)
if not exist "%YARN_EXE%" (
    echo [ERROR] yarn.js 文件不存在: "%YARN_EXE%"
    popd
    pause
    exit /b 1
)

:: 设置PATH并安装依赖
set "PATH=%ROOT_DIR%\runtime\nodejs;%PATH%"
echo [FRONTEND] 安装依赖...
%NODE_EXE% %YARN_EXE% install

:: 启动服务（固定端口）
echo [FRONTEND] 启动服务...
start "Frontend Server" cmd /k "%NODE_EXE% %YARN_EXE% serve -- --port 8081 --host 0.0.0.0"

:: 等待服务完全启动
echo [SYSTEM] 等待服务启动...
:WAIT_LOOP
netstat -ano | findstr ":8081" >nul
if errorlevel 1 (
    ping -n 2 127.0.0.1 >nul
    goto :WAIT_LOOP
)
echo [SYSTEM] 服务已在端口 8081 上就绪

:: 启动浏览器
:BROWSER_LAUNCH
set "FRONTEND_PORT=8081"
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:%FRONTEND_PORT%
) else if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" http://localhost:%FRONTEND_PORT%
) else (
    start "" http://localhost:%FRONTEND_PORT%
)

echo [SYSTEM] 服务已启动，浏览器已打开。
popd
pause
exit