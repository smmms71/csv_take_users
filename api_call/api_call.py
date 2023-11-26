
import os
import json
import requests
import time
import aiohttp
import asyncio
import numpy as np
import cv2
import glob


def api_new_request(sender): 
    input_directory = f'./photos/{sender}/input/'
    output_directory = f'./photos/{sender}/output/'
    os.makedirs(output_directory, exist_ok=True)
    os.system(f"rm -rf {output_directory}*")
    
    image_paths = glob.glob(os.path.join(input_directory, '*'))
    output_paths = []
    for image_path in image_paths:
        image = cv2.imread(image_path) 
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_directory, base_name)
        cv2.imwrite(output_path, gray_image)
        output_paths.append(output_path)
    return output_paths



