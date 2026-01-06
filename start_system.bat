@echo off
title HCI TUIO Learning System - Complete Startup
color 0A

echo ============================================
echo    HCI TUIO LEARNING SYSTEM - COMPLETE SETUP
echo ============================================
echo.

cd /d "%~dp0"

echo Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Checking and installing required packages...
python -c "import flask, flask_socketio, pandas, eventlet" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install flask flask-socketio eventlet python-osc pandas openpyxl websocket-client
) else (
    echo All packages are installed.
)

echo.
echo ============================================
echo Starting System Components...
echo ============================================
echo.

REM 1. Check if ReactVision is installed
echo [1] Checking ReactVision...
if exist "C:\Year3S5\HCI\Final_Project\HCI_Project\HCI_TUIO_Project\reactvision\reacTIVision.exe" (
    echo   ReactVision found at path
) else (
    echo   WARNING: ReactVision not found at C:\ReactVision\
    echo   Please download from: http://reactivision.sourceforge.net/
    echo   Extract to C:\ReactVision\
    echo.
    set /p "continue=Continue without ReactVision? (Y/N): "
    if /i not "%continue%"=="Y" (
        echo Setup cancelled.
        pause
        exit /b 1
    )
)

REM 2. Create ReactVision config if it doesn't exist
echo.
echo [2] Setting up ReactVision configuration...
if not exist "reactvision" mkdir reactvision
if not exist "reactvision\reacTIVision.xml" (
    echo Creating ReactVision config.xml...
    echo ^<?xml version="1.0" encoding="UTF-8"?^> > reactvision\reacTIVision.xml
    echo ^<ReactVisionConfig^> >> reactvision\reacTIVision.xml
    echo     ^<camera^> >> reactvision\reacTIVision.xml
    echo         ^<device^>0^</device^> >> reactvision\reacTIVision.xml
    echo         ^<width^>1280^</width^> >> reactvision\reacTIVision.xml
    echo         ^<height^>720^</height^> >> reactvision\reacTIVision.xml
    echo         ^<fps^>30^</fps^> >> reactvision\reacTIVision.xml
    echo     ^</camera^> >> reactvision\reacTIVision.xml
    echo     ^<fiducials^> >> reactvision\reacTIVision.xml
    echo         ^<artoolkit^> >> reactvision\reacTIVision.xml
    echo             ^<size^>80^</size^> >> reactvision\reacTIVision.xml
    echo             ^<pattern^>0^</pattern^> >> reactvision\reacTIVision.xml
    echo             ^<threshold^>120^</threshold^> >> reactvision\reacTIVision.xml
    echo         ^</artoolkit^> >> reactvision\reacTIVision.xml
    echo     ^</fiducials^> >> reactvision\reacTIVision.xml
    echo     ^<tuio^> >> reactvision\reacTIVision.xml
    echo         ^<enable^>true^</enable^> >> reactvision\reacTIVision.xml
    echo         ^<protocol^>TUIO/UDP^</protocol^> >> reactvision\reacTIVision.xml
    echo         ^<address^>127.0.0.1^</address^> >> reactvision\reacTIVision.xml
    echo         ^<port^>3333^</port^> >> reactvision\reacTIVision.xml
    echo     ^</tuio^> >> reactvision\reacTIVision.xml
    echo ^</ReactVisionConfig^> >> reactvision\reacTIVision.xml
    echo   Config file created: reactvision\reacTIVision.xml
) else (
    echo   Config file already exists: reactvision\reacTIVision.xml
)

REM 3. Start Backend Server
echo.
echo [3] Starting Backend Server (Port 5000)...
start "TUIO Backend Server" cmd /k "title TUIO Backend Server && cd backend\python_server && python main_server.py"

echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

REM 4. Start Web Interface
echo.
echo [4] Starting Web Interface (Port 5001)...
start "Web Interface" cmd /k "title Web Interface && cd frontend && python -m http.server 5001"

