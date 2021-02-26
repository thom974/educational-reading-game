# IMPORTS --------------------------
import pygame
# INIT -----------------------------
pygame.init()
# GLOBALS --------------------------
title_font = pygame.font.Font("scripts/data/fonts/scribble.ttf",80)
game_font = pygame.font.Font("scripts/data/fonts/scribble.ttf",30)
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
    pass

def game_mode_two(screen):
    pass

def game_mode_three(screen):
    pass

# main menu - what will be seen upon program launch
def main_menu(screen):
    # display title
    title, title_rect = loading_font("The Reading Corner",(255,0,0),(400,150),True)
    screen.blit(title,title_rect)

    # display game modes
    mode_one, mode_one_rect = loading_font("Single Word Mode",(222, 29, 80),(240,300))
    screen.blit(mode_one,mode_one_rect)
    mode_two, mode_two_rect = loading_font("Definition Mode",(161, 21, 58),(200,400))
    screen.blit(mode_two,mode_two_rect)
    mode_three, mode_three_rect = loading_font("Sentence Mode", (121,13,36), (240, 500))
    screen.blit(mode_three, mode_three_rect)

