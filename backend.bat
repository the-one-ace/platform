@echo off
echo 正在启动后端服务...

REM 获取当前脚本所在目录
set "ROOT_DIR=%~dp0"

REM 定义 Python 可执行文件路径和后端入口脚本路径
set "PYTHON_EXE=%ROOT_DIR%runtime\python.exe"
set "BACKEND_ENTRY=%ROOT_DIR%backend\app.py"

REM 启动后端服务
start "Backend Server" cmd /k "%PYTHON_EXE% %BACKEND_ENTRY%"

REM 等待 5 秒，确保服务完全启动
ping -n 5 127.0.0.1 >nul

echo 后端服务已启动，您可以通过浏览器或客户端访问服务。
pause