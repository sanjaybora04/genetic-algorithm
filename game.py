# importing libraries
from model import NeuralNet
import pygame
import random
 
speed = 300
spawn_rate_constant=50
spawn_rate = spawn_rate_constant
 
# Window size
window_x = 1210
window_y = 610
 
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
bibits = [NeuralNet()]
 
# food position
food_position = []
food_position.append([random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10])
 

def getState(pos):
    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    for position in  food_position:
        if position[1]<pos[1] and position[0]<pos[0]:
            top_left += 1/((pos[1]-position[1])**2 + (pos[0]-position[0])**2)
        elif position[1]<pos[1] and position[0]>pos[0]:
            top_right += 1/((pos[1]-position[1])**2 + (pos[0]-position[0])**2)
        elif position[1]>pos[1] and position[0]<pos[0]:
            bottom_left += 1/((pos[1]-position[1])**2 + (pos[0]-position[0])**2)
        elif position[1]>pos[1] and position[0]>pos[0]:
            bottom_right += 1/((pos[1]-position[1])**2 + (pos[0]-position[0])**2)

    wall_top = 1/(pos[1]+1)**2
    wall_bottom = 1/(pos[1]-window_y+1)**2
    wall_left = 1/(pos[0]+1)**2
    wall_right = 1/(pos[0]-window_x+1)**2
    
    return [top_left,top_right,bottom_left,bottom_right,wall_top,wall_bottom,wall_left,wall_right]


while True:

    # Moving the bibits
    for bibit in bibits:
        pred = bibit.forward(getState(bibit.position))
        direction = 3
        temp = pred[direction]
        for i,p in enumerate(pred):
            if p>temp:
                direction = i
                temp = p
            
        if direction==0:
            bibit.position[1] -= 8
        elif direction==1:
            bibit.position[1] += 8
        elif direction==2:
            bibit.position[0] -= 8
        else:
            bibit.position[0] += 8
            
 
    # Snake body growing mechanism
    # if foods and snakes collide then scores
    # will be incremented by 8
    for bibit in bibits:
        for i,position in enumerate(food_position):
            if (bibit.position[0] - position[0])**2 + (bibit.position[1] - position[1])**2 < 169:
                bibit.score += 10
                bibit.idlestate = 300
                del(food_position[i])
                break
    
         
    if 100-spawn_rate<0:
        spawn_rate=spawn_rate_constant
        food_position.append([random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10])
    else:
        spawn_rate += 1
         
    
    game_window.fill(bgcolor)
    
    for bibit in bibits:
        pygame.draw.circle(game_window, green,bibit.position, 8)
    for position in food_position:
        pygame.draw.circle(game_window, white,position , 5)
    
    # Wall collide conditions
    print(len(bibits))
    deathnote = []
    for i,bibit in enumerate(bibits):
        if bibit.idlestate==0 or bibit.position[0] < 0 or bibit.position[0] > window_x-10 or bibit.position[1] < 0 or bibit.position[1] > window_y-10:
            bibit.score -= 10
            if len(bibits)<30:
                bibits.extend(bibit.mutate(((300-bibit.idlestate)/60)+1.5+bibit.score/10,mutation_power=0.001))
            deathnote.append(i)

    deathnote.reverse()
    for bibit in deathnote:
        del(bibits[bibit])

 
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(speed)


    for bibit in bibits:
        bibit.idlestate -=1