from player import Player, Dealer
from utils import format_bet, get_hands_result, declare_winner, print_hand

pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}

dealer = Dealer()
player1 = Player()

# Start of the Game
while True:
    playing = True
    num_mapping = {"ones": 1, "fives": 5, "tens": 10, "twentys": 20, "fiftys": 50}

    dealer.deal_hands([player1])
    dealer_card = dealer.hand[0]
    print(f"Dealer hand: {[str(dealer_card.name) + ' of ' + dealer_card.suit]}")
    print_hand(player1)
    while playing:
        # TODO: Modify so it works for multiple players

        # BETTING STAGE -------------------------------------------------------------
        print(f"Pot: {pot}")
        print(f"Pot: {sum([v*num_mapping[k] for k, v in pot.items()])}")
        print(player1.chipset.show_chips())
        bet_amount = input("Bet amount, or check: ")
        if bet_amount.lower() == "check":
            bet_amount = 0
        bet_body = format_bet(pot, bet_amount)
        p1_bet, pot = player1.place_bet(**bet_body)

        # dealer matches player's bet
        dealer_bet, pot = dealer.place_bet(**bet_body)
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
        bet_body = format_bet(pot, bet_amount)
        p1_bet, pot = player1.place_bet(**bet_body)

        # dealer matches player's bet
        dealer_bet, pot = dealer.place_bet(**bet_body)
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
    pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}
    print("RESET POT")
