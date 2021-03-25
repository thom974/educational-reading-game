# IMPORTS --------------------------
import pygame
import threading
import scripts.classes as c
import scripts.api.api as a
# INIT -----------------------------
pygame.init()
spreadsheet = a.Spreadsheet()
# GLOBALS --------------------------
title_font = pygame.font.Font("data/fonts/scribble.ttf",80)
game_font = pygame.font.Font("data/fonts/scribble.ttf",30)
FPS = 60
transition_dictionary = {}
# FUNCTIONS ------------------------
def load_animation_sequence(lst):
    transition_dictionary['scribble'] = []
    for i in range(1,len(lst)+1):
        for _ in range(lst[i-1]):
            transition_dictionary['scribble'].append("transition" + str(i))

def loading_trans_dictionary():
    for i in range(1, 7):
        name = 'transition' + str(i)
        surf = pygame.image.load("data/images/transition/" + name + ".png").convert()
        surf.set_colorkey((0,0,0))
        transition_dictionary[name] = surf

def loading_font(string, colour,position,size):  # string = text to display, colour = tuple, position = tuple
    font_obj = pygame.font.Font("data/fonts/scribble.ttf",size)
    font = font_obj.render(string, True, colour)
    font_rect = font.get_rect(center=position)
    return [font, font_rect]

def transition(screen,frame):
    current_frame_name = transition_dictionary['scribble'][frame]
    current_frame_surf = transition_dictionary[current_frame_name]
    screen.blit(current_frame_surf,(0,0))

# MENUS ----------------------------
def game_mode_one(screen):
    # game mode 1 class
    mode = c.G1(spreadsheet)
    mode.start()

    # transition variables
    start_transition = False
    transition_frame = 0

    # main loop variables + control
    running = True
    clock = pygame.time.Clock()

    # creating art elements / animations
    m_text, m_text_rect = loading_font("Your word:",(0,0,0),[400,110],80)
    h_str, h_rect = loading_font("Word History", (186, 183, 182), (700, 50), 30)
    s_str1, s_rect1 = loading_font("Streak", (186, 183, 182), (75, 50), 30)

    box = c.Animation()
    box.load_frames([pygame.image.load("data/images/box/box1.png").convert(),pygame.image.load("data/images/box/box2.png").convert()])
    box.resize_frames([600,150])
    box.set_position([400,285])

    r_b, w_b, p_b = c.Animation(), c.Animation(), c.Animation()
    r_b.name = "correct"
    w_b.name = "wrong"
    p_b.name = "partial"
    r_b.load_frames([pygame.image.load("data/images/right/right1.png").convert(),pygame.image.load("data/images/right/right2.png").convert()])
    w_b.load_frames([pygame.image.load("data/images/wrong/wrong1.png").convert(),pygame.image.load("data/images/wrong/wrong2.png").convert()])
    p_b.load_frames([pygame.image.load("data/images/partial/partial1.png").convert(),pygame.image.load("data/images/partial/partial2.png").convert()])
    r_b.resize_frames([80,80])
    w_b.resize_frames([80,80])
    p_b.resize_frames([80,80])
    r_b.set_position([200,485])
    w_b.set_position([400,485])
    p_b.set_position([600,485])

    animations = [box,r_b,w_b,p_b]

    while running:
        # clear screen
        screen.fill((255,255,255))

        # mouse code
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    start_transition = True
            if event.type == pygame.MOUSEBUTTONUP:
                for ani in animations:
                    if ani.check_hover(mouse_x,mouse_y):
                        if ani.name == "correct":
                            mode.answer = "Y"
                            mode.e.set()
                        elif ani.name == "wrong":
                            mode.answer = "N"
                            mode.e.set()
                        elif ani.name == "partial":
                            mode.answer = "P"
                            mode.e.set()

        # animation code - each iteration will handle a single Animation object
        for ani in animations:
            screen.blit(ani.frames[ani.cftd],ani.position)
            ani.increment_frame()

        # change cursor when hovering code
        for ani in animations:
            if ani.check_hover(mouse_x,mouse_y) and ani.name != "":
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                break
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        screen.blit(m_text,m_text_rect)

        # display word on screen
        try:
            screen.blit(mode.word_to_display[0],mode.word_to_display[1])
        except IndexError:
            pass

        # display word history
        screen.blit(h_str, h_rect)
        for i in range(1,4):
            try:
                mid = (750 - mode.word_history_d[-1*i][1].w / 2, 150 - 30 * (i - 1))
                mode.word_history_d[-1*i][1].center = mid
                screen.blit(mode.word_history_d[-1*i][0],mode.word_history_d[-1*i][1])
            except IndexError:
                pass

        # display streak
        s_str2, s_rect2 = loading_font(str(mode.streak), (107, 112, 255), (75, 80), 30)
        screen.blit(s_str1,s_rect1)
        screen.blit(s_str2,s_rect2)

        # transition code
        if start_transition:
            transition(screen,transition_frame)
            if transition_frame < len(transition_dictionary['scribble']) - 1:
                transition_frame += 1
            else:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def game_mode_two(screen):
    # game mode class
    mode = c.G2()
    mode.start()

    # main loop variables + control
    running = True
    clock = pygame.time.Clock()

    # transition variables
    start_transition = False
    transition_frame = 0

    # creating art elements / animations
    m_text, m_text_rect = loading_font("Your math question:", (0, 0, 0), [400, 110], 40)
    h_str, h_rect = loading_font("Answers", (186, 183, 182), (700, 50), 30)
    s_str1, s_rect1 = loading_font("Streak", (186, 183, 182), (75, 50), 30)

    # create Selector object
    selector = c.Selector(screen)
    selector.modes = [mode.answers[0][1], mode.answers[1][1],mode.answers[2][1]]
    selector.set_location([200,485])

    box = c.Animation()
    box.load_frames([pygame.image.load("data/images/box/box1.png").convert(),
                     pygame.image.load("data/images/box/box2.png").convert()])
    box.resize_frames([600, 150])
    box.set_position([400, 285])

    animations = [box]      # create a list to hold all Animation objects

    while running:
        # clear screen
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    start_transition = True
                if event.key == pygame.K_LEFT:
                    selector.change_mode(-1,False)
                if event.key == pygame.K_RIGHT:
                    selector.change_mode(1,False)
                if event.key == pygame.K_RETURN:
                    # if 'c' in mode.answers[selector.current_mode]:
                    #     print("You got the answer correct!")
                    # else:
                    #     print("You got the answer wrong.")
                    mode.selected_ans = selector.current_mode
                    mode.e.set()

        # drawing elements to screen
        s_str2, s_rect2 = loading_font(str(mode.streak), (107, 112, 255), (75, 80), 30)
        screen.blit(m_text,m_text_rect)
        screen.blit(h_str,h_rect)
        screen.blit(s_str1,s_rect1)
        screen.blit(s_str2,s_rect2)

        # drawing question history
        for i in range(1,4):
            try:
                mid = (750 - mode.question_history[-1*i][1].w / 2, 150 - 30 * (i - 1))
                mode.question_history[-1*i][1].center = mid
                screen.blit(mode.question_history[-1*i][0],mode.question_history[-1*i][1])
            except IndexError:
                pass

        # drawing Selector to screen
        selector.draw_frame()
        selector.increment_frame()

        # animation code
        for ani in animations:
            screen.blit(ani.frames[ani.cftd],ani.position)
            ani.increment_frame()

        # game mode code
        screen.blit(mode.question_to_display[0],mode.question_to_display[1])
        for q_answer in mode.answers:
            try:
                screen.blit(q_answer[0], q_answer[1])
            except IndexError:
                pass

        # transition code for when mode is exited
        if start_transition:
            transition(screen, transition_frame)
            if transition_frame < len(transition_dictionary['scribble']) - 1:
                transition_frame += 1
            else:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def game_mode_three(screen):
    # game mode variables
    mode = c.G3(spreadsheet)
    mode.start()

    # main loop variables + control
    running = True
    clock = pygame.time.Clock()

    # transition variables
    start_transition = False
    transition_frame = 0

    while running:
        # clear screen
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    start_transition = True
                if event.key == pygame.K_RIGHT:
                    mode.e.set()

        # transition code for when mode is exited
        if start_transition:
            transition(screen, transition_frame)
            if transition_frame < len(transition_dictionary['scribble']) - 1:
                transition_frame += 1
            else:
                running = False

        # display user's image on screen
        try:
            screen.blit(mode.picture_to_display, mode.picture_location)
        except TypeError:
            pass

        # display current question
        try:
            screen.blit(mode.current_question[0],mode.current_question[1])
        except IndexError:
            pass

        # display total pictures shown during current session
        t_text, t_text_rect = loading_font("Total pictures:   " + str(mode.pictures_shown),(186, 183, 182),(400,75),30)
        screen.blit(t_text, t_text_rect)

        pygame.display.flip()
        clock.tick(FPS)

