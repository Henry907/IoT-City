import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['XDG_RUNTIME_DIR'] = '/run/user/' + str(os.getuid())
import pygame
import time
from sys import exit
import subprocess

try:
    if os.getuid() == 0:
        # gets ID of Display, used to make it possible to run this through SSH
        subprocess.run('export DISPLAY=:0',shell=True, check=True)

        # Creates a pygame object and places the image on the Billboard
        print("input 'ctrl+c' to update the display")
        pygame.init()
        screen=pygame.display.set_mode((0,0))
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h
        image = pygame.image.load("amogus.png")
        image = pygame.transform.scale(image, (width,height))
        screen.blit(image, (0,0))
        pygame.display.flip()
    else:
        print("Insufficient Permission")
except Exception as e:
    print(e)
    pygame.quit()

time.sleep(10000)
