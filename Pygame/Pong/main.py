import pygame
import random

#initalizing pygame
pygame.init()
clock = pygame.time.Clock()

#initializing the screen and screen background image
screen = pygame.display.set_mode((900, 700))
screenBackground = pygame.image.load("img/background.png")

#sprite groups
enemy = pygame.sprite.Group()
sprites = pygame.sprite.Group()
ball = pygame.sprite.Group()
buttons = pygame.sprite.Group()
playertwo_group = pygame.sprite.Group()

#initalizing fonts
textFont = pygame.font.Font("BittypixMonospace-3gAG.ttf", 60)
buttonFont = pygame.font.Font("BittypixMonospace-3gAG.ttf", 90)

#text for PONG title
titleText = buttonFont.render("PONG", False, (255, 255, 255))


#player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        self.image = pygame.Surface((30, 150))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

    #player update function
    def update(self):
        keys = pygame.key.get_pressed()

        #player movement and stopping player at screen borders
        if self.rect.y <= 0:
            if keys[pygame.K_s]:
                self.rect.y += 10
        if self.rect.y >= 540:
            if keys[pygame.K_w]:
                self.rect.y -= 10
        if self.rect.y >= 0 and self.rect.y <= 540:
            if keys[pygame.K_w]:
                self.rect.y -= 10
            if keys[pygame.K_s]:
                self.rect.y += 10

#second player class
class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        self.image = pygame.Surface((30, 150))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

    #second player update function
    def update(self):
        keys = pygame.key.get_pressed()

        #player movement but stopping at screen borders
        if self.rect.y <= 0:
            if keys[pygame.K_DOWN]:
                self.rect.y += 10
        if self.rect.y >= 540:
            if keys[pygame.K_UP]:
                self.rect.y -= 10
        if self.rect.y >= 0 and self.rect.y <= 540:
            if keys[pygame.K_UP]:
                self.rect.y -= 10
            if keys[pygame.K_DOWN]:
                self.rect.y += 10

#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed):
        super().__init__()

        self.image = pygame.Surface((30, 150))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        
        self.momentum = "up"

        self.speed = speed

#ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y, x_speed, y_speed, resetTicks):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.originalResetTicks = resetTicks
        self.resetTicks = resetTicks

        self.reset = True

    #function for moving pong ball in a random direction when the ball resets
    def randomMomentum(self):
        randomXMomentum = random.randrange(1, 3) 
        randomYMomentum = random.randrange(1, 3) 

        if randomXMomentum == 1:
            self.x_momentum = "left"
        if randomXMomentum == 2:
            self.x_momentum = "right"
        if randomYMomentum == 1:
            self.y_momentum = "up"
        if randomYMomentum == 2:
            self.y_momentum = "down"

    #ball update function
    def update(self):

        #if the pong ball resets
        if self.reset == True:
            #resetting pong balls position
            self.rect.x, self.rect.y = 435, 350
            self.resetTicks -= 1

            #moving after a time when reset
            if self.resetTicks < 0:
                self.randomMomentum()
                self.reset = False
                self.resetTicks = self.originalResetTicks

        #all updates if the pong ball isn't reset
        if self.reset == False:
            
            #changing momementum direction based on collision with screen borders
            if self.rect.y >= 670:
                self.y_momentum = "up"
            if self.rect.y <= 0:
                self.y_momentum = "down"

            #moving based on momentum
            if self.x_momentum == "left":
                self.rect.x -= self.x_speed
            if self.x_momentum == "right":
                self.rect.x += self.x_speed
            if self.y_momentum == "up":
                self.rect.y -= self.y_speed
            if self.y_momentum == "down":
                self.rect.y += self.y_speed

#button class
class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text=""):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.text = text

    #button update function
    def update(self):
        #blitting text to its own image
        self.image.blit(buttonFont.render(self.text, False, (0, 0, 0)), (40, 60))


#player, playerTwo paddle, AI paddle, and pong ball
player = Player((255, 255, 255), 30, 100)
sprites.add(player)

enemyPaddle = Enemy((255, 255, 255), 840, 100, 20)
enemy.add(enemyPaddle)

pongBall = Ball((255, 255, 255), 435, 350, 5, 5, 120)
ball.add(pongBall) 
pongBall.randomMomentum()

playerTwo = PlayerTwo((255, 255, 255), 840, 100)
playertwo_group.add(playerTwo)

#enemy and player scores
playerScore = 0
enemyScore = 0

#the text for the scores
playerScoreText = textFont.render(str(playerScore), False, (255, 255, 255))
enemyScoreText = textFont.render(str(enemyScore), False, (255, 255, 255))


#buttons on the title screen
AIButton = Button((255, 255, 255), 100, 200, 250, 200, "AI")
buttons.add(AIButton)

