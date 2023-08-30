from PIL import ImageFile, Image, ImageSequence, GifImagePlugin, features
ImageFile.LOAD_TRUNCATED_IMAGES = True
GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_AFTER_DIFFERENT_PALETTE_ONLY
import random
import os
import json
import sys

with open(os.path.join(os.path.dirname(sys.executable), "config.json")) as json_data_file:
    config = json.load(json_data_file)

PIXELS_TO_SHIFT_PERCENT = config['PIXEL_TO_SHIFT_PERCENT']

def wrap_RGB(palette):
    return list(zip(*[iter(palette)] * 3))

def getClosestColorMap(palette):
    closestColorMap = {}
    
    for color in palette:
        closestColorMap[color] = getClosestColor(color, palette)
        
    return closestColorMap

def getClosestColor(color, palette):
    min_distance = None
    closest_color = None
    
    for checkedColor in palette:
        distance = getDistanceBetweenColors(color, checkedColor)
        if ((min_distance == None or distance < min_distance) and checkedColor != color):
            min_distance = distance
            closest_color = checkedColor
            
    return closest_color

def getDistanceBetweenColors(color1, color2):
    return (color1[0]-color2[0])**2 + (color1[1]-color2[1])**2 + (color1[2]-color2[2])**2

def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]

def pixelShiftGifs(input_path, fileName, newFileName):
    output_path = input_path.replace(fileName,newFileName)
    image = Image.open(input_path)
    
    # Create a palette image from the original GIF's palette
    palette_img = Image.new('P', (1, 1))
    palette_img.putpalette(image.getpalette())
                
    if image.getbands() == ('R', 'G', 'B', 'A'):
        raise Exception("INVALID GIF FORMAT : RGBA")
    
    GIF_palette = wrap_RGB(image.getpalette())
    closestColorMap = getClosestColorMap(GIF_palette)
    
    frames = [f.copy() for f in ImageSequence.Iterator(image)]    


    width, height = image.size    
    PIXELS_TO_SHIFT_PER_FRAME = int((PIXELS_TO_SHIFT_PERCENT * width * height) / 100)


    output = []
    
    for frame in frames:
        if frame.getbands() == ('R','G','B', 'A'):
            # Split the alpha channel
            r, g, b, a = frame.split()
            
            # Convert the RGB channels to P mode using the GIF's palette
            frame_rgb = Image.merge('RGB', (r, g, b))
            frame = frame_rgb.quantize(palette=palette_img)
            
        elif frame.getbands() == ('R','G','B'):
            frame = frame.convert("P") 
            
        for i in range(PIXELS_TO_SHIFT_PER_FRAME):
                                
            coord = (random.randint(0, width)-1,random.randint(0, height)-1)
            pixel_index = frame.getpixel(coord)

            frame.putpixel(coord,closestColorMap[GIF_palette[pixel_index]])
        output.append(frame)
            
                
    output[1].save(
        output_path,
        save_all = True,
        append_images = output[1:],
        loop = 0,
        duration=image.info['duration']
    )