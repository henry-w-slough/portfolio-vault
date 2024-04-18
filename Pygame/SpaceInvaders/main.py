import pygame
import random

pygame.init()
clock = pygame.time.Clock()

#defining classes for player, aliens, player bullets, and alien bullets
sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
alienBullets = pygame.sprite.Group()

#defining screen
screen = pygame.display.set_mode((900, 700))
pygame.display.set_icon(pygame.image.load("img/logo.png"))

#text font for text on screen
textFont = pygame.font.Font("joystix monospace.otf", 50)
deathFont = pygame.font.Font("joystix monospace.otf", 50)

#defining all images used in game
alienTexture = pygame.transform.scale(pygame.image.load("img/alien.png"), (55, 55))
cannonTexture = pygame.transform.scale(pygame.image.load("img/cannon.webp"), (60, 50))
bulletTexture = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("img/bullet.png"), 90), (50, 50))
explosionTexture = pygame.transform.scale(pygame.image.load("img/explosion.png"), (50, 45))
backgroundTexture = pygame.image.load("img/background.png")

#defining all sounds used in game
alienDeathSound = pygame.mixer.Sound("audio/alienDeathSound.wav")
cannonShootSound = pygame.mixer.Sound("audio/cannonShootSound.wav")
nextLevelSound = pygame.mixer.Sound("audio/nextLevelSound.wav")
cannonDeathSound = pygame.mixer.Sound("audio/cannonDeathSound.wav")
alienBulletShootSound = pygame.mixer.Sound("audio/alienBulletShootSound.wav")
cannonHurtSound = pygame.mixer.Sound("audio/cannonHurtSound.wav")

#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = bulletTexture
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

    def update(self):
        #killing bullet if it passes the top screen border
        if (self.rect.y <= -50):
            self.kill()
        else:
            self.rect.y -= 10

#alien bullet class
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = bulletTexture
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

    def update(self):
        #killing alien bullet if it moves past bottom screen border
        if (self.rect.y >= 930):
            self.kill()
        else:
            self.rect.y += 10

#alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()

        self.image = alienTexture
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

        self.speed = speed

        self.movement = speed

        self.animationTicks = 25

        self.hit = False

        #random number to decide whether the alien can shoot bullets or not
        self.shootingAlien = random.randrange(1, 100)

        if (self.shootingAlien > 90):
            #setting alien shooting parameters if the shootingAlien is above 90 as a minority chance
            self.originalBulletTicks = random.randrange(60, 120)
            self.bulletTicks = self.originalBulletTicks

    def update(self):

        #checking if the alien can shoot, and then shooting after a random given time if it can
        if (self.shootingAlien > 90):
            self.bulletTicks -= 1

            #shooting
            if self.bulletTicks <= 0:
                alienBulletShootSound.play()
                alienBullets.add(AlienBullet(self.rect.x, self.rect.y))
                self.bulletTicks = self.originalBulletTicks

        #checking for alien and player bullet collision
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            alienDeathSound.play()
            self.hit = True
            
        #checking to see if the alien has been hit, then changing the image to an explosion, and waiting a time till the alien dies
        if self.hit == True:
            self.image = explosionTexture
            self.animationTicks -= 1

            if self.animationTicks <= 0:
                self.kill()
        

        #moving in the movement direction
        self.rect.x += self.movement

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bulletTicks, health):
        super().__init__()

        self.image = cannonTexture
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

        self.bulletTicks = bulletTicks

        self.health = health

        self.animationTicks = 60

        self.hit = False

    def update(self):

        #updates if the player hasnt been hit yet, prevents movement and shooting while dead
        if self.hit == False:
            
            self.bulletTicks += 1
            keys = pygame.key.get_pressed()


            #movement and checking for edges
            if (self.rect.x >= 835):
                if keys[pygame.K_a]:
                    self.rect.x -= 5
            if (self.rect.x <= 0):
                if keys[pygame.K_d]:
                    self.rect.x += 5

            if (self.rect.x >= 0 and self.rect.x <= 835):   
                if keys[pygame.K_a]:
                    self.rect.x -= 5
                if keys[pygame.K_d]:
                    self.rect.x += 5


            #shooting
            if (keys[pygame.K_SPACE]):
                if (self.bulletTicks >= 25):
                    cannonShootSound.play()
                    bullets.add(Bullet(self.rect.x, self.rect.y))
                    self.bulletTicks = 0

            if self.health <= 0:
                self.hit = True
            
        #if the player has been hit, changes the image to an explosion texture and waits a time till death and game ending
        if self.hit == True:
            cannonDeathSound.play()
            self.image = pygame.transform.scale(explosionTexture, (100, 100))
            self.animationTicks -= 1

            if self.animationTicks <= 0:
                self.kill()
            
#function for every new wave
def newWave():
    randomAlienSpeed = random.randrange(2, 4)

    for row in range(6): 
        for column in range(4):
            aliens.add(Alien(row*60, column*60+50, randomAlienSpeed))


#defining player
score = 0
player = Player(0, 600, 15, 3)
player.hit = False
sprites.add(player)


#texts
scoreText = textFont.render("Score "+str(score), False, (255, 255, 255))
healthText = textFont.render("Health "+str(player.health), False, (255, 255, 255))
deathText = textFont.render("You Died!", False, (255, 255, 255))

#setting the first wave
newWave()

#main loop
running = True
while running:
    
    #closing game if you press exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False       

    #main updates for if the player health is bigger than 0
    if player.health > 0:

        #moving all the aliens equally by changing all their momentum variables
        for alien in aliens:
            if alien.rect.x >= 850:
                for alien in aliens:
                    alien.rect.y += 30
                    alien.movement = -alien.speed
            if alien.rect.x <= 1:
                for alien in aliens:
                    alien.movement = alien.speed

        #checking the length of the aliens group to see if all aliens are dead
        if aliens.__len__() <= 0:
            score += 100
            scoreText = textFont.render("Score "+str(score), False, (255, 255, 255))
            newWave()
            pygame.mixer.Sound.play(nextLevelSound)

        #collision between player and alien bullets
        if pygame.sprite.groupcollide(sprites, alienBullets, False, True, pygame.sprite.collide_mask):
            cannonHurtSound.play()
            player.health -= 1
            healthText = textFont.render("Health "+str(player.health), False, (255, 255, 255)) 

        #collision between player and aliens
        if pygame.sprite.groupcollide(sprites, aliens, False, False, pygame.sprite.collide_mask):
            cannonHurtSound.play()
            player.health -= 100
            healthText = textFont.render("Health "+str(player.health), False, (255, 255, 255)) 


    #if the player is dead, kill all aliens and alien bullets too
    if player.hit == True:
        for alien in aliens:
            alien.kill()
        for bullet in alienBullets:
            bullet.kill()

    #updating all sprites
    sprites.update()
    bullets.update()
    aliens.update()
    alienBullets.update()

    #displaying background texture
    screen.blit(backgroundTexture, (0, 0))

    #displaying all the sprites
    sprites.draw(screen)
    bullets.draw(screen)
    aliens.draw(screen)
    alienBullets.draw(screen)

    #blitting score and health texts
    if player.hit == False:
        screen.blit(scoreText, (10, 0))
        screen.blit(healthText, (560, 0))
    if player.hit == True:
        scoreText = deathFont.render("Score "+str(score), False, (255, 255, 255))
        screen.blit(scoreText, (deathText.get_rect(center=(450, 350))))
        screen.blit(deathText, (250, 200))
    

    #updating screen and FPS
    pygame.display.flip()
    clock.tick(60)