# main menu - what will be seen upon program launch
def main_menu(screen):
    # load transition dictionary
    loading_trans_dictionary()
    load_animation_sequence([5,5,5,5,5,5])
    start_transition = False
    transition_frame = 0

    # creating variables
    title, title_rect = loading_font("The Learning Corner",(255,0,0),(400,150),80)
    mode_one, mode_one_rect = loading_font("Word Mode",(222, 29, 80),(240,300),30)
    mode_two, mode_two_rect = loading_font("Math Mode",(161, 21, 58),(200,400),30)
    mode_three, mode_three_rect = loading_font("Visual Mode", (121,13,36), (240, 500),30)

    # create selector object
    selector = c.Selector(screen)
    selector.modes = [mode_one_rect,mode_two_rect,mode_three_rect]
    selector.set_location([400,300])

    # main loop + loop variables for control
    running = True
    clock = pygame.time.Clock()
    while running:
        # clear screen
        screen.fill((255,255,255))
        for event in pygame.event.get():
            # detect exit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # detect keyboard input
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    selector.change_mode(1,True)
                if event.key == pygame.K_UP:
                    selector.change_mode(-1,True)
                if event.key == pygame.K_RETURN:
                    start_transition = True

        # selector code
        selector.draw_frame()
        selector.increment_frame()

        # display game modes
        screen.blit(title,title_rect)
        screen.blit(mode_one,mode_one_rect)
        screen.blit(mode_two,mode_two_rect)
        screen.blit(mode_three, mode_three_rect)

        # transition code
        if start_transition:
            transition(screen,transition_frame)
            if transition_frame < len(transition_dictionary['scribble']) - 1:
                transition_frame += 1
            else:
                start_transition = False
                transition_frame = 0
                if selector.current_mode == 0:
                    game_mode_one(screen)
                elif selector.current_mode == 1:
                    game_mode_two(screen)
                elif selector.current_mode == 2:
                    game_mode_three(screen)

        # pygame code
        pygame.display.flip()
        clock.tick(FPS)
