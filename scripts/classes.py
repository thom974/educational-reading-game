# IMPORTS --------------------------
import pygame
from threading import Thread, Event
import random
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

    def change_mode(self, increment, with_rect):
        if increment > 0:
            self.current_mode = self.current_mode + 1 if self.current_mode < 2 else 0
        else:
            self.current_mode = self.current_mode - 1 if self.current_mode > 0 else 2

        # resizing each frame depending on the current mode selected
        cmr = self.modes[self.current_mode]
        if with_rect:
            self.frame_surfaces[0] = pygame.transform.scale(self.frame_surfaces[0], (cmr.w, cmr.h))
            self.frame_surfaces[1] = pygame.transform.scale(self.frame_surfaces[1], (cmr.w, cmr.h))


class G1(Thread):
    def __init__(self, spreadsheet):
        Thread.__init__(self)
        self.font = pygame.font.Font("data/fonts/scribble.ttf", 60)
        self.h_font = pygame.font.Font("data/fonts/scribble.ttf", 25)
        self.s = spreadsheet
        self.daemon = True
        self.valid_ans = ["Y", "N", "P"]
        self.e = Event()
        self.word_to_display = []
        self.word_history_d = []
        self.answer = None
        self.streak = 0

    def run(self):
        self.s.fetch_endpoint(0)
        while True:
            self.s.find_min()
            self.create_word()
            self.e.wait()  # once found word to display, wait until user guesses it until proceeding

            if self.answer == "Y":
                cur_val = int(self.s.database.cell(self.s.active_row, 2).value)  # get current value in according cell
                self.s.database.update_cell(self.s.active_row, 2, cur_val + 1)
                self.create_h_word(1)
                self.streak += 1
            elif self.answer == "N":
                cur_val = int(self.s.database.cell(self.s.active_row, 3).value)
                self.s.database.update_cell(self.s.active_row, 3, cur_val + 1)
                self.s.incorrect_words.append(self.s.active_word)
                self.create_h_word(2)
                self.streak = 0
            elif self.answer == "P":
                cur_val = int(self.s.database.cell(self.s.active_row, 4).value)
                self.s.database.update_cell(self.s.active_row, 4, cur_val + 1)
                self.create_h_word(3)
                self.streak = 0

            self.e.clear()  # reset flag so that thread will wait.

    def create_word(self):
        word = self.font.render(self.s.active_word, True, (0, 0, 0))
        word_rect = word.get_rect(center=(400, 285))
        self.word_to_display = [word, word_rect]

    def create_h_word(self,num):
        prev_word = self.s.word_history[-1]
        if num == 1:
            color = (50, 168, 82)
        elif num == 2:
            color = (168, 54, 50)
        else:
            color = (222, 217, 84)

        word_str = self.h_font.render(prev_word,True,color)
        self.word_history_d.append([word_str,word_str.get_rect()])  # the font text itself and a Rect, which has NO position yet


