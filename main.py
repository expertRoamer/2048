import sys

import pygame

import random

import math

import os

pygame.init()

WIDTH = 600
HEIGHT = 600

TITLE_COLOR = (119,110,101)
BG_COLOR = (250,248,239)
GRID_BG_COLOR =  (187,173,160)
GRID_COLOR =  (205,193,180)
POINT_GRID_COLOR =  (143,122,102)
WHITE = (255,255,255)
PLAYER_ICON = (108,234,125)

FPS = 60
GRID_WIDTH = 5000 / 67

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
screen.fill((250,248,239))
pygame.display.set_caption('2048!')


running = True
initial = True
font_name = pygame.font.match_font('Yu Gothic UI Semibold')
clock = pygame.time.Clock()
transparency = 255
title_transparency_direction = False #True means transparency increase
level = 0 # 0:初始頁面 1:規則頁面 2:遊戲頁面 
score = 0
end = False

block_colors = [(238,228,218), (237,224,200), (242,177,121), (245,149,99), (246,124,95), (246,94,59), (237,207,114), (237,204,97), (228, 255, 90), (192, 157, 44), (250, 214, 10)]
num_colors = [(119,110,101), (119,110,101), (249,246,242), (255,255,255), (249,246,242), (249,246,242), (249,246,242),  (249,246,242), (249,246,242), (249,246,242), (249,246,242)]        
block_colors_norm = [(238,228,218), (237,224,200), (242,177,121), (245,149,99), (246,124,95), (246,94,59), (237,207,114), (237,204,97), (228, 255, 90), (192, 157, 44), (250, 214, 10)]
num_colors_norm = [(119,110,101), (119,110,101), (249,246,242), (255,255,255), (249,246,242), (249,246,242), (249,246,242),  (249,246,242), (249,246,242), (249,246,242), (249,246,242)]        
block_colors_blue = [(238,228,218), (149, 232, 255), (166, 234, 234), (88, 189, 189), (63, 238, 238), (17, 182, 255), (42, 154,201), (92, 112, 227), (21, 75, 162), (222, 151, 240), (142, 91, 154), (255, 28, 191)]
num_colors_blue = [(119,110,101), (119,110,101), (249,246,242), (255,255,255), (249,246,242), (249,246,242), (249,246,242),  (249,246,242), (249,246,242), (249,246,242), (249,246,242)]
origin_animation = []
origin_positionX_Y = []
speed = []

map = [[-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,0,-1,-1,-1]]
move_map = [[0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]]
player_I = 5
player_J = 2
moving_block_I = 0
moving_block_J = 0
current_direction = ""

gravity_time = 0
new_block_time = 120 #產生新方塊的時間間格

counter = 0 #計時器
player_gravity_time = 0
jumping = False

random_block_position = (0,0)

#初始化封面動畫
for i in range(5):
    origin_animation.append(random.randrange(0,len(block_colors), 1))
    origin_positionX_Y.append((random.randrange(0, 500, 5),random.randrange(-300, -55, 1)))
    speed.append(random.randrange(50, 300, 1) / 100)
    
def change_color():
    global block_colors
    global block_colors_norm
    global block_colors_blue
    if (block_colors[5] == block_colors_norm[5]):
        for i in range(11):
            block_colors[i] = block_colors_blue[i]
    else:
        for i in range(11):
            block_colors[i] = block_colors_norm[i]
            
def draw_text(surf, text, size, x, y, color, faded):
    global transparency
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)    
    text_rect = text_surface.get_rect() 
    text_rect.centerx = x
    text_rect.centery = y
    if (faded):
        text_surface.set_alpha(transparency)
    surf.blit(text_surface, text_rect)

def draw_rule(surf, text, size, c_x, c_y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)    
    text_rect = text_surface.get_rect() 
    text_rect.topleft = (c_x, c_y)
    surf.blit(text_surface, text_rect)

