# importing libraries
import pygame
import random
 
speed = 15
spawn_rate_constant=50
spawn_rate = spawn_rate_constant
 
# Window size
window_x = 720
window_y = 480
 
# defining colors
bgcolor = pygame.Color(23, 163, 91)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
 
# Initialising pygame
pygame.init()
 
# Initialise game window
pygame.display.set_caption('Life')
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
 
# defining snake default position
snake_position = [100, 50]
 
# food position
food_position = []
food_position.append([random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10])
 
 
# setting default snake direction towards
# right
direction = 'RIGHT'
 

def getState():
    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    for position in  food_position:
        if position[1]<snake_position[1] and position[0]<snake_position[0]:
            top_left += 1/((snake_position[1]-position[1])**2 + (snake_position[0]-position[0])**2)
        elif position[1]<snake_position[1] and position[0]>snake_position[0]:
            top_right += 1/((snake_position[1]-position[1])**2 + (snake_position[0]-position[0])**2)
        elif position[1]>snake_position[1] and position[0]<snake_position[0]:
            bottom_left += 1/((snake_position[1]-position[1])**2 + (snake_position[0]-position[0])**2)
        elif position[1]>snake_position[1] and position[0]>snake_position[0]:
            bottom_right += 1/((snake_position[1]-position[1])**2 + (snake_position[0]-position[0])**2)

    wall_top = 1/(snake_position[1]-0)**2
    wall_bottom = 1/(snake_position[1]-window_y)**2
    wall_left = 1/(snake_position[0]-0)**2
    wall_right = 1/(snake_position[0]-window_x)**2
    
    return [top_left,top_right,bottom_left,bottom_right,wall_top,wall_bottom,wall_left,wall_right]

def game_step(direction):
    global spawn_rate
    score = 0

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 8
    if direction == 'DOWN':
        snake_position[1] += 8
    if direction == 'LEFT':
        snake_position[0] -= 8
    if direction == 'RIGHT':
        snake_position[0] += 8
 
    # Snake body growing mechanism
    # if foods and snakes collide then scores
    # will be incremented by 8
    for i,position in enumerate(food_position):
        if (snake_position[0] - position[0])**2 + (snake_position[1] - position[1])**2 < 169:
            score += 10
            del(food_position[i])
            break
    
         
    if 100-spawn_rate<0:
        spawn_rate=spawn_rate_constant
        food_position.append([random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10])
    else:
        spawn_rate += 1
         
    
    game_window.fill(bgcolor)
     
    pygame.draw.circle(game_window, green,snake_position, 8)
    for position in food_position:
        pygame.draw.circle(game_window, white,position , 5)
 
    # Wall collide conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10 or snake_position[1] < 0 or snake_position[1] > window_y-10:
        score -= 10

 
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(speed)
    return score
