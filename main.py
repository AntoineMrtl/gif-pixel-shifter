#!/usr/bin/env python
#pyinstaller --onefile main.py
import os
import json
from utils import pixelShiftGifs
import sys

# IMPORT CONFIGURATION

with open(os.path.join(os.path.dirname(sys.executable), "config.json")) as json_data_file:
    config = json.load(json_data_file)

MULTIPLICATION_RATE = config['MULTIPLICATION_RATE']
GIFS_FOLDER_ABSOLUTE = config['GIFS_FOLDER_ABSOLUTE']

# MAIN HANDLE FUNCTION

def handlePixelShiftFolder(folder_path):
    # Iterate through each file in the directory
    
    for filename in os.listdir(folder_path):
        gifPath = os.path.join(folder_path, filename)
        if os.path.isfile(gifPath) and filename.endswith('.gif'):
            
            print("Creating pixel shifts on : " + filename + " ...")
            
            for shifted_number in range(MULTIPLICATION_RATE):
                pixel_shifted_gif_name = filename.replace(".gif","")+"_shifted"+str(shifted_number)+".gif"
                
                # Create a pixel shifted gif
                pixelShiftGifs(gifPath, filename, pixel_shifted_gif_name)
                print("New pixel shifted gif successfully created (" + pixel_shifted_gif_name + ")")
        
    print("Successfully pixel shifted gifs for folder : " + folder_path)

if __name__ == "__main__":

    for subdir, dirs, files in os.walk(GIFS_FOLDER_ABSOLUTE):
        for dir in dirs:
            dir_path = os.path.join(GIFS_FOLDER_ABSOLUTE, dir)
            print("Folder detected at : " + dir_path)
            handlePixelShiftFolder(dir_path)