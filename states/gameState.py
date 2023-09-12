import pygame

class GameState:
    def __init__(self):
        self.state = "menu" 

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self.state = "game"  
                elif self.state == "game":
                    self.state = "score"  
                elif self.state == "score":
                    self.state = "menu" 
                elif self.state == "score":
                    self.state = "menu" 
                elif self.state == "score":
                    self.state = "menu" 

    def draw(self, screen):
        screen.fill((255,255,255))
        if self.state == "start":
            background = pygame.transform.scale2x(pygame.image.load("assets/bg.jpg")).convert()
            font = pygame.font.Font(None, 36)
            text = font.render("Pressione uma tecla para iniciar", True, (0, 0, 0))
            screen.blit(background, (0, 0))
            screen.blit(text, (250, 250))
        elif self.state == "game":
            font = pygame.font.Font(None, 36)
        elif self.state == "score":
            font = pygame.font.Font(None, 36)
        elif self.state == "score":
            font = pygame.font.Font(None, 36)
        elif self.state == "score":
            font = pygame.font.Font(None, 36)
            