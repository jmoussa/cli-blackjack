import random


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.color = "red" if self.suit in ("heart", "diamonds") else "black"


suits = ["heart", "diamonds", "spades", "clubs"]
numbers = ["ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "king", "queen", "jack"]
global pot
pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}


class Deck:
    def __init__(self):
        self.deck = [Card(value, suit) for value in numbers for suit in suits]

    def draw_card(self):
        card_drawn = random.choice(self.deck)
        self.deck.remove(card_drawn)
        return card_drawn

    def reshuffle(self):
        self.deck = [Card(value, suit) for value in numbers for suit in suits]


class Chipset:
    def __init__(self):
        self.ones = 10
        self.fives = 10
        self.tens = 10
        self.twentys = 10
        self.fiftys = 10

    def place_bet(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        pot["ones"] += ones
        pot["fives"] += fives
        pot["tens"] += tens
        pot["twentys"] += twentys
        pot["fiftys"] += fiftys
        self.ones -= ones
        self.fives -= fives
        self.tens -= tens
        self.twentys -= twentys
        self.fiftys -= fiftys

    def show_chips(self):
        return f"""
            CHIPS: ---------------
            1s  : {self.ones}
            5s  : {self.fives}
            10s : {self.tens}
            20s : {self.twentys}
            50s : {self.fiftys}
            ----------------------
            """

    def collect_winnings(self):
        self.ones += pot["ones"]
        self.fives += pot["fives"]
        self.tens += pot["tens"]
        self.twentys += pot["twentys"]
        self.fiftys += pot["fiftys"]
        return {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}


class Player:
    def __init__(self):
        self.chipset = Chipset()
        self.winner_winner_chicken_dinner = False
        self.hand = []

    def place_bet(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        self.chipset.place_bet(ones, fives, tens, twentys, fiftys)

    def call(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        self.chipset.place_bet(ones, fives, tens, twentys, fiftys)

    def collect_winnings(self):
        if self.winner_winner_chicken_dinner:
            new_pot = self.chipset.collect_winnings()
            global pot
            pot = new_pot
        else:
            print("Sorry you haven't won.")


class Dealer(Player):
    def __init__(self):
        self.deck = Deck()

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


def format_bet(bet_amount):
    bet_amount = int(bet_amount)

    fiftys = bet_amount // 50 if bet_amount > 50 else 0
    after_fiftys = bet_amount % 50 if bet_amount > 50 else bet_amount

    twentys = after_fiftys // 20 if after_fiftys > 20 else 0
    after_twentys = after_fiftys % 20 if after_fiftys > 20 else after_fiftys

    tens = after_twentys // 10 if after_twentys > 10 else 0
    after_tens = after_twentys % 10 if after_twentys > 10 else after_twentys

    fives = after_tens // 5 if after_tens > 5 else 0
    after_fives = after_tens % 5 if after_tens > 5 else after_tens

    ones = after_fives // 1

    bet_amount_body = {"ones": ones, "fives": fives, "tens": tens, "twentys": twentys, "fiftys": fiftys}
    return bet_amount_body


dealer = Dealer()
player1 = Player()

# Start of the Game
while True:
    playing = True
    dealer.deal_hands([player1])
    dealer_card = dealer.hand[0]
    print(f"Dealer: {str(dealer_card.value) + ' of ' + dealer_card.suit }")
    print(f"Player: {[str(card.value) + ' of ' + card.suit for card in player1.hand]}")

    while playing:
        print(player1.chipset.show_chips())
        bet_amount = input("Bet amount: ")
        bet_body = format_bet(bet_amount)
        player1.place_bet(**bet_body)
        print(player1.chipset.show_chips())
        playing = False
    break
