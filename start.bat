@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

:: ��ȡ��ǰ�ű�����Ŀ¼
set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

:: ����·���͹���
set "NODE_EXE=%ROOT_DIR%\runtime\nodejs\node.exe"
set "YARN_EXE=%ROOT_DIR%\runtime\yarn\bin\yarn.js"
set "FRONTEND_DIR=%ROOT_DIR%\frontend\qa-platform-frontend"

:: ���Ŀ¼���ļ�
if not exist "%FRONTEND_DIR%" (
    echo [ERROR] frontend Ŀ¼������: "%FRONTEND_DIR%"
    pause
    exit /b 1
)
if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERROR] package.json �ļ�������: "%FRONTEND_DIR%\package.json"
    pause
    exit /b 1
)

:: ����ǰ�˷���
echo [FRONTEND] ������������...
pushd "%FRONTEND_DIR%"

:: ���Node.js��Yarn
if not exist "%NODE_EXE%" (
    echo [ERROR] node.exe �ļ�������: "%NODE_EXE%"
    popd
    pause
    exit /b 1
)
if not exist "%YARN_EXE%" (
    echo [ERROR] yarn.js �ļ�������: "%YARN_EXE%"
    popd
    pause
    exit /b 1
)

:: ����PATH����װ����
set "PATH=%ROOT_DIR%\runtime\nodejs;%PATH%"
echo [FRONTEND] ��װ����...
%NODE_EXE% %YARN_EXE% install

:: �������񣨹̶��˿ڣ�
echo [FRONTEND] ��������...
start "Frontend Server" cmd /k "%NODE_EXE% %YARN_EXE% serve -- --port 8081 --host 0.0.0.0"

:: �ȴ�������ȫ����
echo [SYSTEM] �ȴ���������...
:WAIT_LOOP
netstat -ano | findstr ":8081" >nul
if errorlevel 1 (
    ping -n 2 127.0.0.1 >nul
    goto :WAIT_LOOP
)
echo [SYSTEM] �������ڶ˿� 8081 �Ͼ���

:: ���������
:BROWSER_LAUNCH
set "FRONTEND_PORT=8081"
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:%FRONTEND_PORT%
) else if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" http://localhost:%FRONTEND_PORT%
) else (
    start "" http://localhost:%FRONTEND_PORT%
)

echo [SYSTEM] ������������������Ѵ򿪡�
popd
pause
exit