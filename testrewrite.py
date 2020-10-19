# -*- coding: utf-8 -*-
import pygame
import time
import math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

WIDTH:int = 640
HEIGHT:int = 480
FPS:float = 60
SPEED:float = .05
ROTSPEED:float = .025

MAPWIDTH:int  = 24
MAPHEIGHT:int = 24

WORLDMAP = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def color(c):
    return {
        1 : (255, 0, 0),
        2 : (0, 255, 0),
        3 : (0, 0, 255),
        4 : (255, 255, 255)
        }.get(c, (255, 255, 0))

def dcolor(c):
    return{
        1 : (127, 0, 0),
        2 : (0, 127, 0),
        3 : (0, 0, 127),
        4 : (127, 127, 127)
        }.get(c, (127, 127, 0))

def angle(a):
    return{
        -1 : math.cos(-ROTSPEED),
        -2 : math.sin(-ROTSPEED),
        1 : math.cos(ROTSPEED),
        2 : math.sin(ROTSPEED)
        }.get(a, None)

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycast Render Test")

posX:float = 22
posY:float = 12
dirX:float = -1
dirY:float = 0
planeX:float = 0
planeY:float = 0.66

done = False



while not done:
    
    pygame.mouse.set_visible(False)
    #pygame.mouse.set_pos(WIDTH/2, HEIGHT/2)
    pygame.event.set_grab(True)
    
    event = pygame.event.poll()
    
    if event.type == pygame.QUIT:
        done = True
    
    displaysurface.fill((0,0,0))
    
    for x in range(WIDTH):
        camX:float = 2.0 * x / WIDTH - 1
        raydirX:float = dirX + planeX * camX
        raydirY:float = dirY + planeY * camX
        
        mapX:int = int(posX)
        mapY:int = int(posY)
        
        sidedistX:float = 0
        sidedistY:float = 0
        
        deltadistX:float = 0
        if raydirX == 0:
            deltadistX = 1
        elif not raydirY == 0:
            deltadistX = abs(1 /raydirX)
            
        deltadistY:float = 0
        if raydirY == 0:
            deltadistY = 1
        elif not raydirX == 0:
            deltadistY = abs(1 / raydirY)
       
        perpwalldist:float = 0
        
        stepX:int = 0
        stepY:int = 0
        
        hit:int = 0
        side:int = 0
        
        if raydirX < 0:
            stepX = -1
            sidedistX = (posX - mapX) * deltadistX
        else:
            stepX = 1
            sidedistX = (mapX + 1.0 - posX) * deltadistX
            
        if raydirY < 0:
            stepY = -1
            sidedistY = (posY - mapY) * deltadistY
        else:
            stepY = 1
            sidedistY = (mapY + 1.0 - posY) * deltadistY
            
        while hit == 0:
            if sidedistX < sidedistY:
                sidedistX += deltadistX
                mapX += stepX
                side = 0
            else:
                sidedistY += deltadistY
                mapY += stepY
                side = 1
            
            if WORLDMAP[mapX][mapY] > 0:
                hit = 1
        
        if side == 0:
            perpwalldist = (mapX - posX + (1 - stepX) / 2) / raydirX
        else:
            perpwalldist = (mapY - posY + (1 - stepY) / 2) / raydirY
            
        if perpwalldist <= 0:
            perpwalldist = 1
            
        lineheight:int = HEIGHT / perpwalldist
        
        drawstart:int = -lineheight / 2 + HEIGHT / 2
        if drawstart < 0:
            drawstart = 0
            
        drawend:int = lineheight / 2 + HEIGHT / 2
        if drawend >= HEIGHT:
            drawend = HEIGHT - 1
            
        c = color(WORLDMAP[mapX][mapY])
        if side:
            c = dcolor(WORLDMAP[mapX][mapY])
        
        pygame.draw.line(displaysurface, c, (x, drawstart), (x, drawend))
    pygame.display.flip()
    
    pressed_keys = pygame.key.get_pressed()
    
    delta_mouse_x, delta_mouse_y = pygame.mouse.get_rel()
    
    if pressed_keys[K_w]:
        if not WORLDMAP[int(posX + dirX * SPEED)][int(posY)]:
            posX += dirX * SPEED
        if not WORLDMAP[int(posX)][int(posY + dirY * SPEED)]:
            posY += dirY * SPEED
    elif pressed_keys[K_s]:
        if not WORLDMAP[int(posX - dirX * SPEED)][int(posY)]:
            posX -= dirX * SPEED
        if not WORLDMAP[int(posX)][int(posY - dirY * SPEED)]:
            posY -= dirY * SPEED
            
    if delta_mouse_x < 0:
        olddirX:float = dirX
        dirX = planeY * angle(-1) - dirY * angle(-2)
        dirY = olddirX * angle(-2) + dirY * angle(-1)
        oldplaneX:float = planeX
        planeX = planeX * angle(-1) - planeY * angle(-2)
        planeY = oldplaneX * angle(-2) + planeY * angle(-1)
    elif delta_mouse_x > 0:
        olddirX:float = dirX
        dirX = dirX * angle(1) - dirY * angle(2)
        dirY = olddirX * angle(2) + dirY * angle(1)
        oldplaneX:float = planeX
        planeX = planeX * angle(1) - planeY * angle(2)
        planeY = oldplaneX * angle(2) + planeY * angle(1)
            
    if pressed_keys[K_ESCAPE]:
        done = True
pygame.quit()