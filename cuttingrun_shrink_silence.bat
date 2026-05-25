@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
title 批量压缩静音到 1/3 - 文件夹递归版

rem ===== 以 bat 所在目录为 BASE =====
set "BASE=%~dp0"
set "IN=%BASE%in"
set "OUT=%BASE%out"
set "SCRIPT=%BASE%shrink_silence.py"

echo [1/7] 切換到 %BASE%
cd /d "%BASE%" || (echo [錯誤] 進入 %BASE% 失敗 & pause & exit /b 1)

echo [2/7] 檢查 Python...
where python >nul 2>&1 || (echo [錯誤] 未找到 Python 3.x & pause & exit /b 1)

echo [3/7] 檢查 pydub 依賴...
python -c "import importlib; importlib.import_module('pydub')" 1>nul 2>nul
if errorlevel 1 (
  echo [提示] 正在安裝 pydub...
  python -m pip install --upgrade pip
  if errorlevel 1 (echo [錯誤] pip 升級失敗 & pause & exit /b 1)
  python -m pip install pydub
  if errorlevel 1 (echo [錯誤] 安裝 pydub 失敗 & pause & exit /b 1)
) else (
  echo [OK] pydub 就緒。
)

echo [4/7] 檢查 ffmpeg/ffprobe...
where ffmpeg >nul 2>&1 && where ffprobe >nul 2>&1 (
  echo [OK] 已檢測到 ffmpeg/ffprobe。
) else (
  echo [警告] 未在 PATH 中檢測到 ffmpeg 或 ffprobe。
  echo        建議將 ffmpeg 的 bin 目錄加入 PATH，或把 ffmpeg.exe/ffprobe.exe 放到 %BASE%。
)

echo [5/7] 檢查 in/out 目錄...
if not exist "%IN%"  (echo [提示] 未發現 %IN% ，正在創建... & mkdir "%IN%")
if not exist "%OUT%" (mkdir "%OUT%")

if not exist "%SCRIPT%" (
  echo [錯誤] 未找到腳本：%SCRIPT%
  pause & exit /b 1
)

echo [6/7] 開始處理：%IN%  ->  %OUT%
echo.
python "%SCRIPT%"
set "ERR=%ERRORLEVEL%"
echo.

echo [7/7] 結果：
if "%ERR%" NEQ "0" (
  echo [完成] 但腳本返回碼=%ERR%（如有錯誤，上方已輸出原因）。
) else (
  echo [完成] 全部處理結束。
)

echo.
echo 打開輸出文件夾...
start "" "%OUT%"
echo.
pause
endlocal