def animation():
    global speed
    for i in range(5):
        pygame.draw.rect(screen, block_colors[origin_animation[i]], [origin_positionX_Y[i][0], origin_positionX_Y[i][1], GRID_WIDTH, GRID_WIDTH], 0, 5)
        origin_positionX_Y[i] = (origin_positionX_Y[i][0], origin_positionX_Y[i][1] + speed[i])
        draw_text(screen, str(2 ** (origin_animation[i] + 1)), 30, origin_positionX_Y[i][0] + GRID_WIDTH / 2, origin_positionX_Y[i][1] + GRID_WIDTH / 2, num_colors[origin_animation[i]], False)
        if (origin_positionX_Y[i][1] > 600):
            origin_positionX_Y[i] = (random.randrange(0, 500, 5),random.randrange(-300, -55, 1))
            speed[i] = random.randrange(50, 300, 1) / 100
            origin_animation[i] = random.randrange(0,len(block_colors), 1)

def origin():
    global transparency
    global title_transparency_direction
    screen.fill(BG_COLOR)
    animation()
    draw_text(screen, "2048!", 100, WIDTH / 2, 100, TITLE_COLOR, False)
    draw_text(screen, "按任意鍵開始遊戲", 20, WIDTH / 2, 400, TITLE_COLOR, True)
    if (transparency < 0):
        title_transparency_direction = True
    elif (transparency > 255):
        title_transparency_direction = False
    if (title_transparency_direction):
        transparency += 5
    else:
        transparency -= 5
    
def rule():
    global transparency
    global title_transparency_direction
    screen.fill(BG_COLOR)
    draw_text(screen, "遊戲規則", 60, WIDTH / 2, 50, TITLE_COLOR, False)
    draw_rule(screen, "1.透過左、右、上(跳躍)鍵來控制你的\"角色\"(有綠色圓點)，可和相同數字的方塊合併", 15, 30, 120, TITLE_COLOR)
    draw_rule(screen, "2.預設角色為方塊2，且下落方塊恆為2", 15, 30, 160, TITLE_COLOR)
    draw_rule(screen, "3.方塊下落的速度恆定", 15,30, 200, TITLE_COLOR)
    draw_rule(screen, "4.按w鍵可以切換顏色", 15,30, 240, TITLE_COLOR)
    draw_rule(screen, "5.遊戲藏有特殊外掛鍵請自行發掘:)", 15,30, 280, TITLE_COLOR)
    draw_rule(screen, "6.按r鍵可重新開始", 15,30, 320, TITLE_COLOR)
    draw_rule(screen, "分數計算:", 25,30, 400, TITLE_COLOR)
    draw_rule(screen, "1.分數增加量為兩個合併方塊的數字和", 15,30, 440, TITLE_COLOR)
    draw_text(screen, "按任意鍵開始遊戲", 20, WIDTH / 2, 500, TITLE_COLOR, True)
    if (transparency < 0):
        title_transparency_direction = True
    elif (transparency > 255):
        title_transparency_direction = False
    if (title_transparency_direction):
        transparency += 5
    else:
        transparency -= 5

def clear(i):
    global map
    global player_I
    global player_J
    for j in range(6):
        if (not(j == player_J and i == player_I)):
            map[i][j] = -1
            
def secret():
    global map
    for i in range(6):
        for j in range(6):
            if (map[i][j] == -1):
                map[i][j] = 10
                
