# import os 
import datetime

# def extract_color_from_path(image_path):
#     file_name = os.path.basename(image_path)
#     file_name_without_extension = os.path.splitext(file_name)[0]
#     parts = file_name_without_extension.split("-")
#     color = parts[-1]
#     return color

def seconds_to_min(t:int):
    return str(datetime.timedelta(seconds=t))[2:]