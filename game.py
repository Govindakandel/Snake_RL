import pygame as py 


py.init()

running = True
height = 600
width = 800
# set screen title
py.display.set_caption("Snake Game")
# set screen size
screen = py.display.set_mode((width, height))

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

py.quit()

