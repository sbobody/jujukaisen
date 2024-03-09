
import pgzrun
import random
import pygame
import os
import sys

from pygame.time import Clock



TITLE = "jujukaisen (другая история)"
FPS = 30
fs = 0

a = 160
b = 60

WIDTH = 1280
HEIGHT = 720

tiles = os.listdir('images/tiles/transparent')
tile = Actor("tiles/transparent/tile_0051.png")
mode = 'menu'
level = 1
ultra = 0
ultra_count = 60
menu = Actor ("меню.jpg")
fon = Actor ('фон.jpg')

coddy = Actor ('hakari_start',(580,500))
enemy = Actor ('kenjaku.png',(700,500))

coddy.hearts = 100
coddy.attack = 40
enemy.hearts = 200
enemy.attack = 20

enemies = [enemy]




game_map = []
for i in range(a):
    game_map.append([])
    for j in range(b):
        game_map[i].append(random.choice(tiles).split('.')[0])

def map_draw():
    for i in range(a):
        for j in range(b):
            #tile.image = "tiles/transparent/" + game_map[i][j]
            tile.left = j * 16
            tile.top = i * 16
            tile.draw()

def win_or_game_over():
    global mode, ultra_count, level, ultra
    if coddy.hearts <= 0:
        mode = 'menu'
        coddy.hearts = 100
        coddy.attack = 40
        enemy.hearts = 200
        enemy.attack = 20
        enemy.image = 'kenjaku'
        ultra_count = 60
    elif enemy.hearts <= 0:
        enemy.image = 'todji'
        coddy.hearts = 150
        coddy.attack = 50
        enemy.hearts = 250
        enemy.attack = 20
        ultra_count = 60
        coddy.image = 'original2'
        level = 2
        ultra = 0


def draw():
    global fs
    if fs == 0:
          screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
          fs = 1
    if mode == 'menu':
        menu.draw ()
        screen.draw.text ('начать игру (p)', pos = (580,60), fontsize= 40)

    elif mode == 'game':
        #map_draw()
        fon.draw()
        coddy.draw()
        screen.draw.text (str(coddy.hearts), pos = (coddy.x - 20,coddy.y - 150 ), fontsize= 40)
        enemy.draw()
        screen.draw.text (str(enemy.hearts), pos = (enemy.x - 20,enemy.y - 150 ), fontsize= 40)
        screen.draw.text (str(ultra_count), pos = (30, 30), fontsize= 40)

def enemy_walk():
    if enemy.x > coddy.x:
        enemy.x -= 1
    else:
        enemy.x += 1

def time_ult():
    global ultra_count, ultra
    if ultra_count < 60:
        ultra_count += 1
        if ultra_count == 60:
            ultra = 0



def ult ():
    global ultra, ultra_count
    if abs(coddy.x - enemy.x) < 300 and ultra == 0:
        enemy.hearts -= coddy.attack
        ultra = 1
        ultra_count = 0

clock.schedule_interval(time_ult, 1)

def update(dt):
    global mode
    win_or_game_over ()
    enemy_walk() 
    if keyboard.p and mode == 'menu':
        mode = 'game'

    elif keyboard.g and mode == 'game':
        mode = 'menu'
    elif keyboard.escape and mode == 'menu':
        sys.exit()

#Управление
    if (keyboard.left or keyboard.a):
        coddy.x = coddy.x - 5
        if level == 1:
            coddy.image = 'hakari_start'

    elif (keyboard.right or keyboard.d) :
        coddy.x = coddy.x + 5
        if level == 1:
            coddy.image = 'hakari_start_right'

    if keyboard.e :
        ult ()

     #Столкновение с врагами
    enemy_index = coddy.collidelist(enemies)
    if enemy_index != -1:
        enemy = enemies[enemy_index]
        enemy.hearts -= coddy.attack
        coddy.hearts -= enemy.attack
        if enemy.x > coddy.x:
            enemy.x += 200
            coddy.x -= 200
        else:
            coddy.x += 200
            enemy.x -= 200
    
    

def on_key_down(key):
    #Прыжок
    if (keyboard.up or keyboard.w) and coddy.y == 500:
        coddy.y = 150
        animate(coddy, tween = 'accelerate', duration = 1,y = 500)
        
 















os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()