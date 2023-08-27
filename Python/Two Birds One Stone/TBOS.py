import pygame
import random

pygame.init()
clock = pygame.time.Clock()


#textures
rock_textures = {
    1: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/rock/rock1.png"), (50, 50)), 
    2: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/rock/rock2.png"), (50, 50)), 
    3: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/rock/rock3.png"), (50, 50)),
    4: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/rock/rock4.png"), (50, 50))
}

slingshot_textures = {
    1: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/slingshot/slingshot1.png"), (120, 120))
}

bird_textures = {
    1: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/bird/bird1.png"), ((90, 90))),
    2: pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/bird/bird2.png"), (90, 90))
}

#other various textures
telephone_pole = pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/telephone pole/telephone_pole.png"), (800, 560))
background = pygame.transform.scale(pygame.image.load("Python/Two Birds One Stone/background.jpeg"), (1500, 750))


#audio
birdDeathNoise = pygame.mixer.Sound("Python/Two Birds One Stone/audio/death.wav")
birdChangeDirection = pygame.mixer.Sound("Python/Two Birds One Stone/audio/changeDirection.wav")
nextLevelNoise = pygame.mixer.Sound("Python/Two Birds One Stone/audio/nextLevel.wav")
shootingNoise = pygame.mixer.Sound("Python/Two Birds One Stone/audio/shoot.wav")

backgroundMusic = pygame.mixer.Sound("Python/Two Birds One Stone/audio/backgroundMusic.mp3")
gameFinishMusic = pygame.mixer.Sound("Python/Two Birds One Stone/audio/gameFinishMusic.mp3")



#screen decleration
screen = pygame.display.set_mode((800, 750))
pygame.display.set_caption("Two Birds One Stone")
screenColor = (20, 124, 190)

#text screen with transparent background
text_layer = pygame.Surface([800, 750], pygame.SRCALPHA, 32).convert_alpha()

all_birds_list = pygame.sprite.Group()
all_bullets_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()



#sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, src, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        
        pygame.draw.rect(self.image, screenColor, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


    def update(self, speed):

        #controls
        keys = pygame.key.get_pressed()

        #stopping movement at the end of the screen.
        if self.rect.x >= 659 or self.rect.x <= 20:
            if self.rect.x >= 659:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.rect.x -= speed

            if self.rect.x <= 20:
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.rect.x += speed

        else:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x -= speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x += speed

        
        
#rock class
class Rock(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.animationTimer = 0
        self.frame = 1

        self.rocksUsed = 0

        self.image = pygame.Surface((width, height))
        
        pygame.draw.rect(self.image, screenColor, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

        self.image = rock_textures[self.frame]


    def update(self, speed, origin_y, origin_x):

        self.rect.y -= speed

        #movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.rect.y <= -150:
                pygame.mixer.Sound.play(shootingNoise)
                self.rocksUsed += 1
                self.rect.y = origin_y+10
                self.rect.x = origin_x+35
            

        #rock animation
        self.animationTimer += 1

        if self.animationTimer == 18:
            self.frame += 1
            self.animationTimer = 0

        if self.frame == 4:
            self.frame = 1

        self.image = rock_textures[self.frame]



#bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.direction = random.randint(1, 10)
        self.speed = random.randint(1, 30)
        self.floor = random.randint(1, 10)

        self.image = pygame.Surface((width, height))
        
        pygame.draw.rect(self.image, ((255, 255, 255)), pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


        #pygame being stupid and not letting birds spawn
        self.rect.y = 240


        #speed 1
        if self.speed <= 10:
            self.speed = 1

        #speed 2
        if self.speed <= 20 and self.speed > 10:
            self.speed = 2

        #speed 3
        if self.speed <= 30 and self.speed > 20:
            self.speed = 3

        
    def update(self):
        
        #changing directions
        if self.rect.x >= 690:
            self.direction = 1
            self.image = bird_textures[1]

        if self.rect.x <= 20:
            self.direction = 10
            self.image = bird_textures[2]


        #changing speed when direction changes
        if self.direction >= 5:
            self.rect.x += self.speed
        if self.direction < 5:
            self.rect.x -= self.speed


        #random floor on the telephone line
        if self.floor >= 5:
            self.rect.y = 240
        if self.floor < 5:
            self.rect.y = 363

def finishGame(rocksUsed, birdsDead):
    
    #the final score of the game, decided by rocks used and birds dead.
    finalScore = 2000
    for x in range(rocksUsed):
        finalScore -= 50
    
    for x in range(birdsDead):
        finalScore += 50


    #stopping background music, and starting the win sound effect.
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gameFinishMusic)


    #clearing the screen.
    screen.blit(background, (0, 0))


    #fonts for the final score, birds dead, and rocks used.
    basicFont = pygame.font.SysFont("applesdgothicneo", 50)
    scoreTextFont = pygame.font.SysFont("applesdgothicneo", 120)


    #rendering the font so it can be displayed on the screen.
    scoreHeaderText = basicFont.render("Final Score", True, (0, 0, 0))
    scoreText = scoreTextFont.render(str(finalScore), True, (0, 0, 0))
    rocksUsed = font.render("Rocks Used: "+str(rocksUsed), True, (0, 0, 0))
    birdsDead = font.render("Birds Killed: "+str(birdsDead), True, (0, 0, 0))


    #aligning final score text
    if finalScore == 2000:
        screen.blit(scoreText, (270, 150))
    if finalScore < 2000:
        screen.blit(scoreText, (285, 150))
    

    #blitting all the other text.
    screen.blit(scoreHeaderText, (290, 100))
    screen.blit(birdsDead, (315, 375))
    screen.blit(rocksUsed, (310, 325))

    pygame.display.flip()



#player
player = Sprite(slingshot_textures[1], 120, 120)
player.image = slingshot_textures[1]
all_sprites_list.add(player)
player.rect.y = 630
player.rect.x = 325



#the only rock that the player shoots.
rock = Rock(30, 25)
rock.rect.x = -40
all_bullets_list.add(rock)


#levels and birds per level.
level = 1
birdsPerLevel = 2
birdsDead = 0


#first 2 birds in the game .
for x in range(birdsPerLevel):
    all_birds_list.add(Bird(38, 35))


running = True
pygame.mixer.Sound.play(backgroundMusic, 25)
while running:
    
    
    #adding to level, dead birds, and playing noise when all the birds are dead
    if all_birds_list.__len__() == 0:
        #making new birds
        for x in range(birdsPerLevel):
            all_birds_list.add(Bird(35, 50))
        
        #changing level, and birdsDead back to zero.
        rock.rect.y = -40
        level += 1
        birdsDead += 1
        pygame.mixer.Sound.play(nextLevelNoise)
        

    
    #collision with birds and rocks
    if pygame.sprite.groupcollide(all_bullets_list, all_birds_list, False, True):
        pygame.mixer.Sound.play(birdDeathNoise)


    #exiting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #secret music
    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        pygame.mixer.Sound.stop(backgroundMusic)
        backgroundMusic = pygame.mixer.Sound("Python/Two Birds One Stone/audio/secret_music.mp3")
        pygame.mixer.Sound.play(backgroundMusic)
    


    #updating sprite groups
    all_sprites_list.update(5)
    all_birds_list.update()
    all_bullets_list.update(8, player.rect.y, player.rect.x)
    

    #blitting images
    screen.blit(background, (0, 0))
    screen.blit(telephone_pole, (0, 100))


    #drawing lists
    all_sprites_list.draw(screen)
    all_birds_list.draw(screen)
    all_bullets_list.draw(screen)


    #filling text layer with transparent texture.
    text_layer.fill(pygame.SRCALPHA)


    #finishing the game at level 20.
    if level == 20:
        finishGame(rock.rocksUsed, birdsDead)
        level = 21
        

    if level < 20:
        #font for all the text.
        font = pygame.font.SysFont("applesdgothicneo", 35)

        #score texts
        levelText = font.render("LEVEL "+str(level), True, (0, 0, 0))
        rockAmountText = font.render("Rocks Used: "+str(rock.rocksUsed), True, (0, 0, 0))
        birdsDeadText = font.render("Birds Killed "+str(birdsDead), True, (0, 0, 0))

    

        #blitting the scores onto the text layer
        text_layer.blit(levelText, (10, 10))
        text_layer.blit(rockAmountText, (415, 10))
        text_layer.blit(birdsDeadText, (175, 10))
    
        #blitting the text layer onto the screen
        screen.blit(text_layer, (0, 0))


        pygame.display.flip()
        clock.tick(60)