def draw_grid():
    global map
    color = GRID_COLOR
    pygame.draw.rect(screen, GRID_BG_COLOR, [50, 90,498,500], 0,5)
    pygame.draw.rect(screen, POINT_GRID_COLOR, [480, 10,70,70], 0,5) #記分區
    for i in range (6):
        for j in range (6):
            if (map[i][j] == -1):
                color = GRID_COLOR
                pygame.draw.rect(screen, color, [50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH),90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH), GRID_WIDTH,GRID_WIDTH], 0,5)
            elif (map[i][j] >= len(block_colors)):
                color = (43,30,19)
                pygame.draw.rect(screen, color, [50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH),90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH), GRID_WIDTH,GRID_WIDTH], 0,5)
                draw_text(screen, str(2 ** (map[i][j] + 1)), 26, 50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2, 90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2,  (249,246,242), False)
            else:
                color = block_colors[map[i][j]]
                pygame.draw.rect(screen, color, [50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH),90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH), GRID_WIDTH,GRID_WIDTH], 0,5)
                if (map[i][j] >= 9):
                    draw_text(screen, str(2 ** (map[i][j] + 1)), 26, 50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2, 90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2, num_colors[map[i][j]], False)
                else:
                    draw_text(screen, str(2 ** (map[i][j] + 1)), 35, 50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2, 90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH) + GRID_WIDTH / 2, num_colors[map[i][j]], False)
            if (i == player_I and j == player_J):
                pygame.draw.circle(screen, PLAYER_ICON, (50 + 0.1 * GRID_WIDTH + (j * 1.1 * GRID_WIDTH) + 3 * GRID_WIDTH / 4, 90 + 0.1 * GRID_WIDTH + (i * 1.1 * GRID_WIDTH) + GRID_WIDTH / 4), GRID_WIDTH / 10, 0)

def draw_game_text():
    global score
    draw_text(screen, "2048!", 50, 150, 50, TITLE_COLOR, False)
    draw_text(screen, "score", 20, 515, 18, WHITE, False)
    if (score <= 999):
        draw_text(screen, str(score), 35, 515, 50, WHITE, False)
    else:
        draw_text(screen, str(score), 26, 515, 50, WHITE, False)
    
def game():
    screen.fill(BG_COLOR)
    draw_grid()
    draw_game_text()
    
def can_Move(i, j, direction):
    global map
    global gravity_time
    global moving_block_I
    global moving_block_J
    if ((gravity_time < 2 or gravity_time > 28)):
        return False
    if (direction == "LEFT"):
        if (j == 0):
            return False
        elif (map[i][j] == map[i][j - 1]):
            moving_block_I = i
            moving_block_J = j
            return True
        elif (map[i][j - 1] == -1):
            moving_block_I = i
            moving_block_J = j
            return True
        else:
            return can_Move(i, j - 1,"LEFT") 
    
    elif (direction == "RIGHT"):
        if (j == 5):
            return False
        elif (map[i][j] == map[i][j + 1]):
            moving_block_I = i
            moving_block_J = j
            return True
        elif (map[i][j + 1] == -1):
            moving_block_I = i
            moving_block_J = j
            return True
        else:
            return can_Move(i, j + 1, "RIGHT") 
    
    elif (direction == "UP"):
        if (i == 0):
            return False
        elif (i < 5 and map[i + 1][j] == -1):
            return False
        elif (map[i - 1][j] == map[i][j] and map[i][j] != -1):
            moving_block_I = i
            moving_block_J = j
            return True
        elif (map[i - 1][j] == -1):
            moving_block_I = i
            moving_block_J = j
            return True
        else:
            return can_Move(i - 1, j , "UP")

def create_block(num, x, y):
    global map
    map[x][y] = num
    