TwoPlayerButton = Button((255, 255, 255), 550, 200, 250, 200, "2P")
buttons.add(TwoPlayerButton)


#bools for seeing which game is chosen
AIGameStarted = False 
TwoPlayerGameStarted = False

#main function
running = True
while running:
    
    #quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #all functions for if the player chooses AI option
    if AIGameStarted == True:

	#moving the AI paddle based on the pong balls position. Also stops AI paddle from passing the screen borders
        if pongBall.rect.y <= 75:
            enemyPaddle.rect.y = 0
        if pongBall.rect.y >= 625:
            enemyPaddle.rect.y = 560
        if pongBall.rect.y <= 625 and pongBall.rect.y >= 75:
            enemyPaddle.rect.y = pongBall.rect.y-75
        
        #collision between player paddle and pong ball and specifics
        if pygame.sprite.spritecollide(pongBall, sprites, False):
            randomBallSpeedX = random.uniform(0.5, 2)
            randomBallSpeedY = random.uniform(0.5, 2)
            
            pongBall.x_speed += randomBallSpeedX
            pongBall.y_speed += randomBallSpeedY

            pongBall.x_speed += 0.5
            pongBall.y_speed += 0.5

            pongBall.x_momentum = "right"


        #colliision between enemy paddle and pong ball and specifics
        if pygame.sprite.spritecollide(pongBall, enemy, False):
            randomBallSpeedX = random.uniform(0.5, 2)
            randomBallSpeedY = random.uniform(0.5, 2)
            
            pongBall.x_speed += randomBallSpeedX
            pongBall.y_speed += randomBallSpeedY

            pongBall.x_speed += 0.5
            pongBall.y_speed += 0.5

            pongBall.x_momentum = "left"

        #resetting pong ball and speed and increasing scores when the pong ball touches outer walls
        if pongBall.rect.x <= 0:
            pongBall.x_speed = 5
            pongBall.y_speed = 5
            pongBall.reset = True

        if pongBall.rect.x >= 900:
            pongBall.x_speed = 5
            pongBall.y_speed = 5
            pongBall.reset = True

        #updating enemy, player, and ball
        enemy.update()
        sprites.update()
        ball.update()

        #blitting background image
        screen.blit(screenBackground, (0, 0))

        #drawing sprites
        enemy.draw(screen)
        sprites.draw(screen)
        ball.draw(screen)

    #update functions for if the player chooses the 2 player option
    if TwoPlayerGameStarted == True:

        #collision between pong ball and player with specifics
        if pygame.sprite.spritecollide(pongBall, sprites, False):
            randomBallSpeedX = random.uniform(0.5, 2)
            randomBallSpeedY = random.uniform(0.5, 2)
            
            pongBall.x_speed += randomBallSpeedX
            pongBall.y_speed += randomBallSpeedY

            pongBall.x_momentum = "right"


        #collision between player 2 and pong ball with specifics
        if pygame.sprite.spritecollide(pongBall, playertwo_group, False):
            randomBallSpeedX = random.uniform(0.5, 2)
            randomBallSpeedY = random.uniform(0.5, 2)
            
            pongBall.x_speed += randomBallSpeedX
            pongBall.y_speed += randomBallSpeedY

            pongBall.x_momentum = "left"


        #resetting pong ball and speed and increasing scores when the pong ball touches outer walls
        if pongBall.rect.x <= 0:
            enemyScore += 1
            enemyScoreText = textFont.render(str(enemyScore), False, (255, 255, 255))
            pongBall.x_speed = 5
            pongBall.y_speed = 5
            pongBall.reset = True
        if pongBall.rect.x >= 900:
            playerScore += 1
            pongBall.x_speed = 5
            pongBall.y_speed = 5
            playerScoreText = textFont.render(str(playerScore), False, (255, 255, 255))
            pongBall.reset = True

        #updating sprites
        ball.update()
        sprites.update()
        playertwo_group.update()

        #blitting background
        screen.blit(screenBackground, (0, 0))

        #blitting score texts
        screen.blit(playerScoreText, (300, 100))
        screen.blit(enemyScoreText, (550, 100))

        #drawing sprites to screen
        ball.draw(screen)
        sprites.draw(screen)
        playertwo_group.draw(screen)
        
    #title screen update functions
    if AIGameStarted == False and TwoPlayerGameStarted == False:
        
        #checking to see if the mouse clicks on the AI option
        if AIButton.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                AIGameStarted = True

        #checking to see if the mouse clicks on the AI option
        if TwoPlayerButton.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                TwoPlayerGameStarted = True
        

        #updating buttons
        buttons.update()

        #filling screen so it's different from the game background
        screen.fill((45, 45, 45))

        #blitting the title text and drawing buttons to screen
        screen.blit(titleText, (285, 50))
        buttons.draw(screen)

    #60 FPS and updating screen
    pygame.display.flip()
    clock.tick(60)
