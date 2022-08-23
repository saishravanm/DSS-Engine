import pygame, sys

class Sprite():
    def __init__(self,sprite,animation,clock):
        self.image = pygame.image.load("defaultSprite.png")
        self.animation = []
        self.clock = pygame.time.Clock()
        self.run = True
    def return_image(self):
        return self.image
    def change_image(self,image):
        self.image = pygame.image.load(image)
    def add_animation(self, image):
        self.animation.append(pygame.image.load(image))
    def remove_animation(self, index):
        self.animation.pop(index)
   # def draw(self,surface):
    #    while self.run:
     #       self.clock.tick(3)
      #      su

