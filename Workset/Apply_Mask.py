import cv2
import os
import argparse
import natsort
import tkinter as tk
from tkinter import filedialog
import numpy as np

# Create argument parser
parser = argparse.ArgumentParser(description='Apply mask to images.')
parser.add_argument('image_folder', type=str, nargs='?', default='', help='Folder containing images.')
parser.add_argument('mask_folder', type=str, nargs='?', default='', help='Folder containing masks.')
parser.add_argument('--no-gui', action='store_true', help='Disable the file dialog.')

args = parser.parse_args()

# Create a Tkinter root and hide it (we just want the file dialog, not a full GUI)
root = tk.Tk()
root.withdraw()

# Function to select a directory with a file dialog or exit with a message if no-gui is specified
def select_directory(directory, purpose):
    if directory == '' or not os.path.isdir(directory):
        if args.no_gui:
            print(f"{purpose} directory not found. Exiting.")
            exit(1)
        else:
            print(f"Please select the {purpose} directory.")
            directory = filedialog.askdirectory()
            print(f"Selected {purpose} directory: {directory}")
    return directory

# Use the select_directory function to set the image and mask directories
args.image_folder = select_directory(args.image_folder, "image")
args.mask_folder = select_directory(args.mask_folder, "mask")

# Get the sorted list of image and mask files
image_files = natsort.natsorted(os.listdir(args.image_folder))
mask_files = natsort.natsorted(os.listdir(args.mask_folder))

# Check if both directories have same number of files
if len(image_files) != len(mask_files):
    print("Number of image and mask files do not match!")
    mask_files = ["" for _ in image_files]

# Create an output directory for masked images if it does not exist
output_folder = os.path.join(args.image_folder, "..", "masked_images")
os.makedirs(output_folder, exist_ok=True)

# Apply each mask to corresponding image
for image_file, mask_file in zip(image_files, mask_files):
    # Load image and mask
    image = cv2.imread(os.path.join(args.image_folder, image_file))
    
    if mask_file != "":
        mask = cv2.imread(os.path.join(args.mask_folder, mask_file), cv2.IMREAD_GRAYSCALE)
        
        # Resize mask to fit image
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

        # Mask out area where mask is 255
        image[mask == 255] = 0

    # Create a circular mask
    circular_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    circle_radius = int(0.45 * image.shape[1])  # 0.9/2 as we need radius from diameter
    cv2.circle(circular_mask, (image.shape[1]//2, image.shape[0]//2), circle_radius, (255), thickness=-1)

    # Apply circular mask to image
    image[circular_mask == 0] = 0

    # Save the masked image
    cv2.imwrite(os.path.join(output_folder, image_file), image)

print(f"Masked images saved in: {output_folder}")
