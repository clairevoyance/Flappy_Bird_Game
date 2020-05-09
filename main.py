import pygame
import sys
import random
from pygame.locals import *


def welcomeScreen():
    player_x = int(SCREENWIDTH / 5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    message_x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    message_y = int(SCREENHEIGHT * 0.13)
    base_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENHEIGHT / 2)
    base_x = 0
    # Create two pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]
    pipeVel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1

    player_flap_acc_vel = -8  # velocity while flapping
    player_flapped = False  # It is true only when the bird is flapping
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_flap_acc_vel
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)  # It will return True if Player has Crashed
        if crashTest:
            return

        # check for score
        player_mid_pos = player_x + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                GAME_SOUNDS['point'].play()

        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        player_y += min(player_vel_y, GROUND_Y - player_y - player_height)

        # moving the pipes to the left
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVel_x
            lowerpipe['x'] += pipeVel_x

        # Add a new pipe when the first pipe is about to cross the left part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if pipe is out of the screen, remove it!
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Blitting the Sprites now!
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        x_offset = (SCREENWIDTH - width) / 2
        for digit in my_digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (x_offset, SCREENHEIGHT * 0.12))
            x_offset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > GROUND_Y - 25 or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = int(SCREENHEIGHT / 3)
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},  # for upper pipe
        {'x': pipe_x, 'y': y2}  # for lower pipe
    ]
    return pipe


# initializing global variables for the game
SCREENWIDTH = 600
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
FPS = 32
PLAYER = 'Images_Audio_Sprites/Sprites/bird.png'
BACKGROUND = 'Images_Audio_Sprites/Sprites/background.png'
PIPE = 'Images_Audio_Sprites/Sprites/pipe.png'

if __name__ == '__main__':
    pygame.init()  # Initializes the different modules of pygame
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Abhishek Sahai", "FlappyBird")

    GAME_SPRITES['numbers'] = (
        pygame.image.load('Images_Audio_Sprites/Sprites/0.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/1.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/2.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/3.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/4.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/5.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/6.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/7.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/8.png').convert_alpha(),
        pygame.image.load('Images_Audio_Sprites/Sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('Images_Audio_Sprites/Sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Images_Audio_Sprites/Sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SOUNDS['die'] = pygame.mixer.Sound('Images_Audio_Sprites/Audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Images_Audio_Sprites/Audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Images_Audio_Sprites/Audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Images_Audio_Sprites/Audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Images_Audio_Sprites/Audio/wing.wav')

    while True:
        welcomeScreen()  # Shows Welcome Screen till the user doesn't press a button
        mainGame()  # Commences the Game when the user presses any button
