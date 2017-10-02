import pygame
import random
import math

pygame.init()  # pygame
screenWidth = 800  # screen resolution variables (fully variable, no hardcode)
screenHight = 600
pixelWidth = screenWidth / 40  # pixel size (fully variable, no hardcode, amount of blocks in game)
pixelHight = screenHight / 30
white = (255,255,255) # colors
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((screenWidth,screenHight))  # start display
pygame.display.set_caption('slither')  # name display

def startGame():
    global lead_x,lead_y,lead_x_change,lead_y_change,state,appleX,appleY,snake_parts,snakeLength,snakeRot
    lead_x = screenWidth / 2  # start pos at center
    lead_y = screenHight / 2
    lead_x_change = 0
    lead_y_change = 0
    snakeRot = 0  # up
    snake_parts = [lead_x,lead_y]  # make firts snake part
    snakeLength = 3

    appleX = int(random.randrange(0,screenWidth,pixelWidth))
    appleY = int(random.randrange(0,screenHight,pixelHight))

    state = 'game running'

def gameTick():
    global lead_x,lead_y,snake_parts,snakeLength,state,appleX,appleY,snakeRot  # allow variables to be changed globally  http://www.python-course.eu/python3_global_vs_local_variables.php
    lead_x += lead_x_change  # movement
    lead_y += lead_y_change
    snake_parts += [lead_x,lead_y]  # add new snake part
    if appleX == lead_x and appleY == lead_y:  # add snake length
        snakeLength += 1
        appleX = int(random.randrange(0,screenWidth,pixelWidth))
        appleY = int(random.randrange(0,screenHight,pixelHight))
    if len(snake_parts) > snakeLength * 2:  # remove oldest snake part if needed
        del snake_parts[0]
        del snake_parts[0]
    if lead_x < 0 or lead_x >= screenWidth or lead_y < 0 or lead_y >= screenHight:  # check for snake out of screen
        state = 'start game'
    else:
        for a in range(round(len(snake_parts) / 2)):  # check for self-eating
            for b in range(round(len(snake_parts) / 2)):
                if a != b:
                    if snake_parts[a * 2] == snake_parts[b * 2] and snake_parts[a * 2 + 1] == snake_parts[b * 2 + 1]:
                        state = 'start game'
                    

clock = pygame.time.Clock()  # start clock for FPS

counter = 0

state = 'start game'

while True:  # game loop
    events = pygame.event.get()  # gets events
    for event in events:  # at all time event handler
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:  # quit
            pygame.quit()
            quit()
    if state == 'game running':
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snakeRot -= 1  # counter clock wise
                elif event.key == pygame.K_RIGHT:
                    snakeRot += 1  # clock wise
        snakeRot = snakeRot % 4
        if snakeRot == 3:
            lead_x_change = pixelWidth * -1  # X * -1 == makes X negative
            lead_y_change = 0
        elif snakeRot == 1:
            lead_x_change = pixelWidth
            lead_y_change = 0
        elif snakeRot == 0:
            lead_y_change = pixelHight * -1
            lead_x_change = 0
        elif snakeRot == 2:
            lead_y_change = pixelHight
            lead_x_change = 0
        if counter % round(snakeLength / 10 + 5) == 0:  # tick rate (longer snake = higher number after '%' = slower tickrate)
            gameTick()
        gameDisplay.fill(green)  # background
        pygame.draw.rect(gameDisplay, red, [appleX,appleY,pixelWidth,pixelHight])  # render apple
        for i in range(round(len(snake_parts) / 2)):  # render snake
            pygame.draw.rect(gameDisplay, blue, [snake_parts[i * 2],snake_parts[(i * 2) + 1],pixelWidth,pixelHight])
        pygame.display.update()  # update

    elif state == 'start game':
        startGame()

    clock.tick(60) # 60 fps limit
    counter += 1  # counter

pygame.quit()  # quit
quit()

