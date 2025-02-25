@echo off
REM Check if two arguments are passed
if "%~1"=="" (
    echo [ERROR] No video device specified.
    echo Usage: stream.bat "<video_device>" "<output_file>"
    exit /b 1
)

if "%~2"=="" (
    echo [ERROR] No output file specified.
    echo Usage: stream.bat "<video_device>" "<output_file>"
    exit /b 1
)

REM Input parameters
set VIDEO_STREAM=%~1
set OUTPUT_FILE=%~2
set KEY_FRAME=50

REM Display input information
echo [INFO] Video device: %VIDEO_STREAM%
echo [INFO] Output file: %OUTPUT_FILE%

REM Run FFmpeg for streaming
ffmpeg -f dshow -i video="%VIDEO_STREAM%" -g %KEY_FRAME% -c:v libx264 -preset ultrafast -sc_threshold 0 -f hls -hls_time 1 -hls_list_size 2 -hls_flags delete_segments "%OUTPUT_FILE%"

exit /b
