import os , datetime, pygame, json

# function to draw about screen
def draw_about_screen(screen):
    font = pygame.font.Font(None, 36)
    screen.fill((173, 216, 230))
    text = font.render("Voltar", True, (255, 0, 0)) 
    text_rect = text.get_rect(center=(1000,600))
    screen.blit(text, text_rect)
    
# function to get a average of a list of numbers
def average(list):
    return round(sum(list)/len(list), 4)

# function to load player info from txt
def read_player_data():
    try:
        with open("player-data/dados_jogador.json", "r") as arquivo:
            data = json.load(arquivo)
            player_info = []
            for entry in data:
                player_info.append({
                    "Nome do jogador": entry["Nome do jogador"],
                    "Pontuacao": entry["Pontuacao"],
                    "Data": entry["Data"]
                })
            return player_info
    except FileNotFoundError:
        return []
    
# function to draw player info
def draw_score_screen(screen):
    font = pygame.font.Font(None, 36)
    screen.fill((173, 216, 230)) 
    player_data = read_player_data()

    title_font = pygame.font.Font(None, 36)
    title_x = [0, 210, 550]
    title_labels = ["Nome", "Pontos", "Data"]

    for i in range(len(title_labels)):
        title_text = title_font.render(title_labels[i], True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(title_x[i] + 100, 75))
        screen.blit(title_text, title_rect)

    x, y = 50, 100

    for player_info in player_data:

        text = font.render(f"{player_info['Nome do jogador']}", True, (0, 0, 0))
        screen.blit(text, (x, y))
        
        text = font.render(f"{player_info['Pontuacao']}", True, (0, 0, 0))
        screen.blit(text, (x + 250, y))
        
        text = font.render(f"{player_info['Data']}", True, (0, 0, 0))
        screen.blit(text, (x + 500, y))

        y += 50

        text = font.render("Voltar", True, (255, 0, 0)) 
        text_rect = text.get_rect(center=(1000,600))
        screen.blit(text, text_rect)

# function to draw text on screen 
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
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

# function to extract the color from img path (if target car is always green, this function is useless :p)
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