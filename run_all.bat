@echo off
echo Starting PupDB Distributed System...

:: Kiểm tra xem có môi trường ảo .venv không, nếu có thì dùng python của venv
IF EXIST .venv\Scripts\python.exe (
    set PYTHON_EXEC=.venv\Scripts\python.exe
) ELSE (
    set PYTHON_EXEC=python
)

echo Su dung trinh bien dich Python tai: %PYTHON_EXEC%

echo Starting Coordinator (Port 5050)...
start "Coordinator" cmd /k "%PYTHON_EXEC% coordinator.py"

echo Starting Shard 0 (Port 5001)...
start "Shard 0" cmd /k "set NODE_ID=shard_0&& set PORT=5001&& %PYTHON_EXEC% node.py"

echo Starting Shard 1 (Port 5002)...
start "Shard 1" cmd /k "set NODE_ID=shard_1&& set PORT=5002&& %PYTHON_EXEC% node.py"

echo Starting Shard 2 (Port 5003)...
start "Shard 2" cmd /k "set NODE_ID=shard_2&& set PORT=5003&& %PYTHON_EXEC% node.py"

echo All services started!
echo Vui long cho vai giay de cac cua so server khoi dong.
echo Sau do ban co the chay "python main.py" (hoac .\main.py) o cua so hien tai.
pause
