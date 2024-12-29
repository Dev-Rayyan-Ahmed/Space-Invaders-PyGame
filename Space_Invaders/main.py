import pygame
import random
from math import sqrt,pow,sin,radians #for Calculation
from pygame import mixer #to handle music

#Intialize the pygame
pygame.init()
#we use tuple to give arguments/parameters
screen = pygame.display.set_mode((800, 600))
running = True

#title and Game window:
pygame.display.set_caption(' Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#BackGround
background = pygame.image.load('background.jpg')

#BackGround Music:
mixer.music.load('background.wav')
mixer.music.play(-1) # -1 argument to loop the music

#mixer.music.load is for such music which is long like BGM
#but for small sounds like, Bullet-Fire we use mixer.sound

#Player
PlayerIMG = pygame.image.load('player.png')
PlayerX = 360
PlayerY = 480
PlayerX_change = 0
Player_angle = 0

#Enemy -- List for Multiple enemies
EnemyIMG = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change =[]
Enemy_angle = 0
No_of_enemies = 6

#Append Value For each
for i in range(No_of_enemies):
    EnemyIMG.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(8,730 ))
    EnemyY.append(random.randint(50,150))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)


#Bullet
# Ready = You can't see bullet on the Screen
# Fire = The Bullet is currently moving

BulletIMG = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 0.9
Bullet_state = "ready"

# SCORE
#for custom font, paste downloaded font in the main-Directory with .ttf extension
#Download it from DaFont.com
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) #Creating a Font for our Score test
textX = 10
textY = 10

#Game Over;
Over_font = pygame.font.Font('freesansbold.ttf', 64)
retry_font = pygame.font.Font('freesansbold.ttf', 45)

def Show_game_over():
    over = Over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over, (200,240))

    retry = retry_font.render('Press "R" to Restart.', True, (255, 255, 255))
    screen.blit(retry, (180,304))


def show_score(x,y):
    #first we render the text in order to blit it ( to draw it )
    score = font.render("Score: " + str(score_value),True,(255,255,255)) #ture is that to show on screen
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(PlayerIMG, (x, y)) #blit basically means to draw on the surface,surface is the screen area.

def enemy(x,y,i):
    screen.blit(EnemyIMG[i], (x, y))  # blit basically means to draw on the surface,surface is the screen area.

def fire_bullet(x,y):
    global Bullet_state
    Bullet_state = "fire" # Change Bullet State to "fire".
    screen.blit(BulletIMG, (x+16, y+10))  # blit basically means to draw on the surface,surface is the screen area.

def isCollision(EnemyX,EnemyY,BulletX,BulletY):
    distance = sqrt(pow(EnemyX-BulletX,2)+pow(EnemyY-BulletY,2))
    if distance <= 27:
        return True
    else:
        return False

def restart_game():
    global PlayerX, PlayerY, PlayerX_change, BulletX, BulletY, Bullet_state, score_value
    global EnemyX, EnemyY, EnemyX_change, EnemyY_change, Enemy_angle

    # Reset Player
    PlayerX = 360
    PlayerY = 480
    PlayerX_change = 0

    # Reset Bullet
    BulletX = 0
    BulletY = 480
    Bullet_state = "ready"

    # Reset Score
    score_value = 0

    # Reset Enemies
    for i in range(No_of_enemies):
        EnemyX[i] = random.randint(8, 730)
        EnemyY[i] = random.randint(50, 150)
        EnemyX_change[i] = 0.3
        EnemyY_change[i] = 40
    Enemy_angle = 0


#GameLoop
while running:
    # anything we want to change in our game, that should be with-in [While running] loop

    #changing BG by using RGB Colors
    screen.fill((0, 0, 0)) #we use tuple to give arguments

    #Add Background to our game
    screen.blit(background, (0, 0))

    for event in pygame.event.get(): #if we want to add more Events functions
                                     #we do it by adding them in this event loop
        if event.type == pygame.QUIT:#like for instance, arrow key to move
            running = False

        #If Keystroke is pressed checking whether it's left OR right
        #Pygame.KEYDOWN is an event for all Keys, whenever a Key is pressed; it's triggered

        if event.type == pygame.KEYDOWN: #event.type is to check which type of event
            if event.key == pygame.K_LEFT: #event.key is to check which key

                # print("Left Arrow")
                PlayerX_change = -0.3

            if event.key == pygame.K_RIGHT:
                # print("Right Arrow")
                PlayerX_change = 0.3

            if event.key == pygame.K_SPACE: #Fire Bullet when SPACE key is pressed
                if Bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav') #play sound when bullet is fired
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX,BulletY)

            if event.key == pygame.K_r:
                # print("Restart")
                restart_game()

        #pygame.KEYUP is an event when pressure is removed from a key, like after pressing and then removing press
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke Released")
                PlayerX_change = 0

    PlayerX += PlayerX_change #change Player's Position

    #setting border for our SpaceShip (Player)
    if PlayerX <= 6: # not 0 ; to make it not look like it's sticking to border,
        PlayerX = 6
    elif PlayerX >= 730: # 736 because 800-64 is 736; where -64 is for image width (64px) [64x64]
                         # but Subtracting more to make it look good
        PlayerX = 730

# Handling Multiple Enemies:
    if score_value == 20:
        No_of_enemies = 10
        for i in range(No_of_enemies):
            EnemyIMG.append(pygame.image.load('enemy.png'))
            EnemyX.append(random.randint(8, 730))
            EnemyY.append(random.randint(50, 150))
            EnemyX_change.append(0.3)
            EnemyY_change.append(40)
            BulletY_change = 1.5

    for i in range(No_of_enemies):

        #Game Over:
        if EnemyY[i] > 440:
            for j in range(No_of_enemies):
                EnemyY[j] = 2000   #Move All enemies Out of Screen Display
            Show_game_over()

        #Setting Border + Movement for our Enemies
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <=6:
            EnemyX_change[i] = 0.3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 730:
            EnemyX_change[i] = -0.3
            EnemyY[i] += EnemyY_change[i]

        #Checking Collision for Every Enemy
        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            BulletY = 480  # reset Bullet
            score_value += 1  # increase Score
            Bullet_state = "ready"  # Reset Bullet state to fire more

            #Play sound when enemy dies
            explosion_sound = mixer.Sound('explosion.wav')  # play sound when bullet is fired
            explosion_sound.play()
            # Spawn New Enemy
            EnemyX[i] = random.randint(8, 730)
            EnemyY[i] = random.randint(50, 150)

        #Deploy all Enemies
        EnemyY[i] += (sin(radians(Enemy_angle)))/7
        Enemy_angle +=0.2
        if Enemy_angle > 360:
            Enemy_angle = 0

        enemy(EnemyX[i], EnemyY[i],i)

    #Bullet Movement
    #multi-bullets
    if BulletY <=0:
        BulletY = 480
        Bullet_state = "ready"

    #move bullet across y-axis
    if Bullet_state == "fire":
        fire_bullet(BulletX,BulletY)
        BulletY -= BulletY_change

    #Flaoting the Player-Ship
    PlayerY += sin(radians(Player_angle))/20
    # PlayerX += math.sin(math.radians(Player_angle))/20
    Player_angle += 0.3
    if Player_angle > 360:
        Player_angle = 0

    show_score(textX, textY)
    player(PlayerX,PlayerY) #Calling the Player Function, and Drawing it at the center
    pygame.display.update() # need this always to update the display!
