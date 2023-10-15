import pygame, pygame.mixer
import random, math, datetime, json
from utils.utils import *
from objects.car import Car
from states.gameState import GameState

# function to save player data as JSON
def save_data():

    actual_date = datetime.datetime.now()
    formated_date = actual_date.strftime("%d/%m/%Y %H:%M:%S")

    player_data = {
        "Nome do jogador": player_name,
        "Pontuacao": score,
        "Velocidade Minima": min_speed,
        "Velocidade Maxima": max_speed,
        "Modo de Jogo": game_mode,
        "Status": patient_status,
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

    color = (255, 0, 0) if active_input == 'min_speed' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_min_speed_rect, 2)
    text_input_min_speed = font.render(str(min_speed), True, (0, 0, 0))
    screen.blit(text_input_min_speed, (410, 255))

    color = (255, 0, 0) if active_input == 'max_speed' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_max_speed_rect, 2)
    text_input_max_speed = font.render(str(max_speed), True, (0, 0, 0))
    screen.blit(text_input_max_speed, (410, 305))

    draw_text(screen, 'Modos de jogo:', 19, 'black', 50, 450)
    draw_text(screen, 'facil:', 19, 'black', 50, 550)  
    draw_text(screen, 'médio:', 19, 'black', 50, 600)  
    draw_text(screen, 'difícil:', 19, 'black', 50, 650)  

    color = (255, 0, 0) if active_input == 'easy_mode' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_easy_mode_rect, 2)
    easy_mode_rect = font.render('X', True, (0, 0, 0)) if selected_mode == 'easy' else font.render('', True, (0, 0, 0))
    screen.blit(easy_mode_rect, (215, 555))

    color = (255, 0, 0) if active_input == 'medium_mode' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_medium_mode_rect, 2)
    medium_mode_rect = font.render('X', True, (0, 0, 0)) if selected_mode == 'medium' else font.render('', True, (0, 0, 0))
    screen.blit(medium_mode_rect, (215, 605))

    color = (255, 0, 0) if active_input == 'hard_mode' else (0, 0, 0)
    pygame.draw.rect(screen, color, input_hard_mode_rect, 2)
    hard_mode_rect = font.render('X', True, (0, 0, 0)) if selected_mode == 'hard' else font.render('', True, (0, 0, 0))
    screen.blit(hard_mode_rect, (215, 655))

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
        car = Car(color, x, y, False, random.randint(int(min_speed), int(max_speed)), True)
        car_count += 1

    else:
        y = random.choice([fwd_lanes[0], fwd_lanes[1]])
        car = Car(color, x, y, True, random.randint(int(min_speed), int(max_speed)), True)
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
pygame.display.set_caption("NeuroVroom")

music_started = False

fullscreen = False

colors = ["azul", "vermelho", "verde", "roxo", "cinza"]
random_color = "verde"

pygame.time.set_timer(pygame.USEREVENT, 1000)

SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(2000, 4000))

game_time = 90

score = 0
patient_status = ''

car_colors = ["assets/car-blue.png", "assets/car-red.png", "assets/car-green.png", "assets/car-purple.png",  "assets/car-gray.png"]
expected_color_path = car_colors[2]
expected_color = extract_color_from_path(expected_color_path)

cars = []
num_cars = 5
car_count = 0
green_count = 0

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

menu_text_x = 850
menu_text_y = 350

selected_mode = ''

easy_mode_lines = [490, 790]
medium_mode_lines = [540, 740]
hard_mode_lines = [580, 700]

easy_gap = 150
medium_gap = 100
hard_gap = 60

dot_spacing = 20

game_state = ''
selected_option = 0 # index of menu_options
menu_options = ['Iniciar Jogo', 'Sobre o Jogo', 'Pontuações', 'Sair do Jogo']
menu_options_gap = 70

config_selected = 0 # index of config_options
config_options = ['Iniciar Jogo', 'Voltar']
config_options_gap = 70

bonk = pygame.mixer.Sound('sound/bonk.mp3')

enter_pressed = False
paused = False
running = True

input_rect = pygame.Rect(300, 100, 300, 36)
input_min_speed_rect = pygame.Rect(400, 250, 50, 36)
input_max_speed_rect = pygame.Rect(400, 300, 50, 36)
input_easy_mode_rect = pygame.Rect(200, 550, 50, 36)
input_medium_mode_rect = pygame.Rect(200, 600, 50, 36)
input_hard_mode_rect = pygame.Rect(200, 650, 50, 36)

active_input = None

player_name = ''
max_chars = 19
max_speed_chars = 2

game_mode = ''

