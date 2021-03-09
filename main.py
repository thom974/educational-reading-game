# IMPORTS --------------------------
import pygame
import scripts.menus as m
# INIT -----------------------------
pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.diamond)
screen = pygame.display.set_mode((800,600))
running = True
# MAIN GAME LOOP -------------------
m.main_menu(screen)


