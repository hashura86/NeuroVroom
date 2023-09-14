import os , datetime


# function to extract the color from img path
def extract_color_from_path(image_path):
    file_name = os.path.basename(image_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    parts = file_name_without_extension.split("-")
    color = parts[-1]
    return color

# function to check collision in spawn
def isColliding(new_car, existing_cars):
    for existing_car in existing_cars:
        if (new_car.rect.colliderect(existing_car.rect)):
            return False
    return True

# function to convert seconds to 'minutes:seconds'
def seconds_to_min(t:int):
    return str(datetime.timedelta(seconds=t))[2:]