import random


class Card:
    def __init__(self, name, suit):
        value_mapping = {"ace": (11, 1), "king": 10, "queen": 10, "jack": 10}
        self.name = name
        self.value = name if name not in ("ace", "king", "queen", "jack") else value_mapping[name]
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
        if len(self.deck) == 0:
            self.reshuffle()
        return card_drawn

    def reshuffle(self):
        self.deck = [Card(value, suit) for value in numbers for suit in suits]


class Chipset:
    def __init__(self, dealer: bool = False):
        if dealer:
            self.ones = 100
            self.fives = 100
            self.tens = 100
            self.twentys = 100
            self.fiftys = 100
        else:
            self.ones = 10
            self.fives = 10
            self.tens = 10
            self.twentys = 10
            self.fiftys = 10

    def place_bet(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        bet_amount_ones = ones if ones < self.ones else self.ones
        bet_amount_fives = fives if fives < self.fives else self.fives
        bet_amount_tens = tens if tens < self.tens else self.tens
        bet_amount_twentys = twentys if twentys < self.twentys else self.twentys
        bet_amount_fiftys = fiftys if fiftys < self.fiftys else self.fiftys

        pot["ones"] += bet_amount_ones
        pot["fives"] += bet_amount_fives
        pot["tens"] += bet_amount_tens
        pot["twentys"] += bet_amount_twentys
        pot["fiftys"] += bet_amount_fiftys
        self.ones = self.ones - ones if ones < self.ones else 0
        self.fives = self.fives - fives if fives < self.fives else 0
        self.tens = self.tens - tens if tens < self.tens else 0
        self.twentys = self.twentys - twentys if twentys < self.twentys else 0
        self.fiftys = self.fiftys - fiftys if fiftys < self.fiftys else 0
        return f"""
            Betting: ---------------
            1s  : {bet_amount_ones}
            5s  : {bet_amount_fives}
            10s : {bet_amount_tens}
            20s : {bet_amount_twentys}
            50s : {bet_amount_fiftys}
            ----------------------
            """

    def show_chips(self):
        return f"""
            REMAINING CHIPS: ---------------
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
    def __init__(self, name: str = "Player1"):
        self.name = name
        self.chipset = Chipset()
        self.hand = []
        self.split_hand = []

    def execute_split(self):
        self.hand.remove(player1.hand[0])
        self.split_hand.append(player1.hand[0])

    def place_bet(self, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
        return self.chipset.place_bet(ones, fives, tens, twentys, fiftys)

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


def format_bet(bet_amount):
    bet_amount = int(bet_amount)

    fiftys = bet_amount // 50 if bet_amount >= 50 else 0
    after_fiftys = bet_amount % 50 if bet_amount >= 50 else bet_amount

    twentys = after_fiftys // 20 if after_fiftys >= 20 else 0
    after_twentys = after_fiftys % 20 if after_fiftys >= 20 else after_fiftys

    tens = after_twentys // 10 if after_twentys >= 10 else 0
    after_tens = after_twentys % 10 if after_twentys >= 10 else after_twentys

    fives = after_tens // 5 if after_tens >= 5 else 0
    after_fives = after_tens % 5 if after_tens >= 5 else after_tens

    ones = after_fives // 1

    bet_amount_body = {"ones": ones, "fives": fives, "tens": tens, "twentys": twentys, "fiftys": fiftys}
    return bet_amount_body


def get_hands_result(hand: []):
    result = []
    sum = 0
    has_ace = False
    for card in hand:
        if card.name != "ace":
            sum += card.value
        else:
            has_ace = True
    if has_ace:
        ace_sum_one = sum + 1
        ace_sum_eleven = sum + 11
        result.append(ace_sum_one)
        result.append(ace_sum_eleven)
    else:
        result.append(sum)
    return result


def declare_winner(players: [Player]):
    winner_matrix = {}
    max_score = 0
    for player in players:
        winner_matrix[player] = []
        player_results = get_hands_result(player.hand)
        print(f"{player.name} results: {player_results}")

        for r in player_results:
            winner_matrix[player].append(r)
        if player.split_hand and len(player.split_hand) > 0:
            player_split_result = get_hands_result(player.split_hand)
            for r in player_split_result:
                winner_matrix[player].append(r)

    for k, v in winner_matrix.items():
        for score in v:
            if score == 21:
                winner = k
                return winner
            if score > max_score and score < 21:
                max_score = score
                winner = k
    return winner


def print_hand(player: Player):
    print(f"{player.name}: {[str(card.name) + ' of ' + card.suit for card in player.hand]}")
    if len(player.split_hand) > 0:
        print(f"{player.name}: {[str(card.name) + ' of ' + card.suit for card in player.split_hand]}")
    print(f"Value: {get_hands_result(player.hand)}")


dealer = Dealer()
player1 = Player()

# Start of the Game
while True:
    playing = True
    num_mapping = {"ones": 1, "fives": 5, "tens": 10, "twentys": 20, "fiftys": 50}
    pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}
    print("RESET POT")
    dealer.deal_hands([player1])
    dealer_card = dealer.hand[0]
    print(f"Dealer: {[str(dealer_card.name) + ' of ' + dealer_card.suit]}")
    print_hand(player1)

    while playing:
        # TODO: Modify so it works for multiple players

        # BETTING STAGE -------------------------------------------------------------
        print(player1.chipset.show_chips())
        bet_amount = input("Bet amount, or check: ")
        if bet_amount.lower() == "check":
            bet_amount = 0
        bet_body = format_bet(bet_amount)
        p1_bet = player1.place_bet(**bet_body)

        # dealer matches player's bet
        dealer_bet = dealer.place_bet(**bet_body)
        print("Dealer will match bet")

        print(p1_bet)
        print(player1.chipset.show_chips())
        print(f"Pot: {pot}")
        print(f"Pot: {sum([v*num_mapping[k] for k, v in pot.items()])}")
        print_hand(player1)

        # CARD HANDLING STAGE -------------------------------------------------------
        p1_decision = input("What would you like to do (hit, stay or split): ")
        if p1_decision.lower() == "hit":
            while p1_decision == "hit":
                dealer.hit(player1)
                print_hand(player1)

                result = get_hands_result(player1.hand)

                if all(i > 21 for i in result):
                    p1_decision = "bust"
                    break
                if 21 in result:
                    p1_decision = "win"
                    break
                else:
                    p1_decision = input("What would you like to do (hit, stay): ")

            if p1_decision == "bust":
                print("BUST!")
                print_hand(player1)
                dealer.collect_winnings()
                playing = False
                break
            elif p1_decision == "win":
                print("WINNER WINNER CHICKEN DINNER!")
                player1.collect_winnings()
                print(player1.chipset.show_chips())
                playing = False
                break
        elif p1_decision.lower() == "split":
            if player1.hand[0].value == player1.hand[1].value:
                player1.execute_split()
                print_hand(player1)

        # FINAL BETTING STAGE --------------------------------------------------------
        bet_amount = input("Bet amount, or check: ")
        if bet_amount.lower() == "check":
            bet_amount = 0
        bet_body = format_bet(bet_amount)
        p1_bet = player1.place_bet(**bet_body)

        # dealer matches player's bet
        dealer_bet = dealer.place_bet(**bet_body)
        print("Dealer will match bet")
        print(f"Pot: {pot}")
        print(f"Pot: {sum([v*num_mapping[k] for k, v in pot.items()])}")

        # SHOW ------------------------------------------------------------------------
        print_hand(player1)
        print_hand(dealer)
        winner = declare_winner([player1, dealer])
        print(f"{winner.name} WINS!")
        winner.collect_winnings()
        playing = False
