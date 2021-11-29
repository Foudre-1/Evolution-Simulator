import pygame
import math #libraries imports
import numpy as np
import random
from .constants import GREEN, BLUE1, BLUE2, BLUE3, BLUE4, GREY1, GREY2, RED1, RED2, RED3, RED4 #files imports

class Grid: #Main grid class
    def __init__(self, size):
        self.__size = size #the size of a cell (1 small, 1000 very large)
        self.__columns = math.floor(pygame.display.get_window_size()[0]/size) #determine the number of rows and columns using the screen resolution
        self.__rows = math.floor(pygame.display.get_window_size()[1]/size)
        """self.grid = np.array([[0 if rows%2 == 0 else 1 for rows in range(self.__columns)] #create a checkboard pattern [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
             if columns%2 == 0 else
             [0 if rows%2 == 1 else 1 for rows in range(self.__columns)]
             for columns in range(self.__rows)])"""
        self.grid = np.array([[0 for i in range(self.__columns)] for i in range(self.__rows)]) #old grid generation
        self.__oldgrid = np.copy(self.grid)
        self.__cell_list = []
        self.__random_direction = ["nothing"] #["right", "left", "up", "down"] + ["nothing" for i in range(6)]
        
    def get(self): #getter
        return f"{self.__size=}\n {self.__rows=}\n {self.__columns=}\n {self.grid=}\n {self.__random_direction=}\n {set([cell.name for cell in self.__cell_list])}"
        
    def get_rows_columns(self):
        return self.__columns, self.__rows
        
    def set(self, column, row, value): #setter
        self.grid[column, row] = value
        
    def create_cell(self, name):
        #if name == "blue":
        #    self.__cell_list.append(Cell(self.__rows//2, self.__columns//2, name))
        #else:
        #    self.__cell_list.append(Cell(random.randint(0, self.__rows-2), random.randint(0, self.__columns-2), name))
        self.__cell_list.append(Cell(0, 0, name))
        #self.__cell_list = self.__cell_list[::-1]
        
    def get_cell_list(self):
        return self.__cell_list
    
    def update_cell(self):
        for current in self.__cell_list:
            for row in range(current.pattern.shape[0]): #current.pattern.shape[0] is the lines
                for column in range(current.pattern.shape[1]): #current.pattern.shape[1] is the columns
                    #print(f"row -> {row + current.origin[0]}\
                    #    \ncolumn -> {column + current.origin[1]}\
                    #    \nvalue -> {current.pattern[row, column]}\
                    #    \n{self.__rows = }\
                    #    \n{self.__columns = }\n")
                    if current.origin[0] + current.pattern.shape[0] -1 < self.__rows and current.origin[1] + current.pattern.shape[1] -1 < self.__columns:
                        self.set(row + current.origin[0], column + current.origin[1], current.pattern[row, column])
        #print(self.grid)
    
    def old_move_cell(self, direction):
        for current in self.__cell_list:
            if current.name == "blue":
                if direction == "left":
                    if current.origin[1] != 0:
                        print([self.grid[current.origin[0]+i, current.origin[1]-1] for i in range(current.pattern.shape[0])])
                        print(all([self.grid[current.origin[0]+i, current.origin[1]-1] for i in range(current.pattern.shape[0])]) == 0)
                        if all([self.grid[current.origin[0]+i, current.origin[1]-1] for i in range(current.pattern.shape[0])]) == 0:
                            current.move_origin(0, -1)
                            #removing right cells
                            for row in range(current.pattern.shape[0]):
                                self.set(current.origin[0]+row, current.origin[1]+current.pattern.shape[1], 0)
                elif direction == "right":
                    if current.origin[1] < self.__columns-current.pattern.shape[1]:
                        if all([self.grid[current.origin[0]+i, current.origin[1]-current.pattern.shape[0]] for i in range(current.pattern.shape[0])]) == 0:
                            current.move_origin(0, 1)
                            #removing left cells
                            for row in range(current.pattern.shape[0]):
                                self.set(current.origin[0] + row, current.origin[1]-1, 0)
                elif direction == "up":
                    if current.origin[0] != 0:
                        if all([self.grid[current.origin[0]-1, current.origin[1]+i] for i in range(current.pattern.shape[0])]) == 0:
                            current.move_origin(-1, 0)
                            #Removing bottom cells
                            for column in range(current.pattern.shape[1]):
                                self.set(current.origin[0]+current.pattern.shape[0], current.origin[1]+column, 0)
                elif direction == "down":
                    if current.origin[0] < self.__rows-current.pattern.shape[0]:
                        if all([self.grid[current.origin[0]+current.pattern.shape[0], current.origin[1]+i] for i in range(current.pattern.shape[1])]) == 0:
                            current.move_origin(1, 0)
                            #Removing top cells
                            for column in range(current.pattern.shape[1]):
                                self.set(current.origin[0]-1, current.origin[1]+column, 0)
    
    def move_cell(self):
        for current in self.__cell_list:
            choice = random.choice(self.__random_direction)
            if choice == "nothing":
                pass
            if choice == "left":
                if current.origin[1] != 0:
                    if all([self.grid[current.origin[0]+i, current.origin[1]-1] for i in range(current.pattern.shape[0])]) == 0:
                        current.move_origin(0, -1)
                        #removing right cells
                        for row in range(current.pattern.shape[0]):
                            self.set(current.origin[0]+row, current.origin[1]+current.pattern.shape[1], 0)
            elif choice == "right":
                if current.origin[1] < self.__columns-current.pattern.shape[1]:
                    if all([self.grid[current.origin[0]+i, current.origin[1]-current.pattern.shape[0]] for i in range(current.pattern.shape[0])]) == 0:
                        current.move_origin(0, 1)
                        #removing left cells
                        for row in range(current.pattern.shape[0]):
                            self.set(current.origin[0] + row, current.origin[1]-1, 0)
            elif choice == "up":
                if current.origin[0] != 0:
                    if all([self.grid[current.origin[0]-1, current.origin[1]+i] for i in range(current.pattern.shape[0])]) == 0:
                        current.move_origin(-1, 0)
                        #Removing bottom cells
                        for column in range(current.pattern.shape[1]):
                            self.set(current.origin[0]+current.pattern.shape[0], current.origin[1]+column, 0)
            elif choice == "down":
                if current.origin[0] < self.__rows-current.pattern.shape[0]:
                    if all([self.grid[current.origin[0]+current.pattern.shape[0], current.origin[1]+i] for i in range(current.pattern.shape[1])]) == 0:
                        current.move_origin(1, 0)
                        #Removing top cells
                        for column in range(current.pattern.shape[1]):
                            self.set(current.origin[0]-1, current.origin[1]+column, 0)
       
    def old_draw_cells(self, window): #Basically convert numbers to colored squares of the right size
        for col in range(self.grid.shape[0]):
            #print((self.__oldgrid[col] == self.grid[col]).all())
            for row in range(self.grid.shape[1]):
                #pygame.draw.rect(WINDOW, COLOR, (XPOS, YPOS, XSIZE, YSIZE), width=BORDERSIZE)
                #pygame.draw.rect(window, GREY, (row*self.__size, col*self.__size, self.__size, self.__size))
                if self.grid[col, row] == -1:
                    pygame.draw.rect(window, GREY1, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 0:
                    pygame.draw.rect(window, GREY2, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 1:
                    pygame.draw.rect(window, RED1, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 2:
                    pygame.draw.rect(window, RED2, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 3:
                    pygame.draw.rect(window, RED3, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 4:
                    pygame.draw.rect(window, RED4, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 5:
                    pygame.draw.rect(window, BLUE1, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 6:
                    pygame.draw.rect(window, BLUE2, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 7:
                    pygame.draw.rect(window, BLUE3, (row*self.__size, col*self.__size, self.__size, self.__size))
                elif self.grid[col, row] == 8:
                    pygame.draw.rect(window, BLUE4, (row*self.__size, col*self.__size, self.__size, self.__size))
        return window
    
    def draw_cells(self, window): #Basically convert numbers to colored squares of the right size
        for col in range(self.grid.shape[0]):
            #print((self.__oldgrid[col] == self.grid[col]).all())
            if (self.__oldgrid[col] == self.grid[col]).all() == False:
                for row in range(self.grid.shape[1]):
                    #pygame.draw.rect(WINDOW, COLOR, (XPOS, YPOS, XSIZE, YSIZE), width=BORDERSIZE)
                    #pygame.draw.rect(window, GREY, (row*self.__size, col*self.__size, self.__size, self.__size))
                    if self.grid[col, row] == -1:
                        pygame.draw.rect(window, GREY1, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 0:
                        pygame.draw.rect(window, GREY1, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 1:
                        pygame.draw.rect(window, RED1, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 2:
                        pygame.draw.rect(window, RED2, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 3:
                        pygame.draw.rect(window, RED3, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 4:
                        pygame.draw.rect(window, RED4, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 5:
                        pygame.draw.rect(window, BLUE1, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 6:
                        pygame.draw.rect(window, BLUE2, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 7:
                        pygame.draw.rect(window, BLUE3, (row*self.__size, col*self.__size, self.__size, self.__size))
                    elif self.grid[col, row] == 8:
                        pygame.draw.rect(window, BLUE4, (row*self.__size, col*self.__size, self.__size, self.__size))
            else:
                self.grid[col] = np.copy(self.__oldgrid[col])
        self.__oldgrid = np.copy(self.grid)
        #dict_draw = {-1: pygame.draw.rect(window, GREY1, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                0: pygame.draw.rect(window, GREY1, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                1: pygame.draw.rect(window, RED1, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                2: pygame.draw.rect(window, RED2, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                3: pygame.draw.rect(window, RED3, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                4: pygame.draw.rect(window, RED4, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                5: pygame.draw.rect(window, BLUE1, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                6: pygame.draw.rect(window, BLUE2, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                7: pygame.draw.rect(window, BLUE3, (row*self.__size, col*self.__size, self.__size, self.__size)),
        #                8: pygame.draw.rect(window, BLUE4, (row*self.__size, col*self.__size, self.__size, self.__size))}
        return window
    
class Cell():
    def __init__(self, row, column, name="test", pattern=np.array([[-1, -1], [-1, -1]])):
        self.origin = (row, column)
        self.pattern = pattern
        self.name = name
        if name == "red":
            self.pattern = np.array([[1, 2], [3, 4]])
        elif name == "blue":
            self.pattern = np.array([[5, 6, 1], [7, 8, 2]])
        #elif name == "blue":
        #    self.pattern = np.array([[5, 6], [7, 8]])
    
    def get_pattern(self):
        return self.pattern
    
    def move_origin(self, column, row):
        self.origin = (self.origin[0] + column, self.origin[1] + row)