class G2(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.e = Event()    # event listener to communicate between threads
        self.daemon = True
        self.question_ans = 0
        self.question_str = ""
        self.question_to_display = []
        self.question_history = []
        self.operation = 0
        self.answers = []
        self.answers_ints = []
        self.selected_ans = 0
        self.streak = 0
        self.q_font = pygame.font.Font("data/fonts/scribble.ttf", 50)
        self.a_font = pygame.font.Font("data/fonts/scribble.ttf", 50)
        self.h_font = pygame.font.Font("data/fonts/scribble.ttf", 25)

    def run(self):
        while True:
            self.answers = []
            self.generate_operation()
            self.generate_question(15)
            self.generate_question_display()
            self.generate_answers()
            self.e.wait()
            self.create_h_question()
            self.e.clear()

    def generate_operation(self):
        self.operation = random.randint(1,2)

    def generate_question(self,max_num):
        num_ans = 0
        if self.operation == 1:
            num_one, num_two = random.randint(1, max_num), random.randint(1, max_num)
            num_ans = num_one + num_two
            self.question_str = str(num_one) + " + " + str(num_two) + " =  ?"
        elif self.operation == 2:
            num_one = random.randint(1, max_num)
            num_two = random.randint(1, num_one)
            num_ans = num_one - num_two
            self.question_str = str(num_one) + " - " + str(num_two) + " =  ?"
        self.question_ans = num_ans

    def generate_question_display(self):
        q_text = self.q_font.render(self.question_str,True,(0,0,0))
        q_text_rect = q_text.get_rect(center=(400, 285))
        self.question_to_display = [q_text,q_text_rect]

    def generate_answers(self):
        alt_one = self.question_ans + random.randint(1,4) * pow(-1,random.randint(1,2))
        alt_two = self.question_ans + random.randint(1,4) * pow(-1,random.randint(1,2))

        while alt_two == alt_one or alt_one < 0 or alt_two < 0:   # ensure alternate choices are not the same
            alt_one = self.question_ans + random.randint(1, 4) * pow(-1, random.randint(1, 2))
            alt_two = self.question_ans + random.randint(1,4) * pow(-1,random.randint(1,2))
        self.answers_ints = [self.question_ans,alt_one,alt_two]
        random.shuffle(self.answers_ints)

        for i, ans in enumerate(self.answers_ints):
            a_text = self.a_font.render(str(ans),True,(0,0,0))
            a_text_rect = a_text.get_rect(center=(200*(i+1),485))
            if ans == self.question_ans:
                self.answers.append([a_text,a_text_rect,'c'])
            else:
                self.answers.append([a_text, a_text_rect])

    def create_h_question(self):
        full_question = self.question_str.replace("?",str(self.answers_ints[self.selected_ans]))
        if 'c' in self.answers[self.selected_ans]:
            h_text = self.h_font.render(full_question,True,(50, 168, 82))
            self.streak += 1
        else:
            h_text = self.h_font.render(full_question, True, (168, 54, 50))
            self.streak = 0

        self.question_history.append([h_text,h_text.get_rect()])

class G3(Thread):
    def __init__(self, spreadsheet):
        Thread.__init__(self)
        self.e = Event()
        self.s = spreadsheet
        self.daemon = True
        self.picture_to_display = None
        self.picture_location = []
        self.current_question_num = 0
        self.current_question = []
        self.pictures_shown = 0
        self.q_font = pygame.font.Font("data/fonts/scribble.ttf", 25)

    def run(self):
        while True:
            self.s.fetch_endpoint(1)
            self.s.find_picture_min()
            self.s.load_picture()
            self.picture_to_display = self.s.image_surface
            self.set_location()
            while self.current_question_num < 6:
                self.generate_question()
                self.e.wait()
                self.e.clear()
            self.update_count()
            self.current_question_num = 0
            self.pictures_shown += 1
            self.e.clear()

    def set_location(self):
        x = 400 - self.picture_to_display.get_width() / 2
        y = 300 - self.picture_to_display.get_height() / 2
        self.picture_location = [x,y]

    def generate_question(self):
        q_str = ""
        if self.current_question_num == 0:
            q_str = "What colours do you see? Shapes? Lines?"
        if self.current_question_num == 1:
            q_str = "Are there people or animals in the picture? What are they doing?"
        if self.current_question_num == 2:
            q_str = "Do you notice a time of day or season?"
        if self.current_question_num == 3:
            q_str = "What do you think the meaning is behind this picture?"
        if self.current_question_num == 4:
            q_str = "Can you make up a short story? Or, you can describe the picture."
        if self.current_question_num == 5:
            q_str = "Answered all questions!"

        q_text = self.q_font.render(q_str,True,(0,0,0))
        q_text_rect = q_text.get_rect(center=(400,525))

        self.current_question_num += 1
        self.current_question = [q_text, q_text_rect]

    def update_count(self):
        cur_val = int(self.s.database.cell(self.s.active_row,2).value)
        self.s.database.update_cell(self.s.active_row,2,cur_val + 1)

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
