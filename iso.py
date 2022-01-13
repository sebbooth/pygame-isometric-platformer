import pygame, math, os, sys, random
from pygame.locals import *
import datetime as dt
from datetime import datetime
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("isoplat")



"""
FUNCTIONS
"""
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

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

def collision_objects(game_map):
    tile_rects = []
    for level in game_map:
            y = 0
            level_rects=[]
            for row in level:
                x = 0
                for block in row:
                    if block != '0':
                        level_rects.append(pygame.Rect(11*x,11*y, 11,11))
                    x+=1
                y+=1   
            tile_rects.append(level_rects) 
    return tile_rects

def handle_particles(particles, timer, col):
    for particle in particles:
        pygame.draw.circle(display, col,
            (11+DISPLAY_W/2 + particle[0][0]-scroll[0],
            10+DISPLAY_H/2 + particle[0][1]-scroll[1]), particle[2])
    
        if timer == 0:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            if particle[2] <= 0:
                particles.remove(particle)
            timer = 3
        else:
            timer -= 1



"""
CONSTANTS
"""
WINDOW_H = 1200
WINDOW_W = 800
WINDOW_SIZE = (WINDOW_H,WINDOW_W)
DISPLAY_H = 200
DISPLAY_W = 300
BLOCK_x = 11
BLOCK_y = 11
BLOCK_z = 11



"""
LOAD IMAGES
"""
block_image = pygame.image.load("blocks/tile5.png")
grass = pygame.image.load("blocks/grass_block.png")
rock = pygame.image.load("blocks/rock_block.png")
fire =  pygame.image.load("blocks/fire.png")
player_img = pygame.image.load("player_slices/slice0.png")

slices = [
pygame.image.load("player_slices/slice0.png"),
pygame.image.load("player_slices/slice1.png"),
pygame.image.load("player_slices/slice2.png"),
pygame.image.load("player_slices/slice3.png"),
pygame.image.load("player_slices/slice4.png"),
pygame.image.load("player_slices/slice5.png"),
]



"""
INITIALIZE pygame OBJECTS
"""
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_W,DISPLAY_H))
player_rect = pygame.Rect(0,0,5,5)
player = pygame.Rect((DISPLAY_W/2, DISPLAY_H/2, player_img.get_width(), player_img.get_height()))



"""
LOAD GAME MAP AND CREATE LIST OF COLLIDEABLE BLOCKS
"""
game_map = load_map('map1')
tile_rects = collision_objects(game_map)



"""
SPAWN COORDS
"""
z = (6+10)*11
player_rect.x = (1)*11
player_rect.y = (1)*11



"""
INITIALIZE VARIABLES
"""
moving_right = False
moving_left = False
moving_fwd = False
moving_bwd = False
jump = False
on_ground = False
mirror = False
movement = False

particles = []
flame = []
true_scroll = [0,0]

flametimer = 0
smoketimer = 0
z_momentum = 0
z_prev = z
level = 0



"""
FOR FPS COUNTER
""
before = dt.datetime.today().timetuple()[5]
fps = 0
""
end fps counter
"""



