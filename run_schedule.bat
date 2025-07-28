@echo off
setlocal

echo 🛠 Activating virtual environment...

:: Use the virtual environment's Python interpreter
set PYTHON=V:\TIAA_ETL_Pipeline\TIAA_ETL_Pipeline\TIAA\Scripts\python.exe

:: Check if the Python executable exists
if not exist "%PYTHON%" (
    echo ❌ Virtual environment Python not found: %PYTHON%
    goto end
)

:: Run only the Scrapy job script
echo 🚀 Running ETL pipeline (Scrapy + CSV + Supabase)...
%PYTHON% V:\TIAA_ETL_Pipeline\TIAA_ETL_Pipeline\run_scrapy_job.py

if %ERRORLEVEL% EQU 0 (
    echo ✅ ETL Pipeline completed successfully.
) else (
    echo ❌ ETL Pipeline failed.
)

:end
exit /b