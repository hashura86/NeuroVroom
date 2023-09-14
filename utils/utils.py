import os , datetime, pygame


# function to draw text on screen 
def draw_text(surface, text, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_str = font.render(text, True, color)
    surface.blit(text_str, (x,y))

# function to draw scenario by img path or other surface (like redline)
def draw_scenario(surface, x, y, image_path = '', surface_target = ''):
    if surface_target == '':
        new_surface = pygame.image.load(image_path).convert()
        surface.blit(new_surface, (x,y))
    else:
        surface.blit(surface_target, (x,y))

# function to create redline with a specific gap
def create_redlines(screen_width, screen_height, dot_spacing, gap):
    redline = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    for y in range(0, screen_height, dot_spacing):
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 + gap, y), 5)
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 - gap, y), 5)
    
    return redline
# function to create redline with a specific gap
def create_redlines(screen_width, screen_height, dot_spacing, gap):
    redline = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    for y in range(0, screen_height, dot_spacing):
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 + gap, y), 5)
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 - gap, y), 5)
    
    return redline
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