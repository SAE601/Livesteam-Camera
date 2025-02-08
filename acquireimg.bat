@echo off
REM Check if two arguments are passed
if "%~1"=="" (
    echo "[ERROR] No input .ts file specified."
    echo "Usage: capture_image.bat <input_ts_file> <output_image_name>"
    exit /b
)

if "%~2"=="" (
    echo "[ERROR] No output file name specified."
    echo "Usage: capture_image.bat <input_ts_file> <output_image_name>"
    exit /b
)

REM Input parameters
set input_file=%~1
set output_file=%~2

REM Display input information
echo "[INFO] Input: %input_file%"
echo "[INFO] Output: %output_file%"

REM Run FFmpeg to capture the image
ffmpeg -i "%input_file%" -vf "select=eq(n\,1)" -vsync vfr -q:v 1 "%output_file%"

REM Check if FFmpeg command was successful
if %errorlevel% neq 0 (
    echo "[ERROR] Image capture failed."
    exit /b
)

echo "[INFO] Image successfully captured: %output_file%"
exit /b
