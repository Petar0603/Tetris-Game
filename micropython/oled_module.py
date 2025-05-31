from machine import Pin, I2C

class OLED:

    OLED_I2C_ADDRESS = 0x3C
    COMMAND_REG = 0x80
    DATA_REG = 0x40
    ON_CMD = 0xAF
    NORMAL_DISPLAY_CMD = 0xA6
    MEMORY_ADDRESSING_MODE = 0x20
    VERTICAL_ADDRESSING_MODE = 0x01
    SET_COLUMN_ADDRESS = 0x21
    SET_PAGE_ADDRESS = 0x22
    CHARGE_PUMP_SETTING = 0x8D
    ENABLE_CHARGE_PUMP = 0x14

    def __init__(self, i2c_id = 0, scl_pin = 22, sda_pin = 21):
        self.i2c = I2C(i2c_id, scl = Pin(scl_pin), sda = Pin(sda_pin))
        self.write_command(self.ON_CMD)
        self.write_command(self.NORMAL_DISPLAY_CMD)
        self.write_command(self.MEMORY_ADDRESSING_MODE) 
        self.write_command(self.VERTICAL_ADDRESSING_MODE) 
        self.write_command(self.CHARGE_PUMP_SETTING) 
        self.write_command(self.ENABLE_CHARGE_PUMP)
        self.clear_full_display()

    def write_command(self, command):
        self.i2c.writeto(self.OLED_I2C_ADDRESS, bytes([self.COMMAND_REG, command]))

    def write_data(self, data):
        self.i2c.writeto(self.OLED_I2C_ADDRESS, bytes([self.DATA_REG, data]))

    def clear_full_display(self):
        self.set_cursor_blue_screen()
        for index in range(768):
            self.write_data(0x00)
        self.set_cursor_yellow_screen()
        for index in range(256):
            self.write_data(0x00)

    def set_cursor_blue_screen(self, X_start = 0, Y_start = 0, X_stop = 5, Y_stop = 127): # pages are x-axis and columns are y-axis
        self.write_command(self.SET_COLUMN_ADDRESS)
        self.write_command(Y_start) # first column to be accessed
        self.write_command(Y_stop) # last column to be accessed, restarts to 0 after
        self.write_command(self.SET_PAGE_ADDRESS)
        self.write_command(X_start) # first page to be accessed
        self.write_command(X_stop) # last page to be accessed, restarts to 0 after
        
    def set_cursor_yellow_screen(self, X_start = 6, Y_start = 0, X_stop = 7, Y_stop = 127): 
        self.write_command(self.SET_COLUMN_ADDRESS)
        self.write_command(Y_start) 
        self.write_command(Y_stop) 
        self.write_command(self.SET_PAGE_ADDRESS)
        self.write_command(X_start)
        self.write_command(X_stop) 

    def display_custom_data(self, data_list):
        for data in data_list:
            self.write_data(data)