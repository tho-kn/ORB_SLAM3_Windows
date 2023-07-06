set SLAM=.\x64\Release\slam.exe
set pathDatasetEgo=Workset
set videoFile=GX010059_3360

:: Could also apply mask to images to remove

:: Setting file, repeat of (image folder, timestamps), camera trajectory output file

:: %SLAM% mono_tum .\Vocabulary\ORBvoc.txt %pathDatasetEgo%\%videoFile%\Ego.yaml %pathDatasetEgo%\%videoFile%\images
%SLAM% mono_tum_vi Vocabulary/ORBvoc.txt %pathDatasetEgo%/%videoFile%/Ego.yaml %pathDatasetEgo%/%videoFile%/images %pathDatasetEgo%\%videoFile%\timestamps.txt %videoFile%