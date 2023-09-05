import pygame
from utils.utils import extract_color_from_path

class Car(pygame.sprite.Sprite):

    def __init__(self, image_path, x, y, dir, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (100, 60))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.dir = dir
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.color = extract_color_from_path(image_path)

    def move(self):

        if not self.dir: 
            self.rect.move_ip(self.speed, 0)
        else: 
            self.rect.move_ip(self.speed * -1, 0)


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    # @property
    # def x (self):
    #     return self.image.get_rect().x
    

    


    