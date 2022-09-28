import pygame

from pygame import mixer
import random
import math

# Initialize pygame and get access to its functions
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))  # double brackets are used as the width and height of the screen
# are considered as tuples.
# Here the screen is opening for few seconds, so to keep it open for long, we need to use infinite loop.
# Every functionality in a pygame is called an event. Suppose moving the plane from one position to the other
# is an event.In the same way, quitting the pygame is also an event. So we need to put a function to quit the game so
# that we can stop the game whenever we like.

# All of the pygame's functionality should be before the running game code. Because all of its events come before closing
# pygame.

# Now we will change the title and icon of the game.
pygame.display.set_caption("Space fighter!")
pygame_icon = pygame.image.load('launch.png')
pygame.display.set_icon(pygame_icon)

# background
background_image = pygame.image.load('wepik-purple-space-stars-desktop-wallpaper-2022816-22550.png')

# uploading and setting the position of the player icon. x axis is width (800) y axis is height (600).
player_image = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 500
playerx_change = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
number_of_enemies = 4

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load('alien.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 100))
    enemyx_change.append(2)
    enemyy_change.append(40)

bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

text_x = 10
text_y = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 65)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 0, 128))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def player(x, y):  # introducing a method for uploading the icon.
    screen.blit(player_image, (x, y))  # blit stands for drawing. x and y are positions of the player and are tuples.


def enemy(x, y, i):  # introducing a method for uploading the icon.
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if (distance < 27):
        return True
    else:
        return False


running_game = True
while running_game:
    for event in pygame.event.get():  # pygame.event.get() is the function of getting access to the events.
        if event.type == pygame.QUIT:
            running_game = False

        # keystroke functions to control the movement of the spaceship.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -3
            if event.key == pygame.K_RIGHT:
                playerx_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    # Player movement
    player_x += playerx_change
    if (player_x <= 0):
        player_x = 0
    elif (
            player_x >= 736):  # 736 because the spaceship is 64 pixels so at the end of the screen it will occupy (800-736)=64 pixels.
        player_x = 736

    # Enemy movement
    for i in range(number_of_enemies):

        # Game over function
        if (enemy_y[i] > 200):
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        enemy_x[i] += enemyx_change[i]
        if (enemy_x[i] <= 0):
            enemyx_change[i] = 2
            enemy_y[i] += enemyy_change[i]
        elif (enemy_x[i] >= 736):
            enemyx_change[i] = -2
            enemy_y[i] += enemyy_change[i]

            # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 100)

        enemy(enemy_x[i], enemy_y[i], i)

    if (bullet_y <= 0):
        bullet_y = 480
        bullet_state = "ready"

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

    player(player_x, player_y)  # calling the function for the movement of the player in each direction.
    show_score(text_x, text_y)
    pygame.display.update()
    # in order to change the background of our window, we can use RGB which stands for Red,
    # green and blue. The shade of colour is in the range of 0 to 255. The code for this
    # background will be within the infinity loop as the background colour will appear as long
    # as the window remains open.

# pass is a statement used when there is no statements to put in a condition and it prevents from giving errors.
# we are not going to use pass as we want to close the screen whenever we want to quit the game.
