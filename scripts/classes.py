# IMPORTS --------------------------
import pygame
# INIT -----------------------------
pygame.init()
# CLASSES --------------------------
class Selector:
    def __init__(self, screen):
        self.current_frame = 0
        self.current_mode = 0
        self.modes = []
        self.frame_surfaces = []
        self.location = []
        self.draw_screen = screen
        self.load_frames()

    def load_frames(self):
        selector_one = pygame.image.load("data/images/selection/select1.png")
        selector_two = pygame.image.load("data/images/selection/select2.png")
        selector_one.set_alpha(75)
        selector_two.set_alpha(75)
        self.frame_surfaces = [selector_one,selector_two]

    def increment_frame(self):
        if self.current_frame < 60:
            self.current_frame += 1
        else:
            self.current_frame = 0

    def draw_frame(self):
        cmr = self.modes[self.current_mode]  # cmr = current_mode_rect
        self.set_location([cmr.x + cmr.w / 2, cmr.y + cmr.h / 2])

        # resizing each frame depending on the current mode selected
        for frame in self.frame_surfaces:
            pygame.transform.scale(frame,(cmr.w,cmr.h))

        if self.current_frame < 15:
            self.draw_screen.blit(self.frame_surfaces[0],self.location)
        elif self.current_frame < 30:
            self.draw_screen.blit(self.frame_surfaces[1],self.location)
        elif self.current_frame < 45:
            self.draw_screen.blit(self.frame_surfaces[0],self.location)
        else:
            self.draw_screen.blit(self.frame_surfaces[1],self.location)

    def set_location(self,loc):
        w, h = self.frame_surfaces[0].get_width(), self.frame_surfaces[0].get_height()
        self.location = [loc[0]-w/2, loc[1]-h/2]

    def change_mode(self, increment):
        if increment > 0:
            self.current_mode = self.current_mode + 1 if self.current_mode < 2 else 0
        else:
            self.current_mode = self.current_mode - 1 if self.current_mode > 0 else 2