"""
GAME LOOP
"""
while True:
    """
    FPS COUNTER
    ""
    now = dt.datetime.today().timetuple()[5]
    if now == (before+1)%60:
        print(fps)
        fps = 0
        before = now
    fps+=1
    ""
    end fps counter
    """


    """
    RESET LAYERS
    """
    transparents = pygame.Surface((DISPLAY_W,DISPLAY_H))
    transparents.set_alpha(50)
    display.fill((60,0,90))



    """
    CALCULATE CAMERA/SCROLL
    """
    true_scroll[0] += (player.x - DISPLAY_W/2 - 6)/20
    true_scroll[1] += (player.y - DISPLAY_H/2 + 22)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    
    

    """
    #DEBUGGING

    #print('height: ' + str(z) + ' prev height: ' + str(z_prev) + ' momentum: ' + str(z_momentum) + ' level : ' + str(level))
    #print(str(int(player_rect.x/11)), str(int(player_rect.y/11)), str(int(z/11)))
    """



    """
    DETECT GROUND COLLISIONS
    """
    for n in range(len(tile_rects)):
            if (z <= n*11 and n*11 <= z_prev):
                level = n
                ground = collision_test(player_rect, tile_rects[level])
                if len(ground) > 0:
                    on_ground = True
                    z = n*11
                else:
                    on_ground = False

            elif (z >= n*11 and n*11 < z_prev):
                level = n


    """
    DISPLAY MINIMAP (FOR DEBUG)
    """
    for tile_rect in tile_rects[level]:
        pygame.draw.rect(transparents,(0,255,255),tile_rect)
        
    for tile_rect in tile_rects[level+1]:
        pygame.draw.rect(transparents,(0,0,255),tile_rect)

    pygame.draw.rect(transparents,(255,255,255),player_rect)



    """
    MOVEMENT

    movement boolean switches back and forth so movement is every other tick
    """
    if movement:
        movement = False


        """
        PLAYER x and y MOVEMENT with collision checks
        """
        if moving_fwd:
            player_rect.x+=1
        if moving_bwd:
            player_rect.x-=1

        walls = collision_test(player_rect,tile_rects[1+int(z/11)]) + collision_test(player_rect,tile_rects[1+int((10+z)/11)])

        if len(walls) > 0:  #handle collision detected
            if moving_fwd:
                player_rect.right = walls[0].left
            if moving_bwd:
                player_rect.left = walls[0].right

        if moving_right:
            player_rect.y+=1
        if moving_left:
            player_rect.y-=1

        walls = collision_test(player_rect,tile_rects[1+int(z/11)]) + collision_test(player_rect,tile_rects[1+int((10+z)/11)])
        
        if len(walls) > 0:  #handle collision detected
            if moving_right:
                player_rect.bottom = walls[0].top
            if moving_left:
                player_rect.top = walls[0].bottom



        """
        PLAYER JUMP/FALLs
        """
        z_momentum -= 1
        if z_momentum <= -6:
            z_momentum = -6

        if on_ground:
            z_momentum = 0
            
            if jump:
                ceiling = collision_test(player_rect, tile_rects[level+2])
                if len(ceiling) == 0:
                    z_momentum += 6
                    on_ground = False
                    ground = []
                ceiling = []
        z_prev = z
        z += z_momentum
    else:
        movement = True


    
    """
    HANDLE USER INPUTS
    """    
    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                jump = True
            if event.key == K_s:
                moving_right = True
            if event.key == K_w:
                moving_left = True

            if event.key == K_d:
                if mirror:
                    moving_bwd = True
                else:
                    moving_fwd = True
            if event.key == K_a:
                if mirror:
                    moving_fwd = True
                else:
                    moving_bwd = True
            if event.key == K_f:
                if mirror:
                    mirror = False
                else:
                    mirror = True

        if event.type == KEYUP:
            if event.key == K_SPACE:
                jump = False
            if event.key == K_s:
                moving_right = False
            if event.key == K_w:
                moving_left = False

            if event.key == K_d:
                if mirror:
                    moving_bwd = False
                else:
                    moving_fwd = False
            if event.key == K_a:
                if mirror:
                    moving_fwd = False
                else:
                    moving_bwd = False
            


    """
    RENDERING 
    DONE IN ORDER OF COORDINATES
    """

    """
    CHECKS IF PLAYER RENDER MUST BE SLICED
    """    
    slice = 11-(player_rect.y%11)
    if slice <=4 and slice >=1:
        blit_slice = True
    else:
        blit_slice = False


    player_coords = [int((player_rect.x+player_rect.width-1)/11), int((player_rect.y)/11), int(2+level)]
    if on_ground:
        player_coords[2] = level+1



    """
    MIRRORED RENDERING
    """
    if mirror:
        render_x=0
        render_y=0

        for render_z in range(0,len(game_map)+1):
            for render_y in range(0,20):
                for render_x in range(-20,1):
                    try:
                        if game_map[render_z][render_y][-render_x] != '0':
                            block_x = DISPLAY_W/2 + render_x * BLOCK_x + render_y * -BLOCK_y - scroll[0]
                            block_y = DISPLAY_H/2  + render_x * BLOCK_x + render_y * BLOCK_y - render_z * BLOCK_z - scroll[1]

                            if game_map[render_z][render_y][-render_x] == '1':
                                display.blit(block_image, (block_x,block_y))
                            if game_map[render_z][render_y][-render_x] == '2':
                                display.blit(grass, (block_x,block_y))
                            if game_map[render_z][render_y][-render_x] == '3':
                                display.blit(rock, (block_x,block_y))
                            if game_map[render_z][render_y][-render_x] == '4':
                                display.blit(fire, (block_x,block_y))
                                if flametimer%11 == 0:
                                    light_radius = random.randint(10,12)
                                pygame.draw.circle(transparents, (255, 165, 0), (BLOCK_x+block_x, BLOCK_y+block_y), light_radius)
                        
                                particle_x = render_x * BLOCK_x + render_y * -BLOCK_y
                                particle_y = render_x * BLOCK_x + render_y * BLOCK_y - render_z * BLOCK_z

                                particles.append([[particle_x, particle_y], [random.randint(0,20)/10-1, random.randint(-4,-1)], random.randint(1,2)])
                               
                                if flametimer == 0:
                                    flame.append([[particle_x, particle_y], [0, -1], random.randint(1,3)])
                                    flametimer = 10
                                else:
                                    flametimer -= 1
                        
                    except:
                        pass
                    
                    if -render_x == player_coords[0] and render_z == player_coords[2]:
                        if render_y == player_coords[1]:
                            display.blit(player_img, (player.x, player.y))
                        elif render_y == 1+player_coords[1] and blit_slice:
                            display.blit(slices[slice], (player.x, player.y))
                        
        y = player_rect.x * -1 + player_rect.y * 1 - 33
        x = player_rect.x * -1 + player_rect.y * -1 + 23
        player.x = DISPLAY_W/2 + x - player.width - scroll[0]
        player.y = DISPLAY_W/2 + y - z - player.height - scroll [1]



        """
        NORMAL RENDERING
        """
    else:
        render_x=0
        render_y=0
        for render_z in range(0,len(game_map)+1):
            for render_y in range(0,20):
                for render_x in range(0,20):
                    try:
                        if game_map[render_z][render_y][render_x] != '0':
                            block_x = DISPLAY_W/2 + render_x * BLOCK_x + render_y * -BLOCK_y - scroll[0]
                            block_y = DISPLAY_H/2  + render_x * BLOCK_x + render_y * BLOCK_y - render_z * BLOCK_z - scroll[1]
                           
                            if game_map[render_z][render_y][render_x] == '1':
                                display.blit(block_image, (block_x,block_y))
                            if game_map[render_z][render_y][render_x] == '2':
                                display.blit(grass, (block_x,block_y))
                            if game_map[render_z][render_y][render_x] == '3':
                                display.blit(rock, (block_x,block_y))
                            if game_map[render_z][render_y][render_x] == '4':
                                display.blit(fire, (block_x,block_y))
                                if flametimer%11 == 0:
                                    light_radius = random.randint(10,12)
                                pygame.draw.circle(transparents, (255, 165, 0), (BLOCK_x+block_x, BLOCK_y+block_y), light_radius)
                        
                                particle_x = render_x * BLOCK_x + render_y * -BLOCK_y
                                particle_y = render_x * BLOCK_x + render_y * BLOCK_y - render_z * BLOCK_z

                                particles.append([[particle_x, particle_y], [random.randint(0,20)/10-1, random.randint(-4,-1)], random.randint(1,2)])
                               
                                if flametimer == 0:
                                    flame.append([[particle_x, particle_y], [0, -1], random.randint(1,3)])
                                    flametimer = 10
                                else:
                                    flametimer -= 1
                            
                    except:
                        pass

                    if render_x == player_coords[0] and render_z == player_coords[2]:
                        if render_y == player_coords[1]:
                            display.blit(player_img, (player.x, player.y))
                        elif render_y == 1+player_coords[1] and blit_slice:
                            display.blit(slices[slice], (player.x, player.y))
        
        x = player_rect.x * 1 + player_rect.y * -1 + 17
        y = player_rect.x * 1 + player_rect.y * 1  -39
        player.x = DISPLAY_W/2 + x - player.width - scroll[0]
        player.y = DISPLAY_W/2 + y - z - player.height - scroll [1]
     
                    
        
    """
    RENDERS PARTICLES
    """
    handle_particles(particles, smoketimer, (175,175,175))
    handle_particles(flame, smoketimer, (255, 165, 0)) 


    """
    COMBINES LAYERS AND UPDATES
    """
    display.blit(transparents,(0,0))
    surf = pygame.transform.scale(display, WINDOW_SIZE) 
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)  #stays at 60 fps 