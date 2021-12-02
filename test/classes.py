import pygame
import math #libraries imports
import numpy as np
import random
from .constants import FOOD, EATER, BONE, PRODUCER, BLUE1, BLUE2, BLUE3, BLUE4, GREY1, GREY2, RED1, RED2, RED3, RED4 #files imports

class Grid: #Main grid class
    def __init__(self, size):
        self.size = size #the size of a cell (1 small, 1000 very large)
        self.columns = math.floor(pygame.display.get_window_size()[0]/size) #determine the number of rows and columns using the screen resolution
        self.rows = math.floor(pygame.display.get_window_size()[1]/size)
        """self.grid = np.array([[0 if rows%2 == 0 else 1 for rows in range(self.columns)] #create a checkboard pattern [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
             if columns%2 == 0 else
             [0 if rows%2 == 1 else 1 for rows in range(self.columns)]
             for columns in range(self.rows)])"""
        self.grid = np.array([[0 for i in range(self.columns)] for i in range(self.rows)]) #old grid generation
        self.oldgrid = np.copy(self.grid)
        self.cell_list = []
        self.food_list = []
        self.random_direction = ["nothing"] #["right", "left", "up", "down"] + ["nothing" for i in range(6)]
        self.random_food = ["left", "up", "right", "down"] + ["nothing" for i in range(750)]
        
    def get(self): #getter
        return f"{self.size=}\n {self.rows=}\n {self.columns=}\n {self.grid=}\n {self.random_direction=}\n {set([cell.name for cell in self.cell_list])}"
        
    def get_rows_columns(self):
        return self.columns, self.rows
        
    def set(self, column, row, value): #setter
        self.grid[column][row] = value
        
    def create_cell(self, name="starter"):
        if name == "test":
            self.cell_list.append(Cell(random.randint(0, self.rows), random.randint(0, self.columns), name))
        else:
            #self.cell_list.append(Cell(-2, 0, name))
            self.cell_list.append(Cell(self.rows//2, self.columns//2, name))
    
    def create_food(self, row, column):
        self.food_list.append(Food(row, column))
     
    def get_cell_list(self):
        return self.cell_list
    
    def reverse_cell_list(self):
        print(self.cell_list)
        self.cell_list = self.cell_list[::-1]
        print(self.cell_list)
    
    def update_cell(self):
        for current in self.food_list:
            self.set(current.row, current.column, 1)
            
        for current in self.cell_list:
            for row in range(current.pattern.shape[0]): #current.pattern.shape[0] is the lines
                for column in range(current.pattern.shape[1]): #current.pattern.shape[1] is the columns
                    #print(f"row -> {row + current.origin[0]}\
                    #    \ncolumn -> {column + current.origin[1]}\
                    #    \nvalue -> {current.pattern[row, column]}\
                    #    \n{self.rows = }\
                    #    \n{self.columns = }\n")
                    if current.origin[0] + current.pattern.shape[0] -1 < self.rows and current.origin[1] + current.pattern.shape[1] -1 < self.columns:
                        #self.set(row + current.origin[0], column + current.origin[1], current.pattern[row][column])
                        if current.pattern[row][column] != -1:
                            self.set(row + current.origin[0], column + current.origin[1], current.pattern[row][column])
                        else:
                            pass
        
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                if self.grid[row][col] == 3:
                    r = random.choice(self.random_food)
                    if r == "left":
                        #print("GAUCHE")
                        if col > 0:
                            if self.grid[row][col-1] == 0:
                                self.create_food(row, col-1)
                    if r == "up":
                        #print("HAUT")
                        if row > 0:
                            if self.grid[row-1][col] == 0:
                                self.create_food(row-1, col)
                    if r == "right":
                        #print("DROITE")
                        if col < self.columns-1:
                            if self.grid[row][col+1] == 0:
                                self.create_food(row, col+1)
                    if r == "down":
                        #print("BAS")
                        if row < self.rows-1:
                            if self.grid[row+1][col] == 0:
                                self.create_food(row+1, col)
    
    def old_move_cell(self, direction):
        for current in self.cell_list:
            if current.name == "starter":
                if direction == "left":
                    if current.origin[1] != 0:
                        #print([current.boundaries["left"][i]-1 for i in range(current.pattern.shape[0])])
                        #print([self.grid[current.origin[0]+i, current.origin[1]+current.boundaries["left"][i]-1] for i in range(current.pattern.shape[0])])
                        #print([self.grid[current.origin[0]+i, current.origin[1]+current.boundaries["left"][i]-1] in (0, -1) for i in range(current.pattern.shape[0])])
                        #print(all([self.grid[current.origin[0]+i, current.origin[1]+current.boundaries["left"][i]-1] in (0, -1) for i in range(current.pattern.shape[0])]))
                        if all([self.grid[current.origin[0]+i, current.origin[1]+current.boundaries["left"][i]-1] in (0, -1) for i in range(current.pattern.shape[0])]):
                            current.move_origin(0, -1)
                            for row in range(current.pattern.shape[0]):
                                for column in range(current.pattern.shape[1]):
                                    if current.pattern[row][column] == -1:
                                        self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                    self.set(current.origin[0]+row, current.origin[1]+current.pattern.shape[1]-current.boundaries["right"][row], 0)
                elif direction == "right":
                    print(current.pattern.shape[1])
                    if current.origin[1] < self.columns-current.pattern.shape[1]:
                        if all([self.grid[current.origin[0]+i, current.origin[1]+current.pattern.shape[1]-current.boundaries["right"][i]] in (0, -1) for i in range(current.pattern.shape[0])]):
                            current.move_origin(0, 1)
                            for row in range(current.pattern.shape[0]):
                                for column in range(current.pattern.shape[1]):
                                    if current.pattern[row][column] == -1:
                                        self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                    self.set(current.origin[0]+row, current.origin[1]+current.boundaries["left"][row]-1, 0)
                            #for row in range(current.pattern.shape[0]):
                            #    self.set(current.origin[0] + row, current.origin[1]+current.boundaries["left"][row]-1, 0)
                            #    #self.set(current.origin[0] + row, current.origin[1]-1, 0)
                            #    #self.set(current.origin[0] + row, current.origin[1]-current.boundaries["right"][row], 5)
                elif direction == "up":
                    if current.origin[0] != 0:
                        if all([self.grid[current.origin[0]+current.boundaries["up"][i]-1, current.origin[1]+i] in (0, -1) for i in range(current.pattern.shape[1])]):
                            current.move_origin(-1, 0)
                            for row in range(current.pattern.shape[0]):
                                for column in range(current.pattern.shape[1]):
                                    if current.pattern[row][column] == -1:
                                        self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                    self.set(current.origin[0]+current.pattern.shape[0]-current.boundaries["down"][column], current.origin[1]+column, 0)
                elif direction == "down":
                    if current.origin[0] < self.rows-current.pattern.shape[0]:
                        if all([self.grid[current.origin[0]+current.pattern.shape[0]-current.boundaries["down"][i], current.origin[1]+i] in (0, -1) for i in range(current.pattern.shape[1])]):
                            current.move_origin(1, 0)
                            for row in range(current.pattern.shape[0]):
                                for column in range(current.pattern.shape[1]):
                                    if current.pattern[row][column] == -1:
                                        self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                    self.set(current.origin[0]+current.boundaries["up"][column]-1, current.origin[1]+column, 0)
                #print(self.grid)
    
    def move_cell(self):
        for current in self.cell_list:
            choice = random.choice(self.random_direction)
            if choice == "nothing":
                pass
            if choice == "left":
                if current.origin[1] != 0:
                        if all([self.grid[current.origin[0]+i, current.origin[1]+current.boundaries["left"][i]-1] in (0, -1) for i in range(current.pattern.shape[0])]):
                            current.move_origin(0, -1)
                            for row in range(current.pattern.shape[0]):
                                for column in range(current.pattern.shape[1]):
                                    if current.pattern[row][column] == -1:
                                        self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                    self.set(current.origin[0]+row, current.origin[1]+current.pattern.shape[1]-current.boundaries["right"][row], 0)
            elif choice == "right":
                if current.origin[1] < self.columns-current.pattern.shape[1]:
                    print(current.origin)
                    if all([self.grid[current.origin[0]+i, current.origin[1]+current.pattern.shape[1]-current.boundaries["right"][i]] in (0, -1) for i in range(current.pattern.shape[0])]):
                        current.move_origin(0, 1)
                        for row in range(current.pattern.shape[0]):
                            for column in range(current.pattern.shape[1]):
                                if current.pattern[row][column] == -1:
                                    self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                self.set(current.origin[0]+row, current.origin[1]+current.boundaries["left"][row]-1, 0)
            elif choice == "up":
                if current.origin[0] != 0:
                    if all([self.grid[current.origin[0]+current.boundaries["up"][i]-1, current.origin[1]+i] in (0, -1) for i in range(current.pattern.shape[1])]):
                        current.move_origin(-1, 0)
                        for row in range(current.pattern.shape[0]):
                            for column in range(current.pattern.shape[1]):
                                if current.pattern[row][column] == -1:
                                    self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                self.set(current.origin[0]+current.pattern.shape[0]-current.boundaries["down"][column], current.origin[1]+column, 0)
            elif choice == "down":
                if current.origin[0] < self.rows-current.pattern.shape[0]:
                    if all([self.grid[current.origin[0]+current.pattern.shape[0]-current.boundaries["down"][i], current.origin[1]+i] in (0, -1) for i in range(current.pattern.shape[1])]):
                        current.move_origin(1, 0)
                        for row in range(current.pattern.shape[0]):
                            for column in range(current.pattern.shape[1]):
                                if current.pattern[row][column] == -1:
                                    self.set(current.origin[0]+row, current.origin[1]+column, 0)
                                self.set(current.origin[0]+current.boundaries["up"][column]-1, current.origin[1]+column, 0)
       
    def old_draw_cells(self, window): #Basically convert numbers to colored squares of the right size
        for col in range(self.grid.shape[0]):
            #print((self.oldgrid[col] == self.grid[col]).all())
            for row in range(self.grid.shape[1]):
                #pygame.draw.rect(WINDOW, COLOR, (XPOS, YPOS, XSIZE, YSIZE), width=BORDERSIZE)
                #pygame.draw.rect(window, GREY, (row*self.size, col*self.size, self.size, self.size))
                if self.grid[col, row] == 0:
                    pygame.draw.rect(window, GREY2, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 1:
                    pygame.draw.rect(window, RED1, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 2:
                    pygame.draw.rect(window, RED2, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 3:
                    pygame.draw.rect(window, RED3, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 4:
                    pygame.draw.rect(window, RED4, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 5:
                    pygame.draw.rect(window, BLUE1, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 6:
                    pygame.draw.rect(window, BLUE2, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 7:
                    pygame.draw.rect(window, BLUE3, (row*self.size, col*self.size, self.size, self.size))
                elif self.grid[col, row] == 8:
                    pygame.draw.rect(window, BLUE4, (row*self.size, col*self.size, self.size, self.size))
        return window
    
    def draw_cells(self, window): #Basically convert numbers to colored squares of the right size
        for col in range(self.grid.shape[0]):
            #print((self.oldgrid[col] == self.grid[col]).all())
            #pygame.draw.rect(WINDOW, COLOR, (XPOS, YPOS, XSIZE, YSIZE), width=BORDERSIZE)
            #pygame.draw.rect(window, GREY, (row*self.size, col*self.size, self.size, self.size))
            if (self.oldgrid[col] == self.grid[col]).all() == False:
                for row in range(self.grid.shape[1]):
                    if self.grid[col, row] == -1:
                        pygame.draw.rect(window, GREY1, (row*self.size, col*self.size, self.size, self.size))
                    elif self.grid[col, row] == 1:
                        pygame.draw.rect(window, FOOD, (row*self.size, col*self.size, self.size, self.size))
                    elif self.grid[col, row] == 0:
                        pygame.draw.rect(window, GREY1, (row*self.size, col*self.size, self.size, self.size))
                    elif self.grid[col, row] == 2:
                        pygame.draw.rect(window, BONE, (row*self.size, col*self.size, self.size, self.size))
                    elif self.grid[col, row] == 3:
                        pygame.draw.rect(window, PRODUCER, (row*self.size, col*self.size, self.size, self.size))
                    elif self.grid[col, row] == 4:
                        pygame.draw.rect(window, EATER, (row*self.size, col*self.size, self.size, self.size))
            else:
                self.grid[col] = np.copy(self.oldgrid[col])
        self.oldgrid = np.copy(self.grid)
        return window
 
class Cell():
    def __init__(self, row, column, name="starter", pattern=np.array([[3, 2, 3], [-1, 4, -1]]), boundaries={"left": [0, 1], "up": [0, 0, 0], "right": [0, 1], "down": [1, 0, 1]}):
        self.origin = (row, column)
        self.pattern = pattern
        self.name = name
        self.boundaries = boundaries
        #if name == "red":
        #    self.pattern = np.array([[-1, 1, -1],
        #                             [1, 9, 1],
        #                             [-1, 1, -1],
        #                             [-1, -1, -1],
        #                             [1, 1, 1]])
        #if name == "blue":
        #    self.pattern = np.array([[5, 6, 7]])
        #if name == "red":
        #    self.boundaries = {"left": [1, 0, 1, 3, 0], "up": [1, 0, 1], "right": [1, 0, 1, 3, 0], "down": [1, 1, 1]}
        #elif name == "blue":
        #    self.boundaries = {"left": [0], "up": [0, 0, 0], "right": [0], "down": [0, 0, 0]}
        #elif name == "blue":
        #    self.pattern = np.array([[5, 6], [7, 8]])
    
    def get_pattern(self):
        return self.pattern
    
    def move_origin(self, column, row):
        self.origin = (self.origin[0] + column, self.origin[1] + row)
        
class Food():
    def __init__(self, row, column):
        self.row = row
        self.column = column