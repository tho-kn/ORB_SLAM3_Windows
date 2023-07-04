import cv2
import os
import numpy as np
import sys
from datetime import datetime
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import yaml # pip install PyYAML

def get_creation_time(video_path):
    parser = createParser(video_path)
    if not parser:
        print(f"Unable to parse file: {video_path}")
        return None
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print(f"Metadata extraction error: {err}")
            return None
        if not metadata:
            print(f"Unable to extract metadata.")
            return None
        for line in metadata.exportPlaintext():
            if "Creation date" in line:
                creation_date_str = line.split(": ")[1]
                creation_date = datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
                timestamp_ns = int(creation_date.timestamp() * 1e9)
                return timestamp_ns
        return None

def adjust_yaml_file(yaml_path, output_path, scale_factor):
    with open(yaml_path, 'r') as stream:
        data = yaml.safe_load(stream)

    # Adjust parameters
    data['Camera']['fx'] *= scale_factor
    data['Camera']['fy'] *= scale_factor
    data['Camera']['cx'] *= scale_factor
    data['Camera']['cy'] *= scale_factor
    data['Camera']['width'] = int(data['Camera']['width'] * scale_factor)
    data['Camera']['height'] = int(data['Camera']['height'] * scale_factor)

    with open(output_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def video_to_frames(video_path, default_base_timestamp_ns, output_resolution):
    base_timestamp_ns = get_creation_time(video_path)

    if base_timestamp_ns is None:
        base_timestamp_ns = default_base_timestamp_ns

    if not os.path.exists(video_path):
        print("Video file not found")
        return

    video_name = os.path.basename(video_path).split(".")[0]
    output_dir = os.path.join("./Workset", f"{video_name}_{output_resolution}")
    os.makedirs(output_dir, exist_ok=True)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print("Original Video Dimension: ", int(width), 'x', int(height))
    print("FPS: ", fps)

    frame_number = 0
    timestamps = []
    while True:
        ret, frame = video.read()

        if not ret:
            break
        
        # Crop the frame to a square
        crop_size = int(min(width, height))
        x = int((width - crop_size) // 2)
        y = int((height - crop_size) // 2)
        cropped = frame[y:y+crop_size, x:x+crop_size]

        # Resize the cropped frame
        resized = cv2.resize(cropped, (output_resolution, output_resolution))

        # Calculate timestamp in nanoseconds, add base timestamp, and save it
        timestamp_ns = int(frame_number / fps * 1e9) + base_timestamp_ns
        timestamps.append(timestamp_ns)

        # Save the resized frame as image
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        output_path = os.path.join(images_dir, f"{timestamp_ns}.png")
        cv2.imwrite(output_path, resized)

        frame_number += 1

    # Save the timestamps to a text file
    timestamps_path = os.path.join(output_dir, "timestamps.txt")
    with open(timestamps_path, "w") as f:
        for timestamp in timestamps:
            f.write(f"{timestamp}\n")

    # Adjust and copy the yaml file
    yaml_file_path = "./Workset/Ego.yaml"
    output_yaml_path = os.path.join(output_dir, "Ego.yaml")
    adjust_yaml_file(yaml_file_path, output_yaml_path, output_resolution/3360)

    print(f"Saved frames, timestamps, and yaml to {output_dir}")

def main():
    default_base_timestamp_ns = 1403636579763555584

    # Check if video path is given as a command-line argument
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        Tk().withdraw()  # Prevent Tkinter from creating an extra window
        video_path = askopenfilename()

    # Check if output resolution is given as a command-line argument
    if len(sys.argv) > 2:
        output_resolution = int(sys.argv[2])
    else:
        output_resolution = 3360  # Default output resolution

    video_to_frames(video_path, default_base_timestamp_ns, output_resolution)

if __name__ == "__main__":
    main()
