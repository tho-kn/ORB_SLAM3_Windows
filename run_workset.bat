set SLAM=x64\Release\slam.exe
set pathDatasetEgo=.\Workset

:: TODO: Create a script to generate image folder and timestamps from a video file
:: Maybe also adjust calibration depending on the input dimensions
:: Could also apply mask to images to remove the black borders

:: Setting file, repeat of (image folder, timestamps), camera trajectory output file
%SLAM% mono_tum_vi %pathDatasetEgo%/Ego.yaml \
    %pathDatasetEgo%/dataset-room1_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room1_512.txt dataset-room1_512_mono