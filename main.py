import pygame, pygame.mixer
import random
import math
import datetime
from utils.utils import *
from objects.car import Car
from states.gameState import GameState

def draw_configuration_screen(screen, player_name, min_speed, max_speed):
    screen.fill((255, 255, 255))  # Preencher a tela com branco ou outro fundo

    # Desenhar elementos da tela de configuração, como caixas de texto e botões
    font = pygame.font.Font(None, 36)

    # Nome do paciente
    text = font.render("Nome do Paciente:", True, (0, 0, 0))
    screen.blit(text, (50, 100))
    pygame.draw.rect(screen, (0, 0, 0), (250, 100, 300, 36), 2)  # Caixa de texto
    text_input = font.render(player_name, True, (0, 0, 0))
    screen.blit(text_input, (255, 105))

    # Velocidade dos carros
    text = font.render("Velocidade dos Carros:", True, (0, 0, 0))
    screen.blit(text, (50, 200))
    text = font.render("Min:", True, (0, 0, 0))
    screen.blit(text, (250, 200))
    text_input = font.render(str(min_speed), True, (0, 0, 0))
    screen.blit(text_input, (300, 205))
    text = font.render("Max:", True, (0, 0, 0))
    screen.blit(text, (400, 200))
    text_input = font.render(str(max_speed), True, (0, 0, 0))
    screen.blit(text_input, (450, 205))

    pygame.draw.rect(screen, (0, 0, 255), (200, 300, 200, 50))
    text = font.render("Iniciar Jogo", True, (255, 255, 255))
    screen.blit(text, (250, 310))

    pygame.draw.rect(screen, (0, 0, 255), (400, 300, 200, 50))
    text = font.render("Voltar", True, (255, 255, 255))
    screen.blit(text, (450, 310))

# function to activate/deactivate sound player
def play_music(path):
    global music_started
    if not music_started:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        music_started = True
    return music_started

# funtion to activate/deactivate sin function in moviment
def check_sin_move(movement):
    global amplitude, frequency
    if movement:
        y_offset = amplitude * math.sin(frequency * elapsed_time)
        car.rect.y += y_offset 

# function to generate other car color if appears a green one
def check_green(color):
    global random_car_color
    while color in random_car_color:
        random_car_color = random.choice(car_colors)

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
pygame.mixer.init()


clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("comoqcaR")

music_started = False


fullscreen = False

colors = ["azul", "vermelho", "verde", "roxo", "cinza"]
# random_color = random.choice(colors)
random_color = "verde"
# expected_color_index = colors.index(random_color)

pygame.time.set_timer(pygame.USEREVENT, 1000)

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 10000))

game_time = 90

score = 0

actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # chamar qd salvar o score, e fechar a tela do jogo

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
hard_mode_lines = [550, 700] # 580 - 700

easy_gap = 150
medium_gap = 100
hard_gap = 60

dot_spacing = 20

menu_text_x = 850
menu_text_y = 350

redline = create_redlines(screen_width, screen_height, dot_spacing, hard_gap)

game_state = ''
selected_option = 0 # index of menu_options
menu_options = ['iniciar jogo', 'sobre o jogo', 'pontuações', 'sair do jogo']
menu_options_gap = 70

input_active = True
space_pressed = False
paused = False
running = True

player_name = ''

for _ in range(num_cars):
    random_car_color = random.choice(car_colors)
    check_green("green")
    car = create_car(random_car_color)

game_state = GameState.change_state(GameState.menu)

while running:

    clock.tick(tickrate)
    elapsed_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                
                # disable/enable sound
                if event.key == pygame.K_m:
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)

                # enable/disable fullscreen mode
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))

                # hit space buttom to score (or not) a point
                if event.key == pygame.K_SPACE:
                    for car in cars:
                        if car.color == expected_color and (car.rect.x > hard_mode_lines[0] and car.rect.x <= hard_mode_lines[1]) and not space_pressed:  
                            print(car.rect.x)
                            space_pressed = True
                            score += 1

                # caps lock to pause game 
                if event.key == pygame.K_CAPSLOCK:
                    paused = not paused

        # elif event.type == pygame.TEXTINPUT:
        #     if input_active:
        #         player_name += event.text        

        # event to spawn cars, and the first car spawns in different time interval                
        elif event.type == SPAWN_CAR and game_state == GameState.game:
            if not paused: 
                create_car("assets/car-green.png") 
                pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 7000)) 
                space_pressed = False
                print('[SPAWN]', seconds_to_min(game_time))

        # USEREVENT to decrease game_time
        elif event.type == pygame.USEREVENT and game_state == GameState.game:
            if not paused: 
                game_time -= 1
                if game_time <= 0:
                    running = False
                    

    if game_state == GameState.menu:
        
        draw_scenario(screen, 0, 0, 'assets/menu.png')

        for i, option in enumerate(menu_options):
            if i == selected_option:
                draw_text(screen, option, (255, 0, 0), menu_text_x, menu_text_y + i * menu_options_gap)
            else:
                draw_text(screen, option, (0, 0, 0), menu_text_x, menu_text_y + i * menu_options_gap)

        keys = pygame.key.get_pressed()

        up_pressed = keys[pygame.K_UP]
        down_pressed = keys[pygame.K_DOWN]

        if up_pressed:
            selected_option = (selected_option - 1) % len(menu_options) if not last_up_pressed else selected_option
            last_up_pressed = True

        if down_pressed:
            selected_option = (selected_option + 1) % len(menu_options) if not last_down_pressed else selected_option
            last_down_pressed = True

        if not up_pressed:
            last_up_pressed = False

        if not down_pressed:
            last_down_pressed = False

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
        
            if selected_option == 0:
                game_state = GameState.change_state(GameState.game)
            elif selected_option == 1:
                game_state = GameState.change_state(GameState.about)
            elif selected_option == 2:
                game_state = GameState.change_state(GameState.score)
            elif selected_option == 3:
                running = False

        pygame.display.update()

    elif game_state == GameState.config:

        draw_configuration_screen(screen, 'jo', 3, 5)
        pygame.display.update()


    elif game_state == GameState.game:

        if not paused:

            play_music('sound/game-theme.mp3')

            draw_scenario(screen, 0, 0, 'assets/background.png')
            draw_scenario(screen, screen_width/2 + 5, 0, 'assets/background.png')
            draw_scenario(screen, 0, 0, '', redline)

            draw_text(screen, "aperte 'espaço' quando o carro " + random_color + " passar pela área vermelha", 'white', 200, 20)
            draw_text(screen, seconds_to_min(game_time), 'white', 300, 90)
            draw_text(screen, str(score), 'white', 300, 120)
                
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


        elif game_state == GameState.score:

            draw_scenario(screen, 0, 0, 'assets/menu.png')
            

        elif game_state == GameState.about:

            draw_scenario(screen, 0, 0, 'assets/menu.png')
               
                             
        pygame.display.flip()

pygame.quit()