from chipset import Chipset
from deck import Deck


class Player:
    def __init__(self, name: str = "Player1"):
        self.name = name
        self.chipset = Chipset()
        self.hand = []
        self.split_hand = []

    def execute_split(self):
        self.hand.remove(self.hand[0])
        self.split_hand.append(self.hand[0])

    def place_bet(self, pot: dict, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        return self.chipset.place_bet(pot, ones, fives, tens, twentys, fiftys)

    def call(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        self.chipset.place_bet(ones, fives, tens, twentys, fiftys)

    def collect_winnings(self):
        new_pot = self.chipset.collect_winnings()
        global pot
        pot = new_pot


class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        self.deck = Deck()
        self.chipset = Chipset(dealer=True)
        self.hand = []
        self.split_hand = []

    def deal_hands(self, players: [Player]):
        self.hand = []
        self.hand.append(self.deck.draw_card())
        self.hand.append(self.deck.draw_card())
        for p in players:
            p.hand = []
            p.hand.append(self.deck.draw_card())
            p.hand.append(self.deck.draw_card())

    def hit(self, player: Player):
        player.hand.append(self.deck.draw_card())
