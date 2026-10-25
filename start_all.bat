@echo off
setlocal
title ARB SoftTech AI Calling Agent Launcher (Native Sarvam AI Mode)
echo ========================================================
echo       Starting ARB SoftTech Native Sarvam AI Calling System
echo       (Zero Docker / Zero Kokoro - 100%% Sarvam AI)
echo ========================================================
echo.

set "BASE_DIR=%~dp0"
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

echo [1/3] Launching FastAPI Backend on Port 8001 (Direct Sarvam AI Engine)...
cd /d "%BASE_DIR%\backend"
if exist ".\.venv\Scripts\python.exe" (
    start "ARB SoftTech Backend (Port 8001)" cmd /k ".\.venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --reload-dir app --reload-exclude *.env --reload-exclude *.db"
    echo [OK] Backend server launched in a new window.
) else (
    echo [ERROR] Virtual environment not found at backend\.venv
)
echo.

echo [2/3] Launching React Frontend on Port 5173...
cd /d "%BASE_DIR%\frontend_1"
if exist "node_modules" (
    start "ARB SoftTech Frontend (Port 5173)" cmd /k "npm run dev"
    echo [OK] Frontend dev server launched in a new window.
) else (
    echo [ERROR] node_modules not found in frontend_1. Please run npm install.
)
echo.

echo [3/3] Launching Telephony Tunnel (Ngrok Port 8001 directly to Backend)...
where ngrok >nul 2>&1
if %errorlevel% equ 0 (
    start "ARB SoftTech Ngrok Tunnel (Port 8001)" cmd /k "ngrok http 8001"
    echo [OK] Ngrok public tunnel launched for VoBiz calls directly to FastAPI Backend.
) else (
    echo [WARNING] ngrok not found in PATH. Please start ngrok manually.
)
echo.

echo ========================================================
echo All services launched in Native Sarvam AI mode!
echo - Frontend Dashboard:   http://localhost:5173
echo - Backend API Docs:     http://localhost:8001/docs
echo - Telephony Webhooks:   https://parish-coconut-herself.ngrok-free.dev
echo ========================================================
ping -n 6 127.0.0.1 >nul 2>&1
exit /b 0
