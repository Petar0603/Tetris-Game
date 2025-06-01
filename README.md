# Tetris-Game
Realized with ESP32, SSD1306 OLED and a joystick.

---
## About

Code for the game is written in Python for ThonnyIDE.
Code consists of the following modules:
- 'interface_module' with GUI hex data for all of the
numbers, letters and tetris shapes presented on the OLED.
- 'data_conversion' used to convert the data matrix (32x12)
to data for OLED display (128x48) (one pixel of data is 4x4
pixels on the OLED)
- 'oled_module' used to control the 128x64 SSD1306 OLED, it
includes functions to write in the command register and
data register of OLED, clear the screen, turn on sequence etc.
- 'tetris_module' consists of the game logic, generating random shapes,
their rotation etc.
- 'run' is the code to be run on the ESP32 board.

---
## Photos
Whole circuit on a breadboard 
<div align="center"><img src="/realization/full circuit.jpg"></div>
OLED Before clearing a row
<div align="center"><img src="/realization/no rows cleared.jpg"></div>
OLED After clearing a row
<div align="center"><img src="/realization/row cleared.jpg"></div>
