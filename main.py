import pygame
import random
import math
from pygame import mixer

# intialise the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# bkg Music
mixer.music.load('background.wav')
mixer.music.play(-1)  # play on loop

# Title and icon
pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load()

# Line
Lineimg = pygame.image.load('Line2.png')
LineX = 0
LineY = 400

# Player
playerimg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(38)

# Bullet
# Ready:You cant see the bullet on screen

# fire:The bullet is visible
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def Line(x, y):
    screen.blit(Lineimg, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # Bcg image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # if key stroke is pressed whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                # Get the current X coordinate of spaceship
                fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    # Check for boundry
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    Line(LineX, LineY)
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
