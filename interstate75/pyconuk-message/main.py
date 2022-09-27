from time import ticks_ms, sleep
import math

from pimoroni import Button
import hub75
import font_8x12, font_10x14
#from font_8x12 import font, letter_width, letter_height
#from font_10x14 import font, letter_width, letter_height


FONT = font_8x12.font
LETTER_WIDTH = font_8x12.letter_width
LETTER_HEIGHT = font_8x12.letter_height

def toggle_font():
    global FONT, LETTER_WIDTH, LETTER_HEIGHT
    f_type = font_10x14 if FONT == font_8x12.font else font_8x12
    FONT = f_type.font
    LETTER_WIDTH = f_type.letter_width
    LETTER_HEIGHT = f_type.letter_height


WIDTH, HEIGHT = 32, 16

hub = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
hub.start()
hub.clear()

text = "      Welcome to the Python Hardware session!"

t_s = ticks_ms()
f_s = ticks_ms() / 1000.0

frames = 0

button_a = Button(hub75.BUTTON_A)

def scroll_text(text, y, t):
    text_length = len(text)
    x = int(t)
    letter = int((x / LETTER_WIDTH) % text_length)
    pixel = x % LETTER_WIDTH
    char = ord(text[letter])
    for s_x in range(WIDTH):
        col = FONT[char - 32][pixel]
        s_y = y + int(math.sin((t / 3.0) + s_x / 30.0) * 8)
        hub.set_color_masked(s_x, s_y, col, hub75.color_hsv(s_x / WIDTH, 1.0, 1.0))
        pixel += 1
        if pixel == LETTER_WIDTH:
            pixel = 0
            letter += 1
            if letter == text_length:
                letter = 0
            char = ord(text[letter])


while True:
    if button_a.read():
        toggle_font()
        sleep(0.25)
    hub.clear()
    t = (ticks_ms() - t_s) / 50.0
    scroll_text(text, int(HEIGHT / 2) - int(LETTER_HEIGHT / 2), t)
    hub.flip()
    frames += 1
    if frames % 60 == 0:
        f_e = ticks_ms() / 1000.0
        print(frames / (f_e - f_s))
