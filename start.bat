@echo off
REM ---------------- 启动 start.py ----------------
REM 使用当前目录下的 Python 解释器运行 start.py
set PYTHON_CMD=python

REM 确保 start.py 在当前目录
set SCRIPT=%~dp0start.py

echo 启动 QQBot 系统...
%PYTHON_CMD% "%SCRIPT%"

pause
