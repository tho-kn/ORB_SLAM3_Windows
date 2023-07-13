import cv2
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def adjust_yaml_file(input_path, output_path, scale_factor):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    # Find and adjust the lines
    for i, line in enumerate(lines):
        trimmed_line = line.lstrip()
        if trimmed_line.startswith('Camera.fx:'):
            value = float(trimmed_line.split(':')[1].strip()) * scale_factor
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.fx: {value}\n'
        elif trimmed_line.startswith('Camera.fy:'):
            value = float(trimmed_line.split(':')[1].strip()) * scale_factor
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.fy: {value}\n'
        elif trimmed_line.startswith('Camera.cx:'):
            value = float(trimmed_line.split(':')[1].strip()) * scale_factor
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.cx: {value}\n'
        elif trimmed_line.startswith('Camera.cy:'):
            value = float(trimmed_line.split(':')[1].strip()) * scale_factor
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.cy: {value}\n'
        elif trimmed_line.startswith('Camera.width:'):
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.width: {int(3360 * scale_factor)}\n'
        elif trimmed_line.startswith('Camera.height:'):
            indent = line[:len(line) - len(trimmed_line)]
            lines[i] = f'{indent}Camera.height: {int(3360 * scale_factor)}\n'
            
    # Write to a new yaml file
    with open(output_path, 'w') as f:
        f.writelines(lines)
        
        
def create_yaml(video_path, output_resolution):
    video_name = os.path.basename(video_path).split(".")[0]
    output_dir = os.path.join("./Workset/Data", f"{video_name}_{output_resolution}")
    os.makedirs(output_dir, exist_ok=True)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print("Original Video Dimension: ", int(width), 'x', int(height))
    print("FPS: ", fps)

    # Adjust and copy the yaml file
    yaml_file_path = "./Workset/Ego.yaml"
    output_yaml_path = os.path.join(output_dir, "Ego.yaml")
    adjust_yaml_file(yaml_file_path, output_yaml_path, output_resolution/3360)

def main():
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

    create_yaml(video_path, output_resolution)

if __name__ == "__main__":
    main()
