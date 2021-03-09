# IMPORTS --------------------------
import pygame
import scripts.menus as m
# INIT -----------------------------
pygame.init()
pygame.display.set_caption("The Reading Corner")
screen = pygame.display.set_mode((800,600))
running = True
# MAIN GAME LOOP -------------------
m.main_menu(screen)


