import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# BackGround
background = pygame.image.load('2471.jpg')
#Background Sound
mixer.music.load('ImperialMarch60.wav')
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_Change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 765))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(3.5)
    enemyY_Change.append(20)

# Bullet
# Ready- You  can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 5
bullet_state = "ready"

# score
score_value=0
font = pygame.font.Font('budmo jigglish.ttf',70)

testX=10
testY=10

# Game over text
over_font=pygame.font.Font("budmo jiggler.ttf",100)


def game_over_text():
    over_text=over_font.render("GAME OVER  ",True,(255,155,155))
    screen.blit(over_text,(160,250))

def show_Score(x,y):
    score=font.render("Score :" + str(score_value),True,((255, 255, 153)))
    screen.blit(score, (x,y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 5, y + 10))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # playerY-=0.1

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            print("A Keystroke is pressed")
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_Change = -4
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_Change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('Gun+Silencer.wav')
                    bullet_sound.play()
                    # get the current cordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Keyword has been released")
                playerX_Change = 0

    # RGB - Red, Green ,Blue
    screen.fill((100, 50, 255))
    # backgound image
    screen.blit(background, (0, 0))

    # player movement
    playerX += playerX_Change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 766:
        playerX = 766

    # enemy movemnent

    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i]>460:
            for j in range (num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 3.5
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 766:
            enemyX_Change[i] = -3.5
            enemyY[i] += enemyY_Change[i]

    # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sasa1.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+= 1
            enemyX[i] = random.randint(0, 765)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_Score(testX,testY)
    pygame.display.update()
