import pygame
import random
import math
import datetime
from utils.utils import *
from objects.car import Car
from states.gameState import GameState


# funtion to activate/deactivate sin function in moviment
def check_sin_move(movement):
    global amplitude, frequency
    if movement:
        y_offset = amplitude * math.sin(frequency * elapsed_time)
        car.rect.y += y_offset 


# function to check if generated car is green
def check_green(color):
    global random_car_color
    while color in random_car_color:
        random_car_color = random.choice(car_colors)

# def draw_scenario(surface, image_path, x, y):
#     surface_target = pygame.image.load(image_path).convert()
#     surface.blit(surface_target, (x,y))

def draw_scenario(surface, x, y, image_path = '', surface_target = ''):
    if surface_target == '':
        new_surface = pygame.image.load(image_path).convert()
        surface.blit(new_surface, (x,y))
    else:
        surface.blit(surface_target, (x,y))


def draw_text(surface, text, color, x, y):
    text_str = font.render(text, True, color)
    surface.blit(text_str, (x,y))
        
# function to create redline with a specific gap
def create_redlines(screen_width, screen_height, dot_spacing, gap):
    redline = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    for y in range(0, screen_height, dot_spacing):
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 + gap, y), 5)
        pygame.draw.circle(redline, (255, 0, 0), (screen_width/2 - gap, y), 5)
    
    return redline


# function to create car in the bottom or top of the screen depending on 'x' value
def create_car(color):
    global car_count
    x = random.uniform(*random.choices(spawn_intervals, weights = [0.5, 0.5], k = num_cars)[0])    
    if x <= 0:
        y = random.choice([bwd_lanes[0], bwd_lanes[1]])
        car = Car(color, x, y, False, random.randint(minSpeed, maxSpeed))
        car_count += 1

    else:
        y = random.choice([fwd_lanes[0], fwd_lanes[1]])
        car = Car(color, x, y, True, random.randint(minSpeed, maxSpeed))
        car_count += 1
        car.flip_image()

    if isColliding(car,cars) or color == 'assets/car-green.png':
        cars.append(car)
    else:
        car_count -= 1
    
pygame.init()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("comoqcaR")

# background = pygame.image.load("assets/background.png").convert()

colors = ["azul", "vermelho", "verde", "roxo", "cinza"]
# random_color = random.choice(colors)
random_color = "verde"
# expected_color_index = colors.index(random_color)

font = pygame.font.Font('freesansbold.ttf', 32)

pygame.time.set_timer(pygame.USEREVENT, 1000)

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 10000))

game_time = 90

score = 0

actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # chamar qd salvar o score, e fechar a tela do jogo

# nome_arquivo = "dados_paciente.txt"

# # Abrir o arquivo de texto no modo de escrita
# with open(nome_arquivo, 'w') as arquivo:
#     # Escrever o nome do paciente
#     arquivo.write(f"Nome do Paciente: {nome_paciente}\n")
    
#     # Escrever os scores
#     arquivo.write("Scores:\n")
#     for score in scores:
#         arquivo.write(f"{score}\n")
    
#     # Escrever a data atual
#     arquivo.write(f"Data Atual: {data_atual}\n")


car_colors = ["assets/car-blue.png", "assets/car-red.png", "assets/car-green.png", "assets/car-purple.png",  "assets/car-gray.png"]
expected_color_path = car_colors[2]
expected_color = extract_color_from_path(expected_color_path)

cars = []
num_cars = 5
car_count = 0

minSpeed = 5
maxSpeed = 10

tickrate = 60

elapsed_time = 0

spawn_intervals =[[-300, 0], [1280, 1400]] 

fwd_lanes = [200, 320]
bwd_lanes = [450, 580]

amplitude = 1
frequency = .1 
sin_moviment = True

# easy_mode_lines = [490, 790]
# medium_mode_lines = [540, 740]

hard_mode_lines = [550, 720]

easy_gap = 150
medium_gap = 100
hard_gap = 60

dot_spacing = 20

redline = create_redlines(screen_width, screen_height, dot_spacing, hard_gap)

for _ in range(num_cars):
    random_car_color = random.choice(car_colors)
    check_green("green")
    car = create_car(random_car_color)

space_pressed = False
paused = False
running = True

while running:
    clock.tick(tickrate)
    elapsed_time += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for car in cars:
                    if car.color == expected_color and (car.rect.x > hard_mode_lines[0] and car.rect.x <= hard_mode_lines[1]) and not space_pressed:  
                        print(car.rect.x)
                        space_pressed = True
                        score += 1
            elif event.key == pygame.K_CAPSLOCK:
                paused = not paused
                    
        elif event.type == SPAWN_CAR:
            if not paused: 
                create_car("assets/car-green.png") 
                pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 7000)) 
                space_pressed = False
                print('[SPAWN]', seconds_to_min(game_time))

        elif event.type == pygame.USEREVENT:
            if not paused: 
                game_time -= 1
                if game_time <= 0:
                    running = False
               
                             
    if not paused:
        draw_scenario(screen, 0, 0, 'assets/background.png')
        draw_scenario(screen, screen_width/2 + 5, 0, 'assets/background.png')
        draw_scenario(screen, 0, 0, '', redline)
        
        for car in cars:
            car.move()

            if car.rect.x > screen_width + 121 or car.rect.x < -301: # 300 is the first possible spawn in bottom AND screen_width + 120 is the last possible spawn in top
                cars.remove(car)
                car_count -= 1
                random_car_color = random.choice(car_colors)
                check_green("green")
                new_car = create_car(random_car_color) 

            if car_count < num_cars: # force to always have <num_cars> cars on the screen
                random_car_color = random.choice(car_colors)
                check_green("green")
                new_car = create_car(random_car_color)
            
            check_sin_move(sin_moviment)
            car.draw(screen)   

        draw_text(screen, "aperte 'espaço' quando o carro " + random_color + " passar pela area vermelha", 'white', 200, 20)
        draw_text(screen, seconds_to_min(game_time), 'white', 300, 90)
        draw_text(screen, str(score), 'white', 300, 120)

        pygame.display.flip()

pygame.quit()