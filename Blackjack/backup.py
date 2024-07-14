import pygame
import random
import os

pygame.init()
clock = pygame.time.Clock()

cursor = pygame.sprite.Group()
buttons = pygame.sprite.Group()
cards = pygame.sprite.Group()

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

        self.image = mouse_texture
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()



class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        super().__init__()

        cards.add(self)

        self.value = random.randrange(1, 10)

        self.image = card_textures[self.value]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.flipped = flipped

    def update(self):
        if self.flipped == True:
            self.image = back_card_texture
        if self.flipped == False:
            self.image = card_textures[self.value]


class Button(pygame.sprite.Sprite):
    def __init__(self, img, pressed_img, x, y):
        super().__init__()

        buttons.add(self)

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



bigTextFont = pygame.font.Font("symtext/Symtext.ttf", 40)
smallTextFont = pygame.font.Font("symtext/Symtext.ttf", 20)
winTextFont = pygame.font.Font("symtext/Symtext.ttf", 60)

playerWinText = winTextFont.render("You Win", False, (255, 255, 255))
dealerWinText = winTextFont.render("Dealer Wins", False, (255, 255, 255))
standOffText = winTextFont.render("Standoff", False, (255, 255, 255))


mouseCursor = Cursor()
cursor.add(mouseCursor)

tenChip = Button(chip_textures[0], chip_clicked_textures[0], 10, 330)
fiftyChip = Button(chip_textures[1], chip_clicked_textures[1], 10, 420)
hundredChip = Button(chip_textures[2], chip_clicked_textures[2], 10, 510)

hitButton = Button(button_textures[0], pressed_button_textures[0], 150, 560)
standButton = Button(button_textures[1], pressed_button_textures[1], 380, 560)



starting_cards = [Card(280, 330, False), Card(340, 330, False), Card(280, 80, False), Card(330, 80, True)]


playerHand = starting_cards[0].value + starting_cards[1].value + 2 
player_cards_count = 1
playerHit = True

playerMoney = 1000
playerBet = 0


dealerHand = starting_cards[2].value + 1
dealer_cards_count = 1
dealer_card_delay = 60


playerWin = False
dealerWin = False



#MAIN FUNCTION
running = True
while running: 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



        #Clicking poker chips and making sure money never goes under zero
        if event.type == pygame.MOUSEBUTTONDOWN:

            if buttonClicked(tenChip, mouseCursor) == True:
                if playerMoney - 10 >= 0:
                    playerBet += 10
                    playerMoney -= 10
            if buttonClicked(fiftyChip, mouseCursor) == True:
                if playerMoney - 50 >= 0:
                    playerBet += 50
                    playerMoney -= 50
            if buttonClicked(hundredChip, mouseCursor) == True:
                if playerMoney - 100 >= 0:
                    playerBet += 100
                    playerMoney -= 100


            #Stand button and hit button
            if buttonClicked(standButton, mouseCursor) == True:
                standButton.clicked = True
                playerHit = False
                dealerHand += starting_cards[3].value + 1
            if buttonClicked(hitButton, mouseCursor) == True:
                hitButton.clicked = True



            if playerHit == True:
                if buttonClicked(hitButton, mouseCursor) == True:
                    newCard = Card(330+player_cards_count*50, 330, False)
                    player_cards_count += 1
                    playerHand += newCard.value

                if playerHand >= 21:
                    dealerHand += starting_cards[3].value
                if playerHand > 21:
                    dealerWin = True


  

    if playerHit == False:
        starting_cards[3].flipped = False
        dealer_card_delay -= 1

        if dealerHand < playerHand and dealer_card_delay <= 0:
            newCard = Card(330+dealer_cards_count*40, 80, False)
            dealerHand += newCard.value
            dealer_card_delay = 60
            dealer_cards_count += 1

        if dealerHand > 21:
            playerWin = True
        if dealerHand > playerHand:
            dealerWin = True
            
            



    buttons.update()
    cards.update()
    cursor.update()

    playerBetText = bigTextFont.render("Bet: "+str(playerBet), False, (255, 255, 255))
    playerMoneyText = bigTextFont.render("Money: "+str(playerMoney), False, (255, 255, 255))
    playerHandText = smallTextFont.render("Hand: "+str(playerHand), False, (255, 255, 255))
    dealerHandText = smallTextFont.render("Dealer Hand: "+str(dealerHand), False, (255, 255, 255))

    screen.blit(background_image, (0, 0))

    cards.draw(screen)
    buttons.draw(screen)

    screen.blit(playerMoneyText, (20, 680))
    screen.blit(playerBetText, (20, 630))
    screen.blit(dealerHandText, (270, 0))
    screen.blit(playerHandText, (320, 540))

    if playerWin == True:
        screen.blit(playerWinText, (230, 220))
    if dealerWin == True:
        screen.blit(dealerWinText, (160, 220))

    cursor.draw(screen)

    clock.tick(60)
    pygame.display.flip()