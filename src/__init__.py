import os

import pygame

from background_image import BackgroundImage
from game import Game

if __name__ == '__main__':
    # pygame setup
    pygame.init()
    pygame.display.set_caption("Astronotes by 1616")

    # Get the path to the "static" dir
    static_dir = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static')

    # List all files in the "static" dir
    img_names = [os.path.join(static_dir, file.name)
                 for file in os.scandir(static_dir) if file.is_file()]

    Game([BackgroundImage(img_name) for img_name in img_names]).run()

    pygame.quit()
