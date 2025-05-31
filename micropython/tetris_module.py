from machine import ADC, Pin
from random import choice

ROWS = 32
COLUMNS = 12

SW_PIN = 13
X_PIN = 34
Y_PIN = 35

SHAPES = ['I', 'L', 'S', 'Z', 'J', 'O', 'T']
SHAPE_SIZE = 4

class Tetris:
    def __init__(self, x_pin = X_PIN, y_pin = Y_PIN, sw_pin = SW_PIN):
        self.static_matrix = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
        self.dynamic_matrix = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
        
        self.joystick_x = ADC(Pin(x_pin))
        self.joystick_y = ADC(Pin(y_pin))
        self.joystick_x.atten(ADC.ATTN_11DB)
        self.joystick_y.atten(ADC.ATTN_11DB)
        
        self.joystick_sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        
        self.determine_next_shape()
        self.shape_orientation = 1
        self.no_shape = True
        
        self.score = 0

    def determine_next_shape(self):
        self.next_shape = choice(SHAPES)
        
    def return_next_shape(self):
        return self.next_shape

    def return_score(self):
        return self.score
    
    def generate_shape(self):
        if self.no_shape == True:
            self.clear_dynamic()
            self.current_shape = self.next_shape
            self.shape_orientation = 1
            
            if self.current_shape == 'I':
                for row in range(4):
                    self.dynamic_matrix[row][5] = 1

            elif self.current_shape == 'L':
                for row in range(3):
                    self.dynamic_matrix[row][5] = 1
                self.dynamic_matrix[2][6] = 1

            elif self.current_shape == 'S':
                self.dynamic_matrix[0][5] = 1
                self.dynamic_matrix[1][5] = 1
                self.dynamic_matrix[1][6] = 1
                self.dynamic_matrix[2][6] = 1

            elif self.current_shape == 'Z':
                self.dynamic_matrix[0][6] = 1
                self.dynamic_matrix[1][6] = 1
                self.dynamic_matrix[1][5] = 1
                self.dynamic_matrix[2][5] = 1

            elif self.current_shape == 'J':
                for row in range(3):
                    self.dynamic_matrix[row][6] = 1
                self.dynamic_matrix[2][5] = 1

            elif self.current_shape == 'O':
                for row in range(2):
                    for column in range(5, 7):
                        self.dynamic_matrix[row][column] = 1

            elif self.current_shape == 'T':
                for row in range(3):
                    self.dynamic_matrix[row][5] = 1
                self.dynamic_matrix[1][6] = 1

            self.determine_next_shape()
            self.no_shape = False

    def read_x(self):
        return self.joystick_x.read()

    def read_y(self):
        return self.joystick_y.read()

    def read_sw(self):
        return self.joystick_sw.value()

    def move_down(self):
        for row in range(ROWS - 1, 0, -1):
            self.dynamic_matrix[row] = self.dynamic_matrix[row - 1][:]
        for column in range(COLUMNS):
            self.dynamic_matrix[0][column] = 0

    def move_up(self):
        for row in range(ROWS - 1):
            self.dynamic_matrix[row] = self.dynamic_matrix[row + 1][:]
        for column in range(COLUMNS):
            self.dynamic_matrix[ROWS - 1][column] = 0

    def move_left(self):
        moving_left = True
        for row in range(ROWS):
            if self.dynamic_matrix[row][0] == 1:
                moving_left = False
                break

        shape_left_side_coordinates = self.left_side_coordinates()
        for shape_part in shape_left_side_coordinates:
            row, column = shape_part
            if column == 0:
                moving_left = False
                break
            if self.static_matrix[row][column - 1] == 1:
                moving_left = False
                break

        if moving_left:
            for row in range(ROWS):
                for column in range(COLUMNS - 1):
                    self.dynamic_matrix[row][column] = self.dynamic_matrix[row][column + 1]
                self.dynamic_matrix[row][COLUMNS - 1] = 0

    def move_right(self):
        moving_right = True
        for row in range(ROWS):
            if self.dynamic_matrix[row][COLUMNS - 1] == 1:
                moving_right = False
                break

        shape_right_side_coordinates = self.right_side_coordinates()
        for shape_part in shape_right_side_coordinates:
            row, column = shape_part
            if column == 11:
                moving_right = False
                break
            elif self.static_matrix[row][column + 1] == 1:
                moving_right = False
                break

        if moving_right:
            for row in range(ROWS):
                for column in range(COLUMNS - 1, 0, -1):
                    self.dynamic_matrix[row][column] = self.dynamic_matrix[row][column - 1]
                self.dynamic_matrix[row][0] = 0

    def clear_dynamic(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.dynamic_matrix[row][column] = 0

    def clear_static(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.static_matrix[row][column] = 0
                
    def clear(self):
        self.clear_static()
        self.clear_dynamic()

    def stop(self):
        self.clear_dynamic()
        self.clear_static()
        self.combine()

    def combine(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.static_matrix[row][column] += self.dynamic_matrix[row][column]
        self.clear_dynamic()
        self.no_shape = True

    def data(self):
        data_matrix = [[0 for columns in range(COLUMNS)] for rows in range(ROWS)]
        for row in range(ROWS):
            for column in range(COLUMNS):
                data_matrix[row][column] = self.static_matrix[row][column] + self.dynamic_matrix[row][column]
        return data_matrix

    def overlap_check(self):
        overlap = False
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.static_matrix[row][column] + self.dynamic_matrix[row][column] > 1:
                    overlap = True
                    break
            if overlap:
                break
        return overlap
      
    def bottom_hit_check(self):
        bottom_hit = False
        for column in range(COLUMNS):
            if self.dynamic_matrix[ROWS - 1][column] == 1:
                bottom_hit = True
                break
        return bottom_hit
    
    def coordinates(self):
        coordinates_array = [[0, 0] for cell in range(SHAPE_SIZE)]
        index = 0
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.dynamic_matrix[row][column] == 1:
                    coordinates_array[index] = [row, column]
                    index += 1
        return coordinates_array

    def right_side_coordinates(self):
        right_side_coordinates_array = []
        for row in range(ROWS):
            for column in range(COLUMNS - 1,-1,-1):
                if self.dynamic_matrix[row][column] == 1:
                    right_side_coordinates_array.append([row, column])
                    break
        return right_side_coordinates_array
    
    def left_side_coordinates(self):
        left_side_coordinates_array = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.dynamic_matrix[row][column] == 1:
                    left_side_coordinates_array.append([row, column])
                    break
        return left_side_coordinates_array

    def out_of_bounds_check(self, possible_coordinates):
        out_of_bounds = False
        for cell in range(SHAPE_SIZE):
            if possible_coordinates[cell][0] > 31 or possible_coordinates[cell][0] < 0 or possible_coordinates[cell][1] > 11 or possible_coordinates[cell][1] < 0:
                out_of_bounds = True
                break
        return out_of_bounds

    def rotate(self):
        old_shape_orientation = self.shape_orientation
        self.shape_orientation += 1
        if self.shape_orientation == 5:
            self.shape_orientation = 1

        current_coordinates = self.coordinates()
        pivot = current_coordinates[0]

        possible_coordinates = [[0, 0] for cell in range(SHAPE_SIZE)]
        possible_coordinates[0] = pivot

        self.clear_dynamic()

        if self.current_shape == 'I':
            if self.shape_orientation in [1, 3]:
                for repeat in range(1,4):
                    possible_coordinates[repeat] = [pivot[0] + repeat, pivot[1]]
            else:
                for repeat in range(1,4):
                    possible_coordinates[repeat] = [pivot[0], pivot[1] + repeat]

        elif self.current_shape == 'L':
            if self.shape_orientation == 1:
                for repeat in range(1,3):
                    possible_coordinates[repeat] = [pivot[0] + repeat, pivot[1]]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1] + 1]
            elif self.shape_orientation == 2:
                for repeat in range(1,3):
                    possible_coordinates[repeat] = [pivot[0], pivot[1] + repeat]
                possible_coordinates[3] = [pivot[0] + 1, pivot[1]]
            elif self.shape_orientation == 3:
                for repeat in range(0,3):
                    possible_coordinates[repeat + 1] = [pivot[0] + repeat, pivot[1] + 1]
            else:
                for repeat in range(0,3):
                    possible_coordinates[repeat + 1] = [pivot[0] + 1, pivot[1] - 2 + repeat]

        elif self.current_shape == 'S':
            if self.shape_orientation in [1, 3]:
                for repeat in range(1,3):
                    possible_coordinates[repeat] = [pivot[0] + 1, pivot[1] - 1 + repeat]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1] + 1]
            else:
                possible_coordinates[1] = [pivot[0], pivot[1] + 1]
                for repeat in range(0,2):
                    possible_coordinates[repeat + 2] = [pivot[0] + 1, pivot[1] - 1 + repeat]
                
        elif self.current_shape == 'Z':
            if self.shape_orientation in [1, 3]:
                for repeat in range(0,2):
                   possible_coordinates[repeat + 1] = [pivot[0] + 1, pivot[1] - 1 + repeat]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1] - 1]
            else:
                for repeat in range(0,2):
                    possible_coordinates[repeat + 1] = [pivot[0] + repeat, pivot[1] + 1]
                possible_coordinates[3] = [pivot[0] + 1, pivot[1] + 2]

        elif self.current_shape == 'J':
            if self.shape_orientation == 1:
                possible_coordinates[1] = [pivot[0] + 1, pivot[1]]
                possible_coordinates[2] = [pivot[0] + 2, pivot[1] - 1]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1]]
            elif self.shape_orientation == 2:
                for repeat in range(0,3):
                    possible_coordinates[repeat + 1] = [pivot[0] + 1, pivot[1] + repeat]
            elif self.shape_orientation == 3:
                possible_coordinates[1] = [pivot[0], pivot[1] + 1]
                for repeat in range(1,3):
                    possible_coordinates[repeat + 1] = [pivot[0] + repeat, pivot[1]]
            else:
                for repeat in range(1,3):
                    possible_coordinates[repeat] = [pivot[0], pivot[1] + repeat]
                possible_coordinates[3] = [pivot[0] + 1, pivot[1] + 2]

        elif self.current_shape == 'T':
            if self.shape_orientation == 1:
                for repeat in range(0,2):
                    possible_coordinates[repeat + 1] = [pivot[0] + 1, pivot[1] + repeat]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1]]
            elif self.shape_orientation == 2:
                for repeat in range(1,3):
                    possible_coordinates[repeat] = [pivot[0], pivot[1] + repeat]
                possible_coordinates[3] = [pivot[0] + 1, pivot[1] + 1]
            elif self.shape_orientation == 3:
                for repeat in range(0,2):
                    possible_coordinates[repeat + 1] = [pivot[0] + 1, pivot[1] - 1 + repeat]
                possible_coordinates[3] = [pivot[0] + 2, pivot[1]]
            else:
                for repeat in range(1,4):
                    possible_coordinates[repeat] = [pivot[0] + 1, pivot[1] - 2 + repeat]
        else:
            for repeat in range(0,4):
                    possible_coordinates[repeat] = current_coordinates[repeat]
                    
        out_of_bounds = self.out_of_bounds_check(possible_coordinates)
        if out_of_bounds:
            for repeat in range(0,4):
                    possible_coordinates[repeat] = current_coordinates[repeat]
        
        for cell in possible_coordinates:
            row, column = cell
            self.dynamic_matrix[row][column] = 1

        overlap = self.overlap_check()
        if overlap:
            self.clear_dynamic()
            for cell in current_coordinates:
                row, column = cell
                self.dynamic_matrix[row][column] = 1
            self.shape_orientation = old_shape_orientation
            
    def row_completed(self,row):
        ones_row = True
        for column in range(COLUMNS):
            if self.static_matrix[row][column] == 0:
                ones_row = False
                break
        return ones_row
    
    def clear_row(self,row):
        for column in range(COLUMNS):
            self.static_matrix[row][column] = 0
        
        for repeat in range(row,4,-1):
            for column in range(COLUMNS):
                self.static_matrix[repeat][column] = self.static_matrix[repeat - 1][column]
        for column in range(COLUMNS):
            self.static_matrix[4][column] = 0
    
    def clear_completed_rows(self):
        completed_rows = []
        for row in range(ROWS - 1,3,-1):
            if self.row_completed(row):
                completed_rows.append(row)
        
        if len(completed_rows) == 0:
            return
        else:
            self.score += len(completed_rows)
            for repeat in range(len(completed_rows)):
                self.clear_row(completed_rows[repeat])
                
    def game_over_check(self):
        game_over = False
        for column in range(COLUMNS):
            if self.static_matrix[3][column] == 1:
                game_over == True
                break
        return game_over