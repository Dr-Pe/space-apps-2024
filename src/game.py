import os
import numpy as np
import pygame
import pygame_menu

pygame.mixer.init(frequency=44100, size=-16, channels=2)

MENU_WIDTH = 800
MENU_HEIGHT = 600
IMG_WIDTH = 1920
IMG_HEIGHT = 1080


class Game:

    def __init__(self, back_images):
        img_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'static/menu')

        self.screen = pygame.display.set_mode(
            (MENU_WIDTH, MENU_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.back_images = back_images
        self.current_image_index = 0

        self.background_img = self._set_background_image()

        ico = pygame.image.load(os.path.join(
            img_dir, "logo1616.ico"))
        pygame.display.set_icon(ico)

        background_menu = pygame_menu.baseimage.BaseImage(
            image_path=os.path.join(
                img_dir, "background.png"),
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
        )
        theme_menu = pygame_menu.themes.THEME_DARK.copy()
        theme_menu.background_color = background_menu

        self.menu = pygame_menu.Menu(
            'Caressing the void', MENU_WIDTH, MENU_HEIGHT, theme=theme_menu)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "Play_Button-V3.png")).scale(0.25, 0.25), self._play)
        self.menu.add.vertical_margin(15)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "How-to_Button-V3.png")).scale(0.25, 0.25), print, "how to")
        self.menu.add.vertical_margin(15)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "Quit_Button-V3.png")).scale(0.25, 0.25), pygame_menu.events.EXIT)

    def run(self):
        pygame.event.clear()
        self.menu.mainloop(self.screen)

    def _play(self):
        self.screen = pygame.display.set_mode(
            (IMG_WIDTH, IMG_HEIGHT), pygame.RESIZABLE | pygame.FULLSCREEN)

        while self.running:
            # Poll for events
            for event in pygame.event.get():
                self._process_event(event)

            # Fill the screen with the image
            self._set_background_image()
            self.screen.blit(self.background_img.background_img, (0, 0))

            # Render your game here

            # Flip the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # Limits FPS to 60

        self.menu.close(pygame_menu.events.EXIT)

    def _process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # Change to the next image
                self.current_image_index = (
                    self.current_image_index + 1) % len(self.back_images)
            elif event.key == pygame.K_LEFT:
                self.current_image_index = (
                    self.current_image_index - 1) % len(self.back_images)
            elif event.key == pygame.K_ESCAPE:
                self.menu.close(pygame_menu.events.EXIT)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener el color RGB en la posición del mouse
            wavelength = self.background_img.get_dominant_wavelenght_at(
                event.pos)
            print(f"Longitud de onda: {wavelength} nm")
            self._play_sound_from_wavelength(wavelength)

    def _set_background_image(self):
        self.background_img = self.back_images[self.current_image_index]
        return self.background_img

    def _play_sound_from_wavelength(self, nm):
        # Convertir nanómetros a metros
        wavelength_m = nm * 1e-9  # convertir nm a metros
        # Calcular la frecuencia
        # 360 m/s
        frequency = 360 / wavelength_m  # velocidad del sonido / longitud de onda

        max_frequency = 360/(400*1e-9)
        min_frequency = 360/(700*1e-9)

        frequency = ((frequency - min_frequency) /
                     (max_frequency - min_frequency)) * (4186-27.5) + 27.5

        print(frequency)

        # Generar una onda sonora simple (seno)
        sample_rate = 44100
        duration = 1.0  # duración en segundos
        t = np.linspace(0, duration, int(
            sample_rate * duration), endpoint=False)
        sound_wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # onda senoidal

        # Convertir a tipo de datos de audio
        sound_wave = (sound_wave * 32767).astype(np.int16)  # convertir a int16
        # Si es estéreo, duplicamos el canal (lo seteamos como estereo en el init, revisar)
        sound_wave = sound_wave.reshape(-1, 1)  # Convertir a 2D
        sound_wave = np.column_stack(
            (sound_wave, sound_wave))  # Crear un array estéreo

        # Crear un objeto de sonido y reproducirlo
        # Sin flatten o reshape, debería funcionar
        sound = pygame.sndarray.make_sound(sound_wave)
        sound.play()
