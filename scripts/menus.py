# IMPORTS --------------------------
import pygame
import threading
import scripts.classes as c
import scripts.api.api as a
# INIT -----------------------------
pygame.init()
spreadsheet = a.Spreadsheet()
spreadsheet.fetch_endpoint()
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
    print(transition_dictionary['scribble'])

def loading_trans_dictionary():
    for i in range(1, 7):
        name = 'transition' + str(i)
        surf = pygame.image.load("data/images/transition/" + name + ".png").convert()
        surf.set_colorkey((0,0,0))
        transition_dictionary[name] = surf
    print(transition_dictionary)

def loading_font(string, colour,position,*args):  # string = text to display, colour = tuple, position = tuple
    if len(args) > 0 and args[0]:
        font = title_font.render(string, True, colour)
        font_rect = font.get_rect(center=position)
    else:
        font = game_font.render(string,True,colour)
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
    m_text, m_text_rect = loading_font("Your word:",(0,0,0),[400,80],True)

    box = c.Animation()
    box.load_frames([pygame.image.load("data/images/box/box1.png").convert(),pygame.image.load("data/images/box/box2.png").convert()])
    box.resize_frames([600,150])
    box.set_position([400,255])

    r_b, w_b, p_b = c.Animation(), c.Animation(), c.Animation()
    r_b.load_frames([pygame.image.load("data/images/right/right1.png").convert(),pygame.image.load("data/images/right/right2.png").convert()])
    w_b.load_frames([pygame.image.load("data/images/wrong/wrong1.png").convert(),pygame.image.load("data/images/wrong/wrong2.png").convert()])
    p_b.load_frames([pygame.image.load("data/images/partial/partial1.png").convert(),pygame.image.load("data/images/partial/partial2.png").convert()])
    r_b.resize_frames([80,80])
    w_b.resize_frames([80,80])
    p_b.resize_frames([80,80])
    r_b.set_position([200,455])
    w_b.set_position([400,455])
    p_b.set_position([600,455])

    animations = [box,r_b,w_b,p_b]

    while running:
        # clear screen
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    start_transition = True
                if event.key == pygame.K_l:
                    print(threading.active_count())

        # drawing elements on the screen
        for ani in animations:
            screen.blit(ani.frames[ani.cftd],ani.position)
            ani.increment_frame()

        screen.blit(m_text,m_text_rect)

        # display word on screen
        try:
            screen.blit(mode.word_to_display[0],mode.word_to_display[1])
        except IndexError:
            pass

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
    # main loop variables + control
    running = True
    clock = pygame.time.Clock()
    while running:
        # clear screen
        screen.fill((0, 255, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()
        clock.tick(FPS)

def game_mode_three(screen):
    # main loop variables + control
    running = True
    clock = pygame.time.Clock()
    while running:
        # clear screen
        screen.fill((0, 0, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

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
    title, title_rect = loading_font("The Reading Corner",(255,0,0),(400,150),True)
    mode_one, mode_one_rect = loading_font("Single Word Mode",(222, 29, 80),(240,300))
    mode_two, mode_two_rect = loading_font("Definition Mode",(161, 21, 58),(200,400))
    mode_three, mode_three_rect = loading_font("Sentence Mode", (121,13,36), (240, 500))

    # create selector object
    selector = c.Selector(screen)
    selector.modes = [mode_one_rect,mode_two_rect,mode_three_rect]
    selector.load_frames()
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
                    selector.change_mode(1)
                if event.key == pygame.K_UP:
                    selector.change_mode(-1)
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
