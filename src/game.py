import pygame


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
            # poll for events
            for event in pygame.event.get():
                self.process_event(event)

            # fill the screen with the image
            self.set_background_image()
            self.screen.blit(self.background_img, (0, 0))

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

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
            print(self.background_img.get_at(event.pos))

    def set_background_image(self):
        self.background_img = self.back_images[self.current_image_index].background_img

        return self.background_img
