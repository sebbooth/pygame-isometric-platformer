import pygame, math, os, sys, random
from pygame.locals import *



clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("First Platformer")


WINDOW_H = 1200
WINDOW_W = 800
WINDOW_SIZE = (WINDOW_H,WINDOW_W)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display_h = 200
display_w = 300
display = pygame.Surface((display_w,display_h))


block_image = pygame.image.load("tile5.png")
player_img = pygame.image.load("player.png")

BLOCK_x = 11
BLOCK_y = 11
BLOCK_z = 11

scroll=[0,0]
scroll[0] = int(display_w/2)
scroll[1] = int(display_h/2)

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('+\n')
    game_map = []
    for level in data:
        level_map = []
        level = level.split('\n')
        for row in level:
            level_map.append(list(row))
        game_map.append(level_map)
    return game_map

game_map = load_map('map')


player_rect = pygame.Rect((display_w/2, display_h/2, player_img.get_width(), player_img.get_height()))

true_scroll = [0,0]


moving_right = False
moving_left = False
moving_fwd = False
moving_bwd = False
moving_up = False


x_mom = 0
y_mom = 0
jump_momentum = 0
fall_momentum = 0

while True:
    display.fill((28,0,36))

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20

    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])


    """
    MAP RENDERING
    """
    x=0
    y=0
    z=0
    for level in game_map:
        x_0 = 0
        y_0 = 0
        for row in level:
            x = x_0
            y = y_0
            for block in row:
                if block == '1':
                    display.blit(block_image, (x * BLOCK_x - scroll[0],z*BLOCK_z + y * BLOCK_y - scroll[1]))

                x += 1
                y += 1     
            x_0 -= 1
            y_0 += 1 
        z -= 1

    



    """
    
    (0,0,0) :
    x =    BLOCK_x*-(len(game_map[0])-1)-scroll[0]
    y =    BLOCK_y*(len(game_map[0]))-scroll[1]

    """
    origin = [BLOCK_x*-(len(game_map[0])-1)-scroll[0], BLOCK_y*(len(game_map[0]))-scroll[1]]

    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    test_rect = pygame.Rect(origin[0], origin[1],2,2)

    pygame.draw.rect(display, (255,255,255),test_rect)

    player_rect.x = origin[0]
    player_rect.y = origin[1]

    if moving_fwd:
        player_rect.x+=1
        player_rect.y-=1
    if moving_bwd:
        player_rect.x-=1
        player_rect.y+=1
    if moving_left:
        player_rect.x-=1
        player_rect.y-=1
    if moving_right:
        player_rect.x+=1
        player_rect.y+=1
    if moving_up and jump_momentum == 0:
        jump_momentum=12

    if jump_momentum > 0:
        player_rect.y-=jump_momentum/3
        jump_momentum-=1
        if jump_momentum == 0:
            fall_momentum = 1
    
    if fall_momentum > 0:
        player_rect.y+=fall_momentum/3
        fall_momentum+=1
        if fall_momentum > 12:
            fall_momentum = 0


    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                moving_fwd = True
            if event.key == K_s:
                moving_bwd = True
            if event.key == K_SPACE:
                moving_up = True
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_fwd = False
            if event.key == K_s:
                moving_bwd = False
            if event.key == K_SPACE:
                moving_up = False


    surf = pygame.transform.scale(display, WINDOW_SIZE) 
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)  #stays at 60 fps 

    