def update_map(i, j, direction):
    global jumping
    global move_map
    global gravity_time
    global score
    global map
    global player_I
    global player_J
    gravity_time += 1

    if (jumping):
        jumping = False
        gravity_time = 0
    if (gravity_time == 30):
        gravity_time = 0
        for m in range(6):
            for n in range(6):
                if (m == 5):
                    move_map[m][n] = 0
                elif (map[m + 1][n] == -1):
                    move_map[m][n] = 1
                else: 
                    move_map[m][n] = 0
                    
        for n in range(6):
            for m in range(4, -1 ,-1):
                if (move_map[m][n]):
                    if (m == player_I and n == player_J):
                        player_I += 1
                    map[m + 1][n] = map[m][n]
                    map[m][n] = -1
                    if (m > 0):
                        move_map[m - 1][n] = 1
                elif (map[m + 1][n] == map[m][n] and map[m][n] != -1):
                    if (m == player_I and n == player_J):
                        player_I += 1
                    map[m + 1][n] += 1
                    score += 2 ** (map[m + 1][n] + 1)
                    map[m][n] = -1
                    if (m > 0):
                        move_map[m - 1][n] = 1
    if (direction == "LEFT"):
        if (map[i][j - 1] == -1):
            for k in range(j - 1, player_J, 1):
                map[i][k] = map[i][k + 1]
            map[i][player_J] = -1
        elif (map[i][j] == map[i][j - 1]):
            map[i][j - 1] += 1
            score += 2 ** (map[i][j - 1] + 1)
            for k in range(j, player_J, 1):
                map[i][k] = map[i][k + 1]
            map[i][player_J] = -1
        player_J -= 1
        
    elif (direction == "RIGHT"):
        if (map[i][j + 1] == -1):
            for k in range(j + 1, player_J, -1):
                map[i][k] = map[i][k - 1]
            map[i][player_J] = -1
        elif (map[i][j] == map[i][j + 1]):
            map[i][j + 1] += 1
            score += 2 ** (map[i][j + 1] + 1)
            for k in range(j, player_J, -1):
                map[i][k] = map[i][k - 1]
            map[i][player_J] = -1
        player_J += 1
        
    elif (direction == "UP"):  
        if (map[i][j] == map[i - 1][j] and map[i][j] != -1):
            map[i - 1][j] += 1
            map[i][j] = -1
            score += 2 ** (map[i -1][j] + 1)
            for k in range(i, player_I, 1):
                map[k][j] = map[k + 1][j]
                map[k + 1][j] = -1
        else:
            for k in range(i - 1, player_I, 1):
                map[k][j] = map[k + 1][j]
                map[k + 1][j] = -1
        map[player_I][player_J] = -1
        player_I -= 1
    


def new():
    global level
    global map
    global move_map
    global player_I
    global player_J
    global moving_block_I
    global moving_block_J
    global current_direction
    global gravity_time
    global new_block_time
    global counter
    global player_gravity_time
    global jumping
    global score
    
    level = 0
    map = [[-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,-1,-1,-1,-1], 
       [-1,-1,0,-1,-1,-1]]
    move_map = [[0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]]
    player_I = 5
    player_J = 2
    moving_block_I = 0
    moving_block_J = 0
    current_direction = ""

    gravity_time = 0
    new_block_time = 120 #產生新方塊的時間間格

    counter = 0 #計時器
    player_gravity_time = 0
    jumping = False
    score = 0
while running:
    clock.tick(60) #FPS = 60
    current_direction = "NONE"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit()
        if (event.type == pygame.KEYDOWN and level != 2):
            if (level == 0):
                level = 1
            elif (level == 1):
                level = 2
        elif (event.type == pygame.KEYDOWN and level == 2):
            if event.key == pygame.K_LEFT:
                if (can_Move(player_I, player_J, "LEFT")):
                    current_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                if (can_Move(player_I, player_J, "RIGHT")):
                    current_direction = "RIGHT"
            elif event.key == pygame.K_UP:
                if (can_Move(player_I, player_J, "UP")):
                    jumping = True
                    current_direction = "UP"
            elif event.key == pygame.K_q:
                secret()
            elif event.key == pygame.K_w:
                change_color()
            elif event.key == pygame.K_1:
                clear(0)
            elif event.key == pygame.K_2:
                clear(1)
            elif event.key == pygame.K_3:
                clear(2)
            elif event.key == pygame.K_4:
                clear(3)
            elif event.key == pygame.K_5:
                clear(4)
            elif event.key == pygame.K_6:
                clear(5)    
            elif event.key == pygame.K_r:
                new()          
    if (level == 2):
        update_map(moving_block_I, moving_block_J, current_direction)
    if (level == 0):
        origin()
    elif (level == 1):
        rule()
    elif (level == 2):
        game()
        if (counter % new_block_time == 0):
            random_block_position = (0,random.randrange(0,6,1))
            while(not(map[0][random_block_position[1]] == -1)):
                random_block_position = (0,random.randrange(0,6,1))
            create_block(random.randrange(0,1,1), random_block_position[0], random_block_position[1])
        counter += 1

    if (end):
        level = 3
    
    pygame.display.update()