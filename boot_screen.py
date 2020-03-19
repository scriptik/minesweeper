import pygame

from sound_engine import MusicPlayer
import data

class BootScreen:
    """  The boot screen! """
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.music_player = MusicPlayer("boot.mp3")
        self.clock = pygame.time.Clock()

    def main(self):
        """ Display the screen and a little bit of text at the bottom
            of the screen. """
        self.music_player.once()

        img_logo = pygame.image.load(data.filepath(".","mineboot.png"))
        #img_logo = pygame.transform.smoothscale(img_logo,util.scale(img_logo,width=self.unit*15))
        #img_logo = pygame.transform.smoothscale(img_logo,(320,240))
        img_logo = pygame.transform.smoothscale(img_logo,(320,240))
        img_logo_rect = img_logo.get_rect()
        img_logo_rect.centerx = 160
        img_logo_rect.centery = 120
        #img_logo_rect.centerx = self.screen.get_rect().centerx
        #img_logo_rect.centery = self.screen.get_rect().centery

        #settings
        seconds_in = 2
        seconds_still = 2
        seconds_out = 2

        fps = 20
        logo_alpha = 0
        logo_alpha_add = int(255.0/float(fps*seconds_in))
        logo_alpha_sub = -int(255.0/float(fps*seconds_out))
        logo_alpha_sum = logo_alpha_add
        stop_counter = fps*seconds_still

        skip = False

        # LOGO INTRO
        while not skip:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    skip = True
                elif event.type == pygame.QUIT:
                    self.running = False
                    return

            #self.screen.fill((0, 0, 0))
            self.screen.fill((255, 255, 255))
            img_logo.set_alpha(logo_alpha)
            self.screen.blit(img_logo, img_logo_rect)

            if logo_alpha == 255 and stop_counter > 0:
                stop_counter-=1
            else:
                logo_alpha += logo_alpha_sum
                if logo_alpha > 255:
                    logo_alpha = 255
                    logo_alpha_sum = logo_alpha_sub
                elif logo_alpha < 0:
                    break

            pygame.display.update()
            self.clock.tick(fps)

        self.music_player.stop()
