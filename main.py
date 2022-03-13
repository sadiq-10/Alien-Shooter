import pygame
import sys
import random
import math

from pygame.constants import KEYDOWN, K_RIGHT

#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800, 600))

#load background image
background = pygame.image.load('./images/background.jpg')

#title and icon
pygame.display.set_caption('Space Shooter')
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

#add player ship
playerImg = pygame.image.load('./images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

#add enemy ship
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 5

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(.3)
    enemyY_change.append(20)

#add bullet
bulletImg = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)



def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def bullet_enemy_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 20:
        return True


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


#game loop
while True:
    screen.fill((0,0,0))        #bg color
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #controlling the player ship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = .3
            if event.key == pygame.K_LEFT:
                playerX_change = -.3
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0



    # set the boundary for player and enemy
    #player ship movement constrain
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    #enemy ship movement 
    for i in range(num_of_enemy):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        #enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = .3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.3
            enemyY[i] += enemyY_change[i]
        #enemy bullet collision
        collision = bullet_enemy_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 200)
    
    
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    
    player(playerX, playerY)
    show_score(textX, textY)
    #display updateing
    pygame.display.update()