REM 5. Start ReactVision if available
echo.
echo [5] Starting ReactVision...
if exist "C:\Year3S5\HCI\Final_Project\HCI_Project\HCI_TUIO_Project\reactvision\reacTIVision.exe" (
    start "ReactVision" "C:\Year3S5\HCI\Final_Project\HCI_Project\HCI_TUIO_Project\reactvision\reacTIVision.exe" reactvision\reacTIVision.xml
    echo   ReactVision started with reacTIVision.xml
    timeout /t 3 /nobreak >nul
) else (
    echo   ReactVision not found, running in simulation mode
)

REM 6. Start Marker Simulator (for testing without camera)
echo.
echo [6] Starting Marker Simulator (for testing)...
start "Marker Simulator" cmd /k "title Marker Simulator && cd backend\python_server && python -c "
start "Marker Simulator" cmd /k "title Marker Simulator && cd backend\python_server && python -c "import time; print('Marker Simulator Running...'); print('Simulating TUIO markers for testing'); print('Use this when you dont have a camera'); print('Press Ctrl+C to stop'); time.sleep(9999)"

REM 7. Start System Test
echo.
echo [7] Starting System Test...
timeout /t 2 /nobreak >nul
start "System Test" cmd /k "title System Test && cd backend\testing && python test_system.py"

echo.
echo ============================================
echo        SYSTEM STARTUP COMPLETE!
echo ============================================
echo.
echo IMPORTANT URLs:
echo   Main Dashboard:  http://localhost:5001/
echo   Teacher Interface: http://localhost:5001/teacher.html
echo   Student Interface: http://localhost:5001/student.html
echo.
echo SYSTEM COMPONENTS:
echo   1. Backend Server: Running on port 5000
echo   2. Web Interface: Running on port 5001
echo   3. ReactVision: Camera and marker detection
echo   4. Marker Simulator: For testing without camera
echo   5. System Test: Checking all components
echo.
echo INSTRUCTIONS:
echo   1. Open browser to: http://localhost:5001/
echo   2. Open Teacher interface in one tab
echo   3. Open Student interface in another tab (or another computer)
echo   4. In Teacher interface: Configure and start a session
echo   5. In Student interface: Student will automatically receive the test
echo   6. Student answers using physical markers (or simulation)
echo.
echo TROUBLESHOOTING:
echo   - No markers detected? Check ReactVision camera view
echo   - Can't connect? Make sure all servers are running
echo   - Simulation mode shows markers every few seconds
echo.
echo ============================================
echo Press any key to open dashboard...
pause >nul

start http://localhost:5001/

echo.
echo All systems are running in separate windows.
echo.
echo To stop everything:
echo   1. Close all command windows
echo   2. Close ReactVision window
echo   3. Close browser tabs
echo.
echo Press any key to show marker instructions...
pause >nul

cls
echo ============================================
echo        MARKER SETUP INSTRUCTIONS
echo ============================================
echo.
echo USING REACTVISION DEFAULT MARKERS:
echo   Print the default marker sheet from ReactVision
echo   Use these marker IDs:
echo.
echo   NUMBERS (for answers):
echo     0 = Number 0     1 = Number 1     2 = Number 2
echo     3 = Number 3     4 = Number 4     5 = Number 5
echo     6 = Number 6     7 = Number 7     8 = Number 8
echo     9 = Number 9
echo.
echo   OPERATORS (for math):
echo     10 = Plus (+)      11 = Minus (-)
echo     12 = Multiply (×)  13 = Divide (÷)
echo     14 = Equals (=)
echo.
echo   CONTROL MARKERS:
echo     50 = Confirm button (GREEN) - move to top-right corner
echo     51 = Navigation dial (YELLOW) - rotate to select
echo     52 = Clear answer
echo     53 = Request hint
echo.
echo   TABLE AREAS:
echo     Left side: Answer area (place number/operator markers)
echo     Top-right corner: Confirm area (place marker 50 here to submit)
echo     Top-left corner: Navigation area (for teacher menu)
echo.
echo SIMULATION MODE:
echo   If you don't have printed markers, the system will simulate
echo   marker detection automatically for testing.
echo.
echo ============================================
echo.
pause