import os
import numpy as np
import pygame
import pygame_menu
import sys

pygame.mixer.init(frequency=44100, size=-16, channels=2)

MENU_WIDTH = 800
MENU_HEIGHT = 600
IMG_WIDTH = 1920
IMG_HEIGHT = 1080


class Game:

    def __init__(self, back_images):
        img_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'static/menu')

        music_button_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'music/button/')
        self.music_back_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'music/background/')

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
        self.menu_background_sound = pygame.mixer.Sound(os.path.join(
            self.music_back_dir, "Astronotes_Short_Loopeable_Music.mp3"))
        self.menu_background_sound.play(-1)

        self.play_sound = pygame.mixer.Sound(
            os.path.join(music_button_dir, "Button_Press.mp3"))

        self.how_to_sound_in = pygame.mixer.Sound(
            os.path.join(music_button_dir, "Howto_Splash_in.mp3"))

        self.how_to_sound_out = pygame.mixer.Sound(
            os.path.join(music_button_dir, "Howto_Splash_out.mp3"))
        self.quit_sound = pygame.mixer.Sound(
            os.path.join(music_button_dir, "Button_Press.mp3"))
        self.select_sound = pygame.mixer.Sound(
            os.path.join(music_button_dir, "Button_Select.mp3"))

        self.menu = pygame_menu.Menu(
            'Astronotes', MENU_WIDTH, MENU_HEIGHT, theme=theme_menu)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "Play_Button-V3.png")).scale(0.25, 0.25), self._play)
        self.menu.add.vertical_margin(15)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "How-to_Button-V3.png")).scale(0.25, 0.25), self._how_to)
        self.menu.add.vertical_margin(15)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "Quit_Button-V3.png")).scale(0.25, 0.25), self._quit_game)

    def run(self):
        pygame.event.clear()
        self.menu.mainloop(self.screen)

    def _quit_game(self):
        self.how_to_sound_in.play()
        pygame.time.delay(150)
        pygame.quit()
        sys.exit()

    def _how_to(self):
        self.how_to_sound_in.play()
        how_to_image_active = True
        img_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'static/menu')
        imp = pygame.image.load(os.path.join(
            img_dir, "How-to-Transparent_Splash-V3.png")
            ).convert_alpha()
        img_width, img_height = imp.get_size()
        screen_width, screen_height = self.screen.get_size()
        x = (screen_width - img_width) // 2
        y = (screen_height - img_height) // 2
        self.screen.blit(imp, (x, y))
        pygame.display.flip()
        
        while self.running and how_to_image_active:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    how_to_image_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        how_to_image_active = False 

            # Update the display
        self.how_to_sound_out.play()
        pygame.display.flip()


    def _play(self):
        self.menu_background_sound.stop()
        self.play_sound.play()
        self.screen = pygame.display.set_mode(
            (IMG_WIDTH, IMG_HEIGHT), pygame.RESIZABLE | pygame.FULLSCREEN)

        self._backgroundSound()
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

    def _process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # Change to the next image
                self.select_sound.play()
                self.current_image_index = (
                    self.current_image_index + 1) % len(self.back_images)
            elif event.key == pygame.K_LEFT:
                self.select_sound.play()
                self.current_image_index = (
                    self.current_image_index - 1) % len(self.back_images)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener el color RGB en la posición del mouse
            wavelength = self.background_img.get_dominant_wavelenght_at(
                event.pos)
            print(f"Longitud de onda: {wavelength} nm")
            self._play_sound_from_wavelength(wavelength)

    def _set_background_image(self):
        self.background_img = self.back_images[self.current_image_index]
        return self.background_img

    # de momento a espera si se usa
    def _low_pass_filter(self, signal, alpha=0.1):
        filtered_signal = np.zeros_like(signal)
        for i in range(1, len(signal)):
            filtered_signal[i] = alpha * signal[i] + \
                (1 - alpha) * filtered_signal[i - 1]
        return filtered_signal

    def _play_sound_from_wavelength(self, nm):

        # Convertir nanómetros a metros
        wavelength_m = nm * 1e-9  # convertir nm a metros
        # Calcular la frecuencia
        frequency = 360 / wavelength_m  # velocidad del sonido / longitud de onda

        max_frequency = 360 / (400 * 1e-9)
        min_frequency = 360 / (700 * 1e-9)

        frequency = ((frequency - min_frequency) /
                     (max_frequency - min_frequency)) * (4186 - 27.5) + 27.5

        print(frequency)

        # Generar el sonido similar a un órgano de iglesia
        sample_rate = 44100
        duration = 2.0  # duración en segundos
        t = np.linspace(0, duration, int(
            sample_rate * duration), endpoint=False)

        sound_wave = (0.4 * np.sin(2 * np.pi * frequency * t) +
                      0.2 * np.sin(2 * np.pi * 1.5 * frequency * t))  # onda senoidal

        attack_duration = 0.5  # Duración de ataque en segundos
        sustain_duration = 1.5  # Duración de sostenido en segundos
        decay_duration = 0.5  # Duración de caída en segundos

        attack = np.linspace(0, 1, int(sample_rate * attack_duration))
        sustain = np.ones(int(sample_rate * sustain_duration))
        decay = np.linspace(1, 0, int(sample_rate * decay_duration))

        envelope = np.concatenate((attack, sustain, decay))

        if len(envelope) < len(sound_wave):
            envelope = np.pad(
                envelope, (0, len(sound_wave) - len(envelope)), 'constant')
        else:
            envelope = envelope[:len(sound_wave)]

        organ_sound = sound_wave * envelope

        # Aplicar filtro pasa-bajos deprecado
        organ_sound = self._low_pass_filter(organ_sound)

        # Convertir a tipo de datos de audio
        organ_sound = (organ_sound * 32767).astype(np.int16)

        organ_sound = organ_sound.reshape(-1, 1)
        organ_sound = np.column_stack((organ_sound, organ_sound))

        sound = pygame.sndarray.make_sound(organ_sound)
        sound.play()

    def _backgroundSound(self):
        pygame.mixer.music.load(os.path.join(
            self.music_back_dir, "188831__0ktober__0ktober_hyperspace.wav"))
        pygame.mixer.music.play(-1)