# severe_limit = 1000
# moderate_limit = 500
# slight_limit = 200

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
            elif input_easy_mode_rect.collidepoint(event.pos):
                selected_mode = "easy"
                active_input = "easy_mode"
            elif input_medium_mode_rect.collidepoint(event.pos):
                selected_mode = "medium"
                active_input = "medium_mode"                
            elif input_hard_mode_rect.collidepoint(event.pos):
                selected_mode = "hard"
                active_input = "hard_mode"
            else:
                active_input = None

            # hit mouse buttons to score (or not :p) a point
            if game_state == GameState.game:
                if event.button == 1 or event.button == 3:
                    for car in cars:

                        if car.color == expected_color and ((car.rect.topright[0] >= redline_position[0] and car.rect.topright[0] <= redline_position[1]) 
                                                                or (car.rect.x >= redline_position[0] and car.rect.x <= redline_position[1])) and car.hit:
                              
                            car.hit = False
                            bonk.play()
                            if (car.rect.topright[0] >= redline_position[0] and car.rect.topright[0] <= redline_position[1]) and (car.rect.x >= redline_position[0] and car.rect.x <= redline_position[1]):
                                score += 3
                            else:
                                score += 1

                    # patient status based on score        
                    if score <= 7:
                        patient_status = 'identificacao de tempo de resposta severo'
                    elif score > 7 and score <=15:
                        patient_status = 'identificacao de tempo de resposta moderado'
                    elif score > 15 and score <=25:
                        patient_status = 'identificacao de tempo de resposta leve'
                    elif score > 25: 
                        patient_status = 'identificacao de tempo de resposta normal'

                               
        elif event.type == pygame.KEYDOWN:

            # type player name/click in the input box
            if game_state == GameState.config:
                if active_input == 'name':
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

                    # just to dont print 'enter' unicode       
                    elif event.key == pygame.K_RETURN:   
                        pass
                    else:   
                        if len(player_name) < max_chars and (event.unicode.isalpha() or event.unicode == ' '):
                            if event.unicode.isascii():  
                                player_name += event.unicode

                # type min_speed/click in the input box
                if active_input == 'min_speed':
                    if event.key == pygame.K_BACKSPACE:
                        min_speed = min_speed[:-1]

                    # just to dont print 'enter' unicode    
                    elif event.key == pygame.K_RETURN:   
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

                    # just to dont print 'enter' unicode    
                    elif event.key == pygame.K_RETURN:   
                        pass
                    else:
                        if len(max_speed) == 0 and event.unicode.isalpha():
                            pass
                        elif len(max_speed) < max_speed_chars:
                            if not max_speed and event.unicode == '0':
                                pass
                            elif event.unicode.isdigit():
                                max_speed += event.unicode
                
                if selected_mode == 'easy':
                    redline_position = easy_mode_lines
                    game_mode = 'facil'
                elif selected_mode == 'medium':
                    redline_position = medium_mode_lines
                    game_mode = 'medio'
                elif selected_mode == 'hard':
                    redline_position = hard_mode_lines
                    game_mode = 'dificil'

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
                green_count += 1
                pygame.time.set_timer(SPAWN_CAR, random.randint(5000, 7000)) 
                print('[SPAWN]',green_count, seconds_to_min(game_time))
                
                

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

        if selected_mode == "easy":
            redline_gap = easy_gap
        elif selected_mode == "medium":
            redline_gap = medium_gap
        elif selected_mode == "hard":
            redline_gap = hard_gap

        redline = create_redlines(screen_width, screen_height, dot_spacing, redline_gap)

        if not paused:

            play_music('sound/game-theme.mp3')

            draw_scenario(screen, 0, 0, 'assets/background.png')
            draw_scenario(screen, screen_width/2 + 5, 0, 'assets/background.png')
            draw_scenario(screen, 0, 0, '', redline)

            # draw_text(screen, "Clique no mouse quando o carro " + random_color + " ficar dentro da área vermelha", 32, 'white', 150, 20)
            # draw_text(screen, seconds_to_min(game_time), 32, 'white', 300, 90)
            # draw_text(screen, str(score), 32, 'white', 300, 120)
                
            for car in cars:
                car.move()
                #REMOVE THIS AFTER, JUST FOR TESTING
                if car.color == 'green':
                    if redline_gap == easy_gap:
                        pygame.draw.line(screen, (255,0,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        if car.rect.x >=490 and car.rect.x <=790:
                            pygame.draw.line(screen, (0,255,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        pygame.draw.line(screen, (255,0,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                        if car.rect.topright[0] >=490 and car.rect.topright[0] <=790:
                            pygame.draw.line(screen, (0,255,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                    elif redline_gap == medium_gap:
                        pygame.draw.line(screen, (255,0,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        if car.rect.x >=540 and car.rect.x <=740:
                            pygame.draw.line(screen, (0,255,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        pygame.draw.line(screen, (255,0,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                        if car.rect.topright[0] >=540 and car.rect.topright[0] <=740:
                            pygame.draw.line(screen, (0,255,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                    elif redline_gap == hard_gap:
                        pygame.draw.line(screen, (255,0,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        if car.rect.x >=580 and car.rect.x <=700:
                            pygame.draw.line(screen, (0,255,0), (car.rect.x, 425), (car.rect.x,425), 5)
                        pygame.draw.line(screen, (255,0,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                        if car.rect.topright[0] >=580 and car.rect.topright[0] <=700:
                            pygame.draw.line(screen, (0,255,0), (car.rect.topright[0], 425), (car.rect.topright[0],425), 5)
                    
                # 300 is the first possible spawn in bottom AND screen_width + 120 is the last possible spawn in top
                if car.rect.x > screen_width + 121 or car.rect.x < -301: 
                    cars.remove(car)
                    car_count -= 1
                    random_car_color = random.choice(car_colors)
                    check_green("green")
                    new_car = create_car(random_car_color) 
                    
                # force to always have <num_cars> cars on the screen
                if car_count < num_cars: 
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