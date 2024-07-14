import pygame
import random
import os

pygame.init()
clock = pygame.time.Clock()

cursor = pygame.sprite.Group()
sprites = pygame.sprite.Group()


#defining screen
screen = pygame.display.set_mode((750, 750))

pygame.display.set_caption("Blackjack")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


#TEXTURES
background_image = pygame.transform.scale(pygame.image.load("img/background.png"), (750, 750))
mouse_texture = pygame.transform.scale(pygame.image.load("img/mouse.png"), (8, 8))
back_card_texture = pygame.transform.scale(pygame.image.load("img/back.png"), (96, 128))
ace_sign_texture = pygame.transform.scale(pygame.image.load("img/ace_sign.png"), (128, 128))

chip_textures = [
    pygame.transform.scale(pygame.image.load("img/chips/ten_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/fifty_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/hundred_chip1.png"), (80, 80))
]

chip_clicked_textures = [
    pygame.transform.scale(pygame.image.load("img/chips/ten_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/fifty_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/hundred_chip2.png"), (80, 80))

]

button_textures = [
    pygame.transform.scale(pygame.image.load("img/hit_button1.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/stand_button1.png"), (200, 75))
]

pressed_button_textures = [
    pygame.transform.scale(pygame.image.load("img/hit_button2.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/stand_button2.png"), (200, 75))
]

card_textures = []
card_iterate_count = 1
for img in os.listdir("img/cards"):
    if card_iterate_count == 11:
        break
    card_textures.append(pygame.transform.scale(pygame.image.load("img/cards/card_"+str(card_iterate_count)+".png"), (96, 128)))
    card_iterate_count += 1





class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        cursor.add(self)

        self.image = mouse_texture
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()



class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        super().__init__()

        sprites.add(self)

        self.value = random.randrange(1, 10)

        self.image = card_textures[self.value]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.flipped = flipped

    def update(self):
        if self.flipped == False:
            self.image = back_card_texture
        if self.flipped == True:
            self.image = card_textures[self.value]


class Button(pygame.sprite.Sprite):
    def __init__(self, img, pressed_img, x, y):
        super().__init__()

        sprites.add(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y  

        self.pressed_img = pressed_img
        self.img = img

        self.clicked = False
        self.animation_frames = 0

    def update(self):
        if self.clicked == True:
            self.animation_frames += 1
            self.image = self.pressed_img

            if self.animation_frames == 25:
                self.image = self.img
                self.clicked = False
                self.animation_frames = 0




def buttonClicked(button, mouse):
    if pygame.sprite.collide_mask(button, mouse):
        button.clicked = True
        return True
    else:
        return False



mouseCursor = Cursor()

tenChip = Button(chip_textures[0], chip_clicked_textures[0], 10, 330)
fiftyChip = Button(chip_textures[1], chip_clicked_textures[1], 10, 420)
hundredChip = Button(chip_textures[2], chip_clicked_textures[2], 10, 510)

hitButton = Button(button_textures[0], pressed_button_textures[0], 150, 560)
standButton = Button(button_textures[1], pressed_button_textures[1], 380, 560)

starting_cards = [Card(280, 380, True), Card(350, 330, True)]
all_cards_len = 1


player_hit = False
player_stand = False



#MAIN FUNCTION
running = True
while running: 
    player_hit = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        if buttonClicked(hitButton, mouseCursor):
            hitButton.clicked = True
            player_hit = True
        if buttonClicked(standButton, mouseCursor):
            standButton.clicked = True
            player_stand = True



    if player_hit == True:
        all_cards_len += 1

        Card(350+all_cards_len*30, 330, True)


            
            


    
        









            
            



    sprites.update()
    cursor.update()

    screen.blit(background_image, (0, 0))

    sprites.draw(screen)
    cursor.draw(screen)

    clock.tick(60)
    pygame.display.flip()
