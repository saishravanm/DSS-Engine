import pygame
import sys
import player
class Fileman():
    def __init__(self):
        self.def_file = open("defSave.dsave", "r") #root save file
        self.file_list = [] #list of all input files
        self.loadOrder = 0 #current index of file that is loaded
        self.savepoint = (0,0)
        self.savepoint_reached = False
    def create_file(self,filename):
        f = open(filename, "w")
        self.file_list.append(f)
    def increment_load_order(self, num):
        self.loadOrder += num
    def scene_writer(self, filename,searchtext,replacetext):

        with open(filename,'r') as file:
            data = file.read()

            data = data.replace(searchtext,replacetext)

        with open(filename, 'w') as file:
            file.write(data)

    def write_save_point(self, location):
        self.savepoint = location

    def check_save_point(self, player):
        if(player.location==self.savepoint):
            self.savepoint_reached = True

    def clear_save(self, filename):
        with open(filename, "r+") as f:
            f.truncate(0)
