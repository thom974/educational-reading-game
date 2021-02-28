# IMPORTS --------------------------
import pygame
import scripts.classes as c
import scripts.api.api as a
# INIT -----------------------------
pygame.init()
spreadsheet = a.Spreadsheet()
# GLOBALS --------------------------
title_font = pygame.font.Font("data/fonts/scribble.ttf",80)
game_font = pygame.font.Font("data/fonts/scribble.ttf",30)
FPS = 60
# FUNCTIONS ------------------------
def loading_font(string, colour,position,*args):  # string = text to display, colour = tuple, position = tuple
    if len(args) > 0 and args[0]:
        font = title_font.render(string, True, colour)
        font_rect = font.get_rect(center=position)
    else:
        font = game_font.render(string,True,colour)
        font_rect = font.get_rect(center=position)
    return [font, font_rect]
# MENUS ----------------------------
def game_mode_one(screen):
    # main loop variables + control
    running = True
    while running:
        # clear screen
        screen.fill((255,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()

def game_mode_two(screen):
    # main loop variables + control
    running = True
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

def game_mode_three(screen):
    # main loop variables + control
    running = True
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

# main menu - what will be seen upon program launch
def main_menu(screen):
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
                    if selector.current_mode == 0:
                        game_mode_one(screen)
                    elif selector.current_mode == 1:
                        game_mode_two(screen)
                    elif selector.current_mode == 2:
                        game_mode_three(screen)

        # selector code
        selector.draw_frame()
        selector.increment_frame()

        # display game modes
        screen.blit(title,title_rect)
        screen.blit(mode_one,mode_one_rect)
        screen.blit(mode_two,mode_two_rect)
        screen.blit(mode_three, mode_three_rect)

        # pygame code
        pygame.display.flip()
        clock.tick(FPS)
