import os
import textwrap
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
        font_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'static/font')

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
            img_dir, "How-to_Button-V3.png")).scale(0.25, 0.25), self._how_to)
        self.menu.add.vertical_margin(15)

        self.menu.add.banner(pygame_menu.BaseImage(image_path=os.path.join(
            img_dir, "Quit_Button-V3.png")).scale(0.25, 0.25), pygame_menu.events.EXIT)

        self.modal_bg_img = pygame.image.load(os.path.join(
            img_dir, "How-to-Transparent_Splash-V3.png"))

        font_path = os.path.join(
            font_dir, "ComingSoon-Regular.ttf")

        self.font_tittle = pygame.font.Font(font_path, 25)
        self.font_text = pygame.font.Font(font_path, 20)

    def run(self):
        pygame.event.clear()
        self.menu.mainloop(self.screen)

    def _how_to(self):
        modal_active = True

        while self.running and modal_active:
            # First, render the menu
            self.menu.draw(self.screen)  # Draw the menu behind the modal

            # Draw the modal box on top of the menu
            modal_width, modal_height = 450, 400
            modal_surface = pygame.Surface((modal_width, modal_height))
            modal_surface.fill((100, 100, 100))  # Dark gray modal background
            modal_rect = modal_surface.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

            # Scale background img
            scaled_bg_img = pygame.transform.scale(
                self.modal_bg_img, (modal_width, modal_height))

            # Draw modal background
            modal_surface.blit(scaled_bg_img, (0, 0))
            # Render the "HOW TO" title in the center of the modal box
            # Larger font for the title
            font_title = self.font_tittle  # pygame.font.Font(None, 32)
            title_text = "How to use:"
            title_surface = font_title.render(
                title_text, True, (0, 0, 0))  # black text
            title_rect = title_surface.get_rect(
                center=(modal_rect.width // 2, modal_rect.height // 7))  # Move title down a bit

            # Render the instructions text (with a considerable gap)
            # Adjust font size for readability
            font = self.font_text  # pygame.font.Font(None, 28)

            text = """Discover the universe through sound! Click anywhere on the image and a one-of-a-kind auditory experience 
            will be created based on the liminal frequency data from the JWST. Each click reveals a new cosmic sound."""

            # Use textwrap to split the text into lines that fit the modal width
            # Adjust width to fit your modal
            wrapped_text = textwrap.wrap(text, width=40)

            # Calculate starting position for wrapped text (increase gap between title and content)
            start_y = title_rect.bottom + 50

            # Render each line of text
            for i, line in enumerate(wrapped_text):
                text_surface = font.render(
                    line, True, (0, 0, 0))  # black text
                text_rect = text_surface.get_rect(
                    center=(modal_rect.width // 2, start_y + i * font.get_height()))
                modal_surface.blit(text_surface, text_rect)

            # Blit modal onto the screen (including title and text)
            self.screen.blit(modal_surface, modal_rect)
            self.screen.blit(title_surface, title_rect.move(
                modal_rect.left, modal_rect.top))  # Ensure title is inside the modal

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    modal_active = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Close the modal when clicked anywhere on the screen (not just inside the modal)
                    modal_active = False
                    self.menu.close()  # Close the menu when modal is closed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        modal_active = False  # Close the modal on Escape key

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

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

        max_frequency = 360 / (400 * 1e-9)
        min_frequency = 360 / (700 * 1e-9)

        frequency = ((frequency - min_frequency) /
                     (max_frequency - min_frequency)) * (4186 - 27.5) + 27.5

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
