import colour
import numpy as np
import pygame


class BackgroundImage:

    def __init__(self, img_name):
        background_img = pygame.image.load(img_name)
        # TODO: Should crop the image instead of scaling
        self.background_img = pygame.transform.scale(
            background_img, (1280, 720))

    def get_dominant_wavelenght_at(self, pos):
        rgb = self.background_img.get_at(
            pos)[:3]  # Obtener solo R, G, B
        return self._rgb_to_wavelength(rgb)  # Llamar al método de conversión

    def _rgb_to_wavelength(self, rgb):
        rgb_normalized = np.array(rgb) / 255.0
        illuminant = colour.SDS_ILLUMINANTS["FL2"]
        res = colour.convert(
            rgb_normalized,
            "sRGB",
            "Dominant Wavelength",
            sd_to_XYZ={"illuminant": illuminant},
        )

        return res[0]
