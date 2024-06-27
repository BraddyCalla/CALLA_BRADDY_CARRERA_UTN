import pygame
from datos import lista
from biblioteca import *
from os import system

system("cls")
pygame.init()

mostrar_menu_inicio()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_start.collidepoint(event.pos):
                iniciar_juego()
    
    if juego_iniciado:
        mostrar_pregunta()
        juego_iniciado = False

    pygame.display.flip()
    clock.tick(30)
