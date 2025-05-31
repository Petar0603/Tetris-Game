from tetris_module import Tetris
from oled_module import OLED
from data_conversion import convert
from interface_module import update_yellow_screen, YELLOW_SCREEN_START
import time

tetris = Tetris()
oled = OLED()
oled.set_cursor_yellow_screen()
oled.display_custom_data(YELLOW_SCREEN_START)
start_time = time.ticks_ms()
interval = 100

while True:
    
    if time.ticks_ms() - start_time > interval:
        tetris.generate_shape()
        
        x_value = tetris.read_x()
        y_value = tetris.read_y()
        sw_value = tetris.read_sw()
        
        if x_value > 2500:
            tetris.move_right()
        if x_value < 1500:
            tetris.move_left()
        if sw_value == 0:
            tetris.rotate()
        
        if y_value > 2500:
            interval = 5
        else:
            interval = 100
        
        tetris.move_down()
        overlap = tetris.overlap_check()
        bottom_hit = tetris.bottom_hit_check()
        
        if overlap:
            tetris.move_up()
            tetris.combine()
            
        if bottom_hit:
            tetris.combine()
            
        tetris.clear_completed_rows()
        
        matrix = tetris.data()
        score = tetris.return_score()
        next_shape = tetris.return_next_shape()
        
        blue_screen = convert(matrix)
        yellow_screen = update_yellow_screen(score,next_shape)
        
        oled.set_cursor_blue_screen()
        oled.display_custom_data(blue_screen)
        oled.set_cursor_yellow_screen()
        oled.display_custom_data(yellow_screen)
        
        game_over = tetris.game_over_check()
        
        if game_over:
            tetris.clear()
            oled.clear_full_display()
        
        start_time = time.ticks_ms()