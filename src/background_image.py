import pygame


class BackgroundImage:

    def __init__(self, img_name):
        background_img = pygame.image.load(img_name)
        self.background_img = pygame.transform.scale(
            background_img, (1280, 720))  # TODO: Should crop the image instead of scaling
