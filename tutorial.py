import random
import pygame
from darkrooms import *
from colors import *


FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial")
clock = pygame.time.Clock()
running = True
player = Player(WIDTH / 4, HEIGHT / 2, 25, 25, PRIMARY, 5, 5, False, False)
color_shower = StaticObject(WIDTH - 20, HEIGHT - 20, 20, 20, player.bullet_colors[player.bullet_color_index % 3], True, False)
pygame.mouse.set_visible(False)
header = Text(WIDTH / 2 - (Text.find_text_size('Tutorial', 30) / 2), 10, 30, (255,255,255), 'Tutorial')



while running:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            player.handle_keydown(event.key)
            if event.key == pygame.K_2:
                header.hidden = True
    mouse_x, mouse_y = pygame.mouse.get_pos() 
    color_shower.color = player.bullet_colors[player.bullet_color_index % 3]
    color_shower.draw(window)
    player.update()
    player.handle_movement()
    player.draw(window)
    header.draw(window)

    pygame.display.update()
    clock.tick(FPS)
