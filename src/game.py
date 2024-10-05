import pygame
import numpy as np
import colour

pygame.mixer.init(frequency=44100, size=-16, channels=1)


class Game:

    def __init__(self, back_images):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        self.back_images = back_images
        self.current_image_index = 0

        self.background_img = self.set_background_image()

    def run(self):
        while self.running:
            # Poll for events
            for event in pygame.event.get():
                self.process_event(event)

            # Fill the screen with the image
            self.set_background_image()
            self.screen.blit(self.background_img, (0, 0))

            # Render your game here

            # Flip the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # Limits FPS to 60

        pygame.quit()

    def process_event(self, event):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener el color RGB en la posición del mouse
            rgb = self.background_img.get_at(
                event.pos)[:3]  # Obtener solo R, G, B
            nm = self.rgb_to_wavelength(rgb)  # Llamar al método de conversión

            print(f"RGB: {rgb}, Longitud de onda: {nm} nm")

            self.play_sound_from_wavelength(nm)

    def set_background_image(self):
        self.background_img = self.back_images[self.current_image_index].background_img
        return self.background_img

    def rgb_to_wavelength(self, rgb):
        rgb_normalized = np.array(rgb) / 255.0
        illuminant = colour.SDS_ILLUMINANTS["FL2"]
        res = colour.convert(
            rgb_normalized,
            "sRGB",
            "Dominant Wavelength",
            sd_to_XYZ={"illuminant": illuminant},
        )

        return res[0]

    def play_sound_from_wavelength(self, nm):
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
        sound_wave = sound_wave.reshape(-1, 1)  # Convertir a 2D
        if pygame.mixer.get_num_channels() == 1:  # Si el mixer está en mono
            # Convertir a forma (n_samples, 1)
            sound_wave = sound_wave.reshape(-1, 1)
        else:  # Si es estéreo, duplicamos el canal
            sound_wave = np.column_stack(
                (sound_wave, sound_wave))  # Crear un array estéreo

        # Crear un objeto de sonido y reproducirlo
        # Sin flatten o reshape, debería funcionar
        sound = pygame.sndarray.make_sound(sound_wave)
        sound.play()
