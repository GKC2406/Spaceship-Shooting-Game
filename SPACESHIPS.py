import pygame
import os
from pygame import time
from pygame import display

from pygame.version import PygameVersion      #Helps to define the path to the spaceships images 
pygame.font.init()      #Initializes the pygame font library
pygame.mixer.init()     #Initializes Sound Effect Library


WIDTH,HEIGHT=900,500
WIN= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)



BORDER=pygame.Rect(WIDTH//2-5,0, 10,HEIGHT)        

BULLET_HIT_SOUND= pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND= pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT=pygame.font.SysFont('comicsans',40)     #Defining the font
WINNER_FONT=pygame.font.SysFont('comicsans',100)

FPS=60      #FRAMES PER SECOND 'how quickly our game to update'
VEL=5
BULLET_VEL=7
MAX_BULLETS=5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT=55,40

YELLOW_HIT=pygame.USEREVENT+1           #This represents the code/number for a CUSTOM USER EVENT (out of multiple user events) unique event ID
RED_HIT=pygame.USEREVENT+2              #Now we have defined 2 separate USER EVENTS & if we have done +1 in both they would become same event because they would have same underlying number representing them.so in sequence done +2


#Below images get loaded by pygame are known as SURFACES
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
#YELLOW_SPACESHIP=pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))  this scaleup the yellow spaceship image according to given parametres
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)
#Above will rotate the image by 90 degress


RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
#RED_SPACESHIP=pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))  this scaleups the red spaceship image acccording to given parameters
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)
#Above will rotate the image by 270 degress


SPACE=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH, HEIGHT))

def draw_window(red,yellow,red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill((WHITE))     #for filling background & if we don't draw the white background the pygame keeps on drawing and it does not remove the last drawing
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, BLACK,BORDER)        #For drawing rectangle on the window with Arguments with this specific pygame function is the WINDOW/SURFACE with drawing
    
    red_health_text= HEALTH_FONT.render("Health: "+ str(red_health),1, WHITE)       #We will use this font to render some text, 1 for ANTI-ALIASING, then COLOR of the text
    yellow_health_text= HEALTH_FONT.render("Health: "+ str(yellow_health),1, WHITE)

    WIN.blit(red_health_text,(WIDTH- red_health_text.get_width()-10, 10))        
    
    WIN.blit(yellow_health_text,(10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))     
    
    WIN.blit(RED_SPACESHIP, (red.x,red.y))

    #DRAWING BULLETS
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()




def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:   
        yellow.x-=VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL+ yellow.width<BORDER.x+20:   
        yellow.x+=VEL

    if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
        yellow.y-=VEL

    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-20: 
        yellow.y+=VEL
    




def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x + BORDER.width:
        red.x-=VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL+ red.width<WIDTH+20:    
        red.x+=VEL

    if keys_pressed[pygame.K_UP] and red.y-VEL>0:
        red.y-=VEL

    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height<HEIGHT-20:
        red.y+=VEL




def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    #MOVE THE BULLETS, HANDLE COLLISION OF THE BULLETS & HANDLE REMOVING OF THE BULLETS THAT GO OFF-SCREEN OR COLLIDE WITH CHARACTER
    for bullet in yellow_bullets:       
        bullet.x+=BULLET_VEL            #First will move the bullets,
        if red.colliderect(bullet):      
            pygame.event.post(pygame.event.Event(RED_HIT))            
            yellow_bullets.remove(bullet)       #Bullet collided & we removed it
        elif bullet.x> WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:       
        bullet.x-=BULLET_VEL            #First will move the bullets,
        if yellow.colliderect(bullet):      
            pygame.event.post(pygame.event.Event(YELLOW_HIT))            
            red_bullets.remove(bullet)       #Bullet collided & we removed it
        elif bullet.x< 0:
            red_bullets.remove(bullet)


def draw_winner(text):      #CALL THIS FUNCTION WHEN SOMEONE WINS
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2 -draw_text.get_width()/2, HEIGHT/2- draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000*5)        #Pause the Game for 5 seconds show this Text and restart immediately after

def main():
    '''
    Rect has 4 parameters:
    Rect(LEFT,TOP,WIDTH,HEIGHT)
    Also Rect(pos,size)
    Rect(x away from y-axis ,y of top corner of rectangle, length of rectangle, breadth of the rectangle)'''
    red=pygame.Rect(700,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)       #defining position/Coordinates of rectangle that represents red spaceship
    yellow=pygame.Rect(100,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)       # yellow is a pygame rectangle

    #EACH PLAYER SHOULD HAVE FINITE NUMBER OF BULLETS
    red_bullets=[]        #PROJECTILE MOTION
    yellow_bullets=[]

    red_health=10
    yellow_health=10
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)    #for controlling the speed of while loop and makes our game controllable
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y +yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x ,red.y +red.height//2 -2, 10, 5)
                    #We haven't added red.width since the RED spaceship(on right) is facing Towards the LEFT so it's bullets moving towards (0,0) which means we want bullets to come out from the Left side of image not the Right side
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            #BOTH CHARACTERS WILL HAVE FINITE NUMBER OF HEALTHS
            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()
            
            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

        winner_text=""
        if red_health<=0:
            winner_text="YELLOW WINS"
        if yellow_health<=0:
            winner_text="RED WINS"
        if winner_text!="":        #If either the RED or YELLOW player has losti.e. ZERO health, then we will set something other than EMPTY STRING
            draw_winner(winner_text)    #DRAW THE WINNER TEXT on Screen & will pause for 5 SECONDS & then break and then pygame.quit() QUITS the game
            break


        #We are going to make controllers 'AWSD' for left yellow spaceship and 'ARROWKEYS' for right red spaceship
        #Below method allows u to press multiple keys at the same time
        
        keys_pressed=pygame.key.get_pressed()    
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow, red)


        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
    pygame.quit()
    

#To RESTART the Game: since the main function not consists of any Game SPECIFIC VARIABLES, so when we recall the main function it will REDEFINE THESE VARIABLES in Game, then Game Restarts

if (__name__=="__main__"):
    main()