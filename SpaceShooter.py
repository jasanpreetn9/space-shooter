# red_text = GAME_FONT.render(f'HEALTH: {str(red_health)}', 1, RED)
# WINDOW.blit(red_text, (600, 10))

from time import sleep
import pygame
# import go at the top

pygame.font.init()

# variables
WINDOW = pygame.display.set_mode((1000, 600))
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MYCOLOR = (13, 17, 26)
SPACE = pygame.transform.scale(
    pygame.image.load("assets/space.png"), (1000, 600))
SPACESHIP_RED = pygame.transform.scale(
    pygame.image.load("assets/spaceship_red.png"), (50, 50))
SPACESHIP_YELLOW = pygame.transform.scale(
    pygame.image.load("assets/spaceship_red.png"), (50, 50))

VEL = 4
BULLET_VEL = 7
MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

GAME_FONT = pygame.font.Font("assets/Quicksand-Regular.ttf", 36)

# methods


def drawWindow(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WINDOW.blit(SPACE, (0, 0))
    WINDOW.blit(SPACESHIP_RED, (red.x, red.y))
    WINDOW.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))

    pygame.draw.rect(WINDOW, (255,255,255), pygame.Rect(475, 10, 100, 10)) #red_health_bar_outline
    pygame.draw.rect(WINDOW, RED, pygame.Rect(475, 10, red_health * 10, 10)) # red_health_bar
    pygame.draw.rect(WINDOW, (255,255,255), pygame.Rect(475, 580, 100, 10)) # yellow_health_bar_outline
    pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(475, 580, yellow_health * 10, 10)) # yellow_health_bar
    
    if yellow_health == 0:
        red_won = GAME_FONT.render(f'RED WON!', 1, RED, (255,255,255))
        WINDOW.blit(red_won, (30, 10))
        pygame.display.update()
        pygame.time.delay(5000)
        quit()
        
    if red_health == 0:
        yellow_won = GAME_FONT.render(f'YELLOW WON!', 1, YELLOW, (255,255,255))
        WINDOW.blit(yellow_won, (30, 10))
        pygame.display.update()
        pygame.time.delay(5000)
        quit()
        
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)


def bulletMovement(yellow, red, yellow_bullets, red_bullets):
    for bullet in yellow_bullets:
        bullet.y = bullet.y - BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        if bullet.y + bullet.height < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y = bullet.y + BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.y > WINDOW.get_height():
            red_bullets.remove(bullet)


def yellowMovement(keysPressed, yellow):
    if keysPressed[pygame.K_UP] and yellow.y - VEL > WINDOW.get_height() // 2:
        yellow.y -= VEL
    if keysPressed[pygame.K_DOWN] and yellow.y + VEL < WINDOW.get_height():
        yellow.y += VEL
    if keysPressed[pygame.K_LEFT] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keysPressed[pygame.K_RIGHT] and yellow.x + VEL < WINDOW.get_width():
        yellow.x += VEL


def redMovement(keysPressed, red):
    # Up
    if keysPressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    # Down
    if keysPressed[pygame.K_s] and red.y + VEL + 50 < WINDOW.get_height() // 2:
        red.y += VEL
    # left
    if keysPressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    # right
    if keysPressed[pygame.K_d] and red.x + VEL + 50 < WINDOW.get_width():
        red.x += VEL
    pass


def game():

    yellow = pygame.Rect(500, 400, 50, 50)  # runs once
    red = pygame.Rect(500, 40, 50, 50)  # runs once
    fps = pygame.time.Clock()  # clock class

    red_bullets = []
    yellow_bullets = []
    running = True

    yellow_health = 10
    red_health = 10

    while running:  # while the game is running
        fps.tick(60)  # update the FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width // 2 - 1, yellow.y, 3, 10)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width // 2 - 1, red.y + red.height - 5, 3, 10)
                    red_bullets.append(bullet)

            if event.type == YELLOW_HIT:
                if yellow_health > 0:
                    yellow_health -= 1

            if event.type == RED_HIT:
                if red_health > 0:
                    red_health -= 1

        keysPressed = pygame.key.get_pressed()  # get the keys pressed
        yellowMovement(keysPressed, yellow)  # move the yellow
        redMovement(keysPressed, red)  # move the red spaceship

        bulletMovement(yellow, red, yellow_bullets, red_bullets)

        drawWindow(yellow, red, yellow_bullets, red_bullets,
                   yellow_health, red_health)
        
        pygame.display.update()  # update the window


# main method
if __name__ == "__main__":
    pygame.init()  # initialize the pygame module
    pygame.display.set_caption("Space Shooter")  # set the window title
    pygame.display.set_icon(SPACESHIP_YELLOW)  # set the window icon
    game()
    pygame.quit()  # quit the pygame module

    