@echo off
setlocal enabledelayedexpansion

REM Set paths and other parameters
set SLAM=.\x64\Release\slam.exe
set pathScript=Workset
set pathDatasetEgo=Workset\Data
set downsampleRate=1

REM Check command line arguments
if "%~1"=="" (
    echo Usage: %~nx0 video_file resolution [downsample_rate]
    exit /b
)
if "%~2"=="" (
    echo Usage: %~nx0 video_file resolution [downsample_rate]
    exit /b
)

set videoFile=%~1
set resolution=%~2

REM Set downsample rate if specified
if not "%~3"=="" (
    set downsampleRate=%~3 
)

REM New directory created by Video_to_Dataset.py script
set newDir=%pathDatasetEgo%\%videoFile%_%resolution%

if not exist "%newDir%\Ego.yaml" (
    REM Call Python script to create Ego.yaml file if it does not exist
    echo Creating Ego.yaml file...
    python %pathScript%\Create_Setting.py %pathDatasetEgo%\%videoFile%.MP4 %resolution%
    
    if not exist "%newDir%\Ego.yaml" (
        echo Error: Ego.yaml file not created
        exit /b
    )
)

REM Check if images directory exists inside newDir
if not exist "%newDir%\images\" (
    REM Call Python script to split video into frames if directory does not exist
    echo Splitting video into frames...
    python %pathScript%\Video_to_Dataset.py %pathDatasetEgo%\%videoFile%.MP4 %resolution%
)

if not exist "%newDir%\masked_images\" (
    REM Apply mask using Apply_Mask.py script
    echo Applying mask to images...
    python %pathScript%\Apply_Mask.py %newDir%\images %newDir%\mask
)

REM Set new directory for masked images
set newDirMaskedImages=%newDir%\masked_images
if not exist "%newDirMaskedImages%\" (
    set newDirMaskedImages=%newDir%\images
)

REM Use original timestamps file if downsample rate is 1
if "%downsampleRate%"=="1" (
    set timestampsFile=%newDir%\timestamps.txt
) else (
    REM Create new timestamps file with every nth timestamp
    set i=0
    set timestampsFile=%newDir%\timestamps_downsampled.txt
    > "%timestampsFile%" (
        for /F "usebackq delims=" %%a in ("%newDir%\timestamps.txt") do (
            set /A "i=(i+1)%%downsampleRate"
            if !i!==1 echo %%a
        )
    )
)

REM Execute SLAM with the new masked images directory and (possibly downsampled) timestamps
%SLAM% mono_tum_vi Vocabulary/ORBvoc.txt %newDir%\Ego.yaml %newDirMaskedImages% %timestampsFile% %videoFile%_%resolution%

endlocal
