import pygame
import sys
import player
class Fileman():
    def __init__(self):
        self.def_file = open("defSave.dsave", "r") #root save file
        self.file_list = [] #list of all input files
        self.loadOrder = 0 #current index of file that is loaded
    def create_file(self,filename):
        f = open(filename, "w")
        self.file_list.__add__(f)
    def increment_load_order(self, num):
        self.loadOrder += num
    def scene_writer(self, filename,searchtext,replacetext):

        with open(filename,'r') as file:
            data = file.read()

            data = data.replace(searchtext,replacetext)

        with open(filename, 'w') as file:
            file.write(data)



