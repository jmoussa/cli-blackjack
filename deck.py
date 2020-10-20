from card import Card
import random

suits = ["heart", "diamonds", "spades", "clubs"]
numbers = ["ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "king", "queen", "jack"]


class Deck:
    def __init__(self):
        self.deck = [Card(value, suit) for value in numbers for suit in suits]

    def draw_card(self):
        card_drawn = random.choice(self.deck)
        self.deck.remove(card_drawn)
        if len(self.deck) == 0:
            self.reshuffle()
        return card_drawn

    def reshuffle(self):
        self.deck = [Card(value, suit) for value in numbers for suit in suits]
