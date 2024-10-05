import pygame
from game import Game
from background_image import BackgroundImage
import os

if __name__ == '__main__':
    # pygame setup
    pygame.init()

    # Get the path to the "static" dir
    static_dir = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static')

    # List all files in the "static" dir
    img_names = [os.path.join(static_dir, file)
                 for file in os.listdir(static_dir)]

    Game([BackgroundImage(img_name) for img_name in img_names]).run()

    pygame.quit()
