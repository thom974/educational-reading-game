# IMPORTS --------------------------
import pygame
from threading import Thread, Event

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
        selector_one = pygame.image.load("data/images/selection/select1.png").convert()
        selector_two = pygame.image.load("data/images/selection/select2.png").convert()
        selector_one = pygame.transform.scale(selector_one, (181, 32))
        selector_two = pygame.transform.scale(selector_two, (181, 32))
        selector_one.set_alpha(100)
        selector_two.set_alpha(100)
        self.frame_surfaces = [selector_one, selector_two]

    def increment_frame(self):
        if self.current_frame < 60:
            self.current_frame += 1
        else:
            self.current_frame = 0

    def draw_frame(self):
        cmr = self.modes[self.current_mode]  # cmr = current_mode_rect
        self.set_location([cmr.x + cmr.w / 2, cmr.y + cmr.h / 2])

        if self.current_frame < 15:
            self.draw_screen.blit(self.frame_surfaces[0], self.location)
        elif self.current_frame < 30:
            self.draw_screen.blit(self.frame_surfaces[1], self.location)
        elif self.current_frame < 45:
            self.draw_screen.blit(self.frame_surfaces[0], self.location)
        else:
            self.draw_screen.blit(self.frame_surfaces[1], self.location)

    def set_location(self, loc):
        w, h = self.frame_surfaces[0].get_width(), self.frame_surfaces[0].get_height()
        self.location = [loc[0] - w / 2, loc[1] - h / 2]

    def change_mode(self, increment):
        if increment > 0:
            self.current_mode = self.current_mode + 1 if self.current_mode < 2 else 0
        else:
            self.current_mode = self.current_mode - 1 if self.current_mode > 0 else 2

        # resizing each frame depending on the current mode selected
        cmr = self.modes[self.current_mode]
        self.frame_surfaces[0] = pygame.transform.scale(self.frame_surfaces[0], (cmr.w, cmr.h))
        self.frame_surfaces[1] = pygame.transform.scale(self.frame_surfaces[1], (cmr.w, cmr.h))


class G1(Thread):
    def __init__(self, spreadsheet):
        Thread.__init__(self)
        self.font = pygame.font.Font("data/fonts/scribble.ttf", 60)
        self.daemon = True
        self.s = spreadsheet
        self.valid_ans = ["Y", "N", "P"]
        self.e = Event()
        self.word_to_display = []
        self.answer = None

    def run(self):
        while True:
            self.s.find_min()
            self.create_word()
            self.e.wait()  # once found word to display, wait until user guesses it until proceeding

            if self.answer == "Y":
                cur_val = int(self.s.database.cell(self.s.active_row, 2).value)  # get current value in according cell
                self.s.database.update_cell(self.s.active_row, 2, cur_val + 1)
            elif self.answer == "N":
                cur_val = int(self.s.database.cell(self.s.active_row, 3).value)
                self.s.database.update_cell(self.s.active_row, 3, cur_val + 1)
                self.s.incorrect_words.append(self.s.active_word)
            elif self.answer == "P":
                cur_val = int(self.s.database.cell(self.s.active_row, 4).value)
                self.s.database.update_cell(self.s.active_row, 4, cur_val + 1)

            self.e.clear()  # reset flag so that thread will wait.

    def create_word(self):
        word = self.font.render(self.s.active_word, True, (0, 0, 0))
        word_rect = word.get_rect(center=(400, 285))
        self.word_to_display = [word, word_rect]


class Animation:  # two frame scribble animations
    def __init__(self):
        self.name = ""
        self.frames = []
        self.current_frame = 0
        self.cftd = 0
        self.position = []

    def set_position(self, pos):
        self.position = [pos[0] - self.frames[0].get_width() / 2, pos[1] - self.frames[0].get_height() / 2]

    def load_frames(self, frames):
        self.frames = frames

    def resize_frames(self, size):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], size)

    def increment_frame(self):
        if self.current_frame < 60:
            if self.current_frame % 20 == 0:
                self.cftd = 1 if self.cftd == 0 else 0
            self.current_frame += 1
        else:
            self.current_frame = 0

    def check_hover(self, xm, ym):
        hitbox = self.frames[0].get_rect(x=self.position[0], y=self.position[1])
        return hitbox.collidepoint(xm, ym)
