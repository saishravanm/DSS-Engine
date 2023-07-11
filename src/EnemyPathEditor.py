from genericObject import Enemy
import genericObject
import math
import pygame
from player import Player


class Enemy():
    
    def __init__(self, pos, fov, targets, speed, condition):
        self.pos = pos
        self.fov = fov
        self.targets = targets
        self.speed = speed
        self.condition = condition
        self.current_target = targets[0]
        self.rigid_body = genericObject.Enemy(self.pos, 0)

    def update(self, player_pos):
        self.pos = self.rigid_body.get_pos()
        if self.player_in_range(player_pos):
            self.follow_object(player_pos)
        else:
            self.follow_targets()
        self.rigid_body.set_pos(self.pos)


    def follow_object(self, object_pos):
        x, y = (object_pos[0] - self.pos[0],object_pos[1] - self.pos[1])
        x2, y2 = x / (x**2 + y**2)**0.5, y / (x**2 + y**2)**0.5
        displacement = (x2, y2) * self.speed
        self.pos = self.pos[0] + displacement[0], self.pos[1] + displacement[1]

    def follow_targets(self):
        if self.reached_current_target():
            self.pos = self.current_target.location
            self.change_target()
        else:
            self.follow_object(self.current_target.location)

    def reached_current_target(self):
        return ((self.current_target.location[0] - self.pos[0])**2 + (self.current_target.location[1] - self.pos[1])**2)**0.5 <= self.speed

    def change_target(self):
        if len(self.targets) > 1:
            if self.current_target == self.targets[-1]:
                if self.condition:
                    self.current_target = self.condition_function(self.current_target)
                else:
                    self.current_target = self.current_target
            else:
                self.current_target = self.targets[self.targets.index(self.current_target) + 1]
        else:
            self.current_target = self.current_target

    def player_in_range(self, player_pos):
        print(((player_pos[0] - self.pos[0])**2 + (player_pos[1] - self.pos[1])**2)**0.5)
        return ((player_pos[0] - self.pos[0])**2 + (player_pos[1] - self.pos[1])**2)**0.5 <= self.fov

########################
    def condition_function(self, target):
        #print("Testcode")
        if self.condition == 1:
            #print("1")
            return self.targets[0]
        elif self.condition == 2:
            self.targets.reverse()
            #print("2")
            return self.targets[1]
        else:
            return target

########################

    #    player = Player()
    #   enemy = Enemy([50, 50], [300, 300], 5)
    #  while True:
    #     player_pos = player.location
    #    enemy.update(player_pos)
    #   if enemy.is_within_range(player_pos):
    #      enemy.follow(player_pos)


class Target():
    def __init__(self,location):
        self.location = location