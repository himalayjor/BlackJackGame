import os
import sys
import re
import shutil
import pygame, random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)


CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = pygame.image.load("cards.jfitz.png").convert()

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = pygame.image.load("card_back.png")


in_play = False
outcome = ""
score = 0
message = ""


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None


    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        posrect = [pos[0] , pos[1], CARD_SIZE[0], CARD_SIZE[1]]
        imgrect = [CARD_SIZE[0] * RANKS.index(self.rank), CARD_SIZE[1] * SUITS.index(self.suit), CARD_SIZE[0], CARD_SIZE[1]]
        canvas.blit(card_images, posrect,  imgrect )


    def draw_back(self, canvas, pos):
        posrect = [pos[0] , pos[1], CARD_BACK_SIZE[0], CARD_BACK_SIZE[1]]

        canvas.blit(card_back, posrect)


# define hand class
class Hand:
    def __init__(self, player):
        self.hand = []
        self.player = player

    def __str__(self):
        s = "Hand contains "
        for i in self.hand:
           s += str(i) + " "
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        val = 0
        ace = False
        for i in self.hand:
            j = str(i)
            val += VALUES[j[1]]
            if j[1] == 'A':
                ace = True

        if self.player == 'p':
            return val

        if not ace:
            return val
        else:
            if val + 10 <= 21:
                return val + 10
            else:
                return val


    def draw(self, canvas, pos):
        if (self.player == 'p') or (self.player == 'd' and not in_play):
            for i in self.hand:
                i.draw(canvas,pos)
                pos[0] += 25 + 71
        else:
             l = len(self.hand)
             cd = self.hand[0]
             cd.draw_back(canvas, pos)
             pos[0] += 71 + 25
             i = 1
             while (i < l):
                 cd = self.hand[i]
                 cd.draw(canvas, pos)
                 i += 1

# define deck class class Deck:
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        s = "Deck contains "
        for i in self.deck:
            s += str(i) + " "
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dhand, phand, message, score

    if in_play:
        score -= 1
        outcome = "You lose"
        in_play = False

    deck = Deck()
    deck.shuffle()
    dhand = Hand('d')
    phand = Hand('p')

    dhand.add_card(deck.deal_card())
    dhand.add_card(deck.deal_card())
    phand.add_card(deck.deal_card())
    phand.add_card(deck.deal_card())

    in_play = True
    outcome = ""
    message = "Hit or stand?"


def hit():
    global in_play, outcome, score, message

    if not in_play:
        return

    phand.add_card(deck.deal_card())
    if phand.get_value() > 21:
        in_play = False
        outcome = "You went busted and lose"
        score -= 1
        message = "New deal?"

def stand():
    global in_play, outcome, score, message


    if not in_play:
        return

    while dhand.get_value() < 17:
        dhand.add_card(deck.deal_card())


    if dhand.get_value() > 21:
        outcome = "Dealer is busted and You win"
        in_play = False
        score += 1
    elif dhand.get_value() >= phand.get_value():
        outcome = "You lose"
        in_play = False
        score -= 1
    else:
        outcome = "You win"
        in_play = False
        score += 1
    message = "New deal?"

# draw handler
def draw(screen):
    # test to make sure that card.draw works, replace with your code below
    font=pygame.font.Font(None, 48)
    text=font.render('Blackjack', 1,(0,255,255))
    screen.blit(text, (100, 100))

    font=pygame.font.Font(None, 32)
    text=font.render('Score : ' + str(score), 1,(255,0,0))
    screen.blit(text, (400, 120))

    font=pygame.font.Font(None, 24)
    text=font.render("Dealer", 1,(0,0,0))
    screen.blit(text, (75, 175))

    text=font.render(outcome, 1,(0,0,0))
    screen.blit(text, (250, 175))

    text=font.render('Player', 1,(0,0,0))
    screen.blit(text, (75, 350))

    text=font.render(message, 1,(0,0,0))
    screen.blit(text, (250, 350))


    phand.draw(screen, [75, 375])
    dhand.draw(screen, [75, 200])


pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

deal()

while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == K_d:
                deal()
            elif event.type == pygame.KEYDOWN and event.key == K_h:
                hit()
            elif event.type == pygame.KEYDOWN and event.key == K_s:
                stand()

        screen.fill((0, 100, 0))
        draw(screen)
        pygame.display.update()





