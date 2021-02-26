# IMPORTS --------------------------
import pygame
import scripts.menus as m
# INIT -----------------------------
pygame.init()
screen = pygame.display.set_mode((800,600))
running = True
# MAIN GAME LOOP -------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    m.main_menu(screen)

    pygame.display.flip()

