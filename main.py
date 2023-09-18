import pygame, pygame.mixer
import random
import math
import datetime
import json
from utils.utils import *
from objects.car import Car
from states.gameState import GameState


# def draw_countdown():
#     screen.fill((0, 0, 0))
#     for i in range (3):
#         draw_text(screen, str(i), 50, 'white', 580, 360)
#     pygame.display.flip()



# function to save player data as JSON
def save_data():

    actual_date = datetime.datetime.now()
    formated_date = actual_date.strftime("%d/%m/%Y %H:%M:%S")

    player_data = {
        "Nome do jogador": player_name,
        "Pontuacao": score,
        "Velocidade Minima": min_speed,
        "Velocidade Maxima": max_speed,
        "Data": formated_date
    }

    try:
        with open("player-data/dados_jogador.json", "r") as arquivo:
            dados_jogador = json.load(arquivo)
    except FileNotFoundError:
        dados_jogador = []
    dados_jogador.append(player_data)

    with open("player-data/dados_jogador.json", "w") as arquivo:
        json.dump(dados_jogador, arquivo, indent=4) 



# function to draw configuration screen
def draw_configuration_screen(screen):
    global active_input, input_rect, player_name, min_speed, max_speed, input_min_speed_rect, input_max_speed_rect

    screen.fill((173, 216, 230)) 

    font = pygame.font.Font(None, 36)

    draw_text(screen, 'Nome do paciente:', 25, 'black', 50, 100)
    color = (255, 0, 0) if active_input == 'name' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_rect , 2)  
    text_input = font.render(player_name, True, (0, 0, 0))
    screen.blit(text_input, (305, 105))
    
    draw_text(screen, 'Velocidade mínima dos carros:', 19, 'black', 50, 250)
    draw_text(screen, 'Velocidade máxima dos carros:', 19, 'black', 50, 300)   

    color_min = (255, 0, 0) if active_input == 'min_speed' else (0, 0, 0)
    pygame.draw.rect(screen, color_min, input_min_speed_rect, 2)
    text_input_min_speed = font.render(str(min_speed), True, (0, 0, 0))
    screen.blit(text_input_min_speed, (455, 255))

    color_max = (255, 0, 0) if active_input == 'max_speed' else (0, 0, 0)
    pygame.draw.rect(screen, color_max, input_max_speed_rect, 2)
    text_input_max_speed = font.render(str(max_speed), True, (0, 0, 0))
    screen.blit(text_input_max_speed, (455, 305))

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
        car = Car(color, x, y, False, random.randint(int(min_speed), int(max_speed)))
        car_count += 1

    else:
        y = random.choice([fwd_lanes[0], fwd_lanes[1]])
        car = Car(color, x, y, True, random.randint(int(min_speed), int(max_speed)))
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

game_time = 20 #90

score = 0

car_colors = ["assets/car-blue.png", "assets/car-red.png", "assets/car-green.png", "assets/car-purple.png",  "assets/car-gray.png"]
expected_color_path = car_colors[2]
expected_color = extract_color_from_path(expected_color_path)

cars = []
num_cars = 5
car_count = 0

min_speed = ''
max_speed = ''

tickrate = 60

elapsed_time = 0

spawn_intervals =[[-300, 0], [1280, 1400]] 

fwd_lanes = [200, 320]
bwd_lanes = [450, 580]

amplitude = 1
frequency = .1 
sin_moviment = False

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
menu_options = ['Iniciar Jogo', 'Sobre o Jogo', 'Pontuações', 'Sair do Jogo']
menu_options_gap = 70

config_selected = 0 # index of config_options
config_options = ['Iniciar Jogo', 'Voltar']
config_options_gap = 70

enter_pressed = False
space_pressed = False
paused = False
running = True

input_rect = pygame.Rect(300, 100, 300, 36)
input_min_speed_rect = pygame.Rect(450, 250, 50, 36)
input_max_speed_rect = pygame.Rect(450, 300, 50, 36)

active_input = None

player_name = ''
max_chars = 19
max_speed_chars = 2

config_ready = False

game_state = GameState.change_state(GameState.menu)

