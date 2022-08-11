import pygame
import sys
from universe import Universe
class Fileman():
    def __init__(self):
        self.def_file = open("defSave.dsave", "x") #root save file
        self.file_list = [] #list of all input files
        self.loadOrder = 0 #current index of file that is loaded
    def create_file(self,filename):
        f = open(filename, "w")
        self.file_list.__add__(f)
    def increment_load_order(self, num):
        self.loadOrder += num
    def scene_writer(self, filename):
        f = open(filename,"a")

