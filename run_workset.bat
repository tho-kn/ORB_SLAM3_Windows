@echo off
setlocal

set SLAM=.\x64\Release\slam.exe
set pathScript=Workset
set pathDatasetEgo=Workset\Data

REM Check command line arguments
if "%~1"=="" (
    echo Usage: %~nx0 video_file resolution
    exit /b
)
if "%~2"=="" (
    echo Usage: %~nx0 video_file resolution
    exit /b
)

set videoFile=%~1
set resolution=%~2

REM New directory created by Video_to_Dataset.py script
set newDir=%pathDatasetEgo%\%videoFile%_%resolution%

REM Check if images directory exists inside newDir
if not exist "%newDir%\images\" (
    REM Call Python script to split video into frames if directory does not exist
    python %pathScript%\Video_to_Dataset.py %pathDatasetEgo%\%videoFile%.MP4 %resolution%
)

if not exist "%newDir%\masked_images\" (
    REM Apply mask using Apply_Mask.py script
    python %pathScript%\Apply_Mask.py %newDir%\images %newDir%\mask
)

REM Set new directory for masked images
set newDirMaskedImages=%newDir%\masked_images
if not exist "%newDirMaskedImages%\" (
    set newDirMaskedImages=%newDir%\images
)

REM Execute SLAM with the new masked images directory
%SLAM% mono_tum_vi Vocabulary/ORBvoc.txt %newDir%\Ego.yaml %newDirMaskedImages% %newDir%\timestamps.txt %videoFile%

endlocal