while running:

    clock.tick(tickrate)
    elapsed_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active_input = "name"
            elif input_min_speed_rect.collidepoint(event.pos):
                active_input = "min_speed"
            elif input_max_speed_rect.collidepoint(event.pos):
                active_input = "max_speed"
            else:
                active_input = None
            
        elif event.type == pygame.KEYDOWN:

            # type player name/click in the input box
            if game_state == GameState.config:
                if active_input == 'name':
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]   
                    elif event.key == pygame.K_RETURN:  # just to dont print 'enter' unicode 
                        pass
                    else:   
                        if len(player_name) < max_chars and (event.unicode.isalpha() or event.unicode == ' '):  
                            player_name += event.unicode

                # type min_speed/click in the input box
                if active_input == 'min_speed':
                    if event.key == pygame.K_BACKSPACE:
                        min_speed = min_speed[:-1]
                    elif event.key == pygame.K_RETURN:  # just to dont print 'enter' unicode 
                        pass
                    else:
                        if len(min_speed) == 0 and event.unicode.isalpha():
                            pass
                        elif len(min_speed) < max_speed_chars:
                            if not min_speed and event.unicode == '0':
                                pass
                            elif event.unicode.isdigit():
                                min_speed += event.unicode

                # type max_speed/click in the input box
                if active_input == 'max_speed':
                    if event.key == pygame.K_BACKSPACE:
                        max_speed = max_speed[:-1]
                    elif event.key == pygame.K_RETURN:  # just to dont print 'enter' unicode 
                        pass
                    else:
                        if len(max_speed) == 0 and event.unicode.isalpha():
                            pass
                        elif len(max_speed) < max_speed_chars:
                            if not max_speed and event.unicode == '0':
                                pass
                            elif event.unicode.isdigit():
                                max_speed += event.unicode

                if (max_speed and min_speed and player_name) and enter_pressed:
                    config_ready = True                    

                    
            if game_state == GameState.game:   
                
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

                # caps lock to pause game (and music too :p)
                if event.key == pygame.K_CAPSLOCK:
                    paused = not paused
                    if pygame.mixer.music.get_busy(): 
                        pygame.mixer.music.pause() 
                    else:
                        pygame.mixer.music.unpause()
            
            if game_state == GameState.score:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = GameState.change_state(GameState.menu)

            if game_state == GameState.about:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = GameState.change_state(GameState.menu)


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
                    save_data()
                    running = False


    if config_ready:
        for _ in range(num_cars):
            random_car_color = random.choice(car_colors)
            check_green("green")
            car = create_car(random_car_color)

    if game_state == GameState.menu:
        
        # draw_scenario(screen, 0, 0, 'assets/menu.png')
        screen.fill((173, 216, 230)) 

        for i, option in enumerate(menu_options):
            if i == selected_option:
                draw_text(screen, option, 32, (255, 0, 0), menu_text_x, menu_text_y + i * menu_options_gap)
            else:
                draw_text(screen, option, 32, (0, 0, 0), menu_text_x, menu_text_y + i * menu_options_gap)

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not enter_pressed:
                    enter_pressed = True
                
                    if selected_option == 0:
                        game_state = GameState.change_state(GameState.config)
                    elif selected_option == 1:
                        game_state = GameState.change_state(GameState.about)
                    elif selected_option == 2:
                        game_state = GameState.change_state(GameState.score)
                    elif selected_option == 3:
                        running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                enter_pressed = False

        pygame.display.update()

    elif game_state == GameState.config:

        draw_configuration_screen(screen)

        for i, option in enumerate(config_options):
            if i == config_selected:
                draw_text(screen, option, 32, (255, 0, 0), menu_text_x, menu_text_y + i * config_options_gap)
            else:
                draw_text(screen, option, 32, (0, 0, 0), menu_text_x, menu_text_y + i * config_options_gap)

        keys = pygame.key.get_pressed()

        up_pressed = keys[pygame.K_UP]
        down_pressed = keys[pygame.K_DOWN]

        if up_pressed:
            config_selected = (config_selected - 1) % len(config_options) if not last_up_pressed else config_selected
            last_up_pressed = True

        if down_pressed:
            config_selected = (config_selected + 1) % len(config_options) if not last_down_pressed else config_selected
            last_down_pressed = True

        if not up_pressed:
            last_up_pressed = False

        if not down_pressed:
            last_down_pressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:

                if not enter_pressed:
                    enter_pressed = True

                    if config_selected == 0:
                        game_state = GameState.change_state(GameState.game)
                    elif config_selected == 1:
                        game_state = GameState.change_state(GameState.menu)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                enter_pressed = False
        

        pygame.display.update()


    elif game_state == GameState.game:

        if not paused:

            # draw_countdown()

            play_music('sound/game-theme.mp3')

            draw_scenario(screen, 0, 0, 'assets/background.png')
            draw_scenario(screen, screen_width/2 + 5, 0, 'assets/background.png')
            draw_scenario(screen, 0, 0, '', redline)

            draw_text(screen, "aperte 'espaço' quando o carro " + random_color + " passar pela área vermelha", 32, 'white', 200, 20)
            draw_text(screen, seconds_to_min(game_time), 32, 'white', 300, 90)
            draw_text(screen, str(score), 32, 'white', 300, 120)
                
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

        draw_score_screen(screen)
            

    elif game_state == GameState.about:

        draw_about_screen(screen) 
               
                             
    pygame.display.flip()

pygame.quit()