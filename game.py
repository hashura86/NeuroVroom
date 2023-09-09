import pygame
import random
import time
import math
from utils.utils import *
from objects.car import Car

# function to create car in the bottom or top of the screen depending on 'x' value
def create_car(color):
    global car_count
    x = random.uniform(*random.choices(spawn_intervals, weights = [0.5, 0.5], k = num_cars)[0])    
    if x <= 0:
        y = random.choice([bwd_lanes[0], bwd_lanes[1]])
        car = Car(color, x, y, False, random.randint(minSpeed, maxSpeed))

    else:
        y = random.choice([fwd_lanes[0], fwd_lanes[1]])
        car = Car(color, x, y, True, random.randint(minSpeed, maxSpeed))
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

background = pygame.image.load("assets/background.png").convert()

colors = ["azul", "vermelho", "verde", "roxo", "cinza"]
# random_color = random.choice(colors)
random_color = "verde"

# expected_color_index = colors.index(random_color)
space_pressed = False

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("aperte 'espaço' quando ver o carro " + random_color + " na tela", True, "white")

pygame.time.set_timer(pygame.USEREVENT, 1000)

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 30000))
game_time = 300

score = 0

# codigo mto complexow
car_colors = ["assets/car-blue.png", "assets/car-red.png", "assets/car-green.png", "assets/car-purple.png",  "assets/car-gray.png"]
# expected_color_path = car_colors[expected_color_index]
# expected_color = extract_color_from_path(expected_color_path)

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

# spawn_gap = 50

amplitude = 1
frequency = .1 

dot_spacing = 20

redline = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
for y in range(0, screen_height, dot_spacing):
    pygame.draw.circle(redline, (255,0,0), (screen_width/2 + 60, y), 5)

redline2 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
for y in range(0, screen_height, dot_spacing):
    pygame.draw.circle(redline, (255,0,0), (screen_width/2 - 60, y), 5)

for _ in range(num_cars):
    random_car_color = random.choice(car_colors)
    while "green" in random_car_color:
        random_car_color = random.choice(car_colors)
    car = create_car(random_car_color)
    car_count += 1

paused = False

running = True

# next_green = random.randint(5,30)
# print('spawn time:',next_green)

while running:
    clock.tick(tickrate)
    elapsed_time += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                score += 1

        elif event.type == SPAWN_CAR:
            if not paused: 
                create_car("assets/car-green.png") 
                car_count += 1
                pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 7000)) 
                print('[SPAWN]', seconds_to_min(game_time))

        elif event.type == pygame.USEREVENT:
            if not paused: 
                game_time -= 1
                if game_time <= 0:
                    running = False

        # elif event.type == pygame.USEREVENT:
        #     if not paused: 
        #         game_time -= 1

        #     if (300 - game_time) % (next_green + 1) == 0 and not green_car_spawned:
        #         print('[SPAWN]', seconds_to_min(game_time))
        #         print((300 - game_time) % (next_green + 1))
        #         create_car("assets/car-green.png")
        #         green_car_spawned = True
        #         next_green = random.randint(5,7)
        #         print('spawn time:',next_green)

        #     elif (300 - game_time) % next_green != 0:
        #         green_car_spawned = False
               
                
                
    if not paused:
        
        screen.blit(background, (0, 0))
        screen.blit(background, (screen_width/2 + 5, 0))
        screen.blit(redline, (0, 0))
        time_text = font.render(seconds_to_min(game_time), True, "white")
        score_text = font.render(str(score), True, "white")
        
        for car in cars:
            car.move()

            if car.rect.x > screen_width + 121 or car.rect.x < -301: # 300 is the first possible spawn in bottom AND screen_width + 120 is the last possible spawn in top
                cars.remove(car)
                car_count -= 1
                random_car_color = random.choice(car_colors)
                while "green" in random_car_color:
                    random_car_color = random.choice(car_colors)
                new_car = create_car(random_car_color) 
                car_count += 1   

            if car_count < num_cars:
                random_car_color = random.choice(car_colors)
                while "green" in random_car_color:
                    random_car_color = random.choice(car_colors)
                new_car = create_car(random_car_color)
                car_count += 1
                
            y_offset = amplitude * math.sin(frequency * elapsed_time)
            car.rect.y += y_offset  
            
            car.draw(screen)   

        screen.blit(text, (300,20))
        screen.blit(time_text, (300,90))
        screen.blit(score_text, (300,120))

        

        # game_state.handle_events(pygame.event.get())
        # game_state.draw(screen)

        pygame.display.flip()

pygame.quit()