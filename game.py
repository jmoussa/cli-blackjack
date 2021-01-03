from player import Player, Dealer
from utils import (
    get_hands_result,
    declare_winner,
    print_hand,
    construct_optimal_bet,
    expand_chipset,
    compress_chipset,
    decision_generator,
)

pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}

dealer = Dealer()
player1 = Player()

# Start of the Game
while True:
    playing = True
    num_mapping = {"ones": 1, "fives": 5, "tens": 10, "twentys": 20, "fiftys": 50}
    bust = []
    dealer.deal_hands([player1])
    dealer_card = dealer.hand[0]
    # print(f"Dealer hand: {[str(dealer_card.name) + ' of ' + dealer_card.suit]}")
    print_hand(dealer)
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
        elif int(bet_amount) > player1.get_total():
            print("Enter an amount that you can cover, bud.")
            continue

        if bet_amount != 0:
            uncompressed_chipset = expand_chipset(player1.chipset.__dict__)
            uncompressed_bet = construct_optimal_bet(int(bet_amount), uncompressed_chipset)
            bet_body = compress_chipset(uncompressed_bet)
            if bet_body:
                bet_body["pot"] = pot
                p1_bet, pot = player1.place_bet(**bet_body)
            else:
                print("Enter an amount that you can cover, bud.")
                continue

            # dealer matches player's bet
            dealer_bet, pot = dealer.place_bet(**bet_body)
            print("Dealer will match bet")

            print(p1_bet)
            print(player1.chipset.show_chips())
        print(f"Pot: {pot}")
        print(f"Pot: {sum([v*num_mapping[k] for k, v in pot.items()])}")
        print_hand(player1)

        # CARD HANDLING STAGE -------------------------------------------------------
        players = [dealer, player1]
        for p in players[:]:
            print(f"{p.name}'s turn ------------------")
            p_decision = (
                input(f"What would {p.name} like to do (hit, stay or split): ")
                if p.name != "Dealer"
                else decision_generator(p.hand, dealer_card)
            )

            if p.name == "Dealer":
                print(f"Dealer {p_decision}")

            if p_decision.lower() == "hit":
                while p_decision == "hit":
                    dealer.hit(p)
                    print_hand(p)
                    result = get_hands_result(p.hand)

                    if all(i > 21 for i in result):
                        p_decision = "bust"
                        bust.append(p)
                        break
                    if 21 in result:
                        p_decision = "win"
                        break
                    else:
                        # TODO: alter so basic strategy takes into acount dealer_sum not just dealer card
                        p_decision = (
                            input(f"What would {p.name} like to do (hit, stay or split): ")
                            if p.name != "Dealer"
                            else decision_generator(p.hand, dealer_card)
                        )

                if p_decision == "bust":
                    print("BUST!")
                    print_hand(p, override=True)
                    players.remove(p)
                    playing = False
                    break
                elif p_decision == "win":
                    print("{p.name}: WINNER WINNER CHICKEN DINNER!")
                    print(f"{[card.name + ' of ' card.suit for card in p.hand]}")
                    p.collect_winnings(pot)
                    print(p.chipset.show_chips())
                    playing = False
                    break
            elif p_decision.lower() == "split":
                if p.hand[0].value == p.hand[1].value:
                    p.execute_split()
                    print_hand(p)

        if playing is False:
            break

        # FINAL BETTING STAGE --------------------------------------------------------
        print("-------------------Final Betting Stage-------------------")
        bet_amount = input("Bet amount, or check: ")
        if bet_amount.lower() == "check":
            bet_amount = 0
        elif int(bet_amount) > player1.get_total():
            print("Enter an amount that you can cover, bud.")
            continue
        if bet_amount != 0:
            uncompressed_chipset = expand_chipset(player1.chipset.__dict__)
            uncompressed_bet = construct_optimal_bet(int(bet_amount), uncompressed_chipset)
            bet_body = compress_chipset(uncompressed_bet)
            if bet_body:
                bet_body["pot"] = pot
                p1_bet, pot = player1.place_bet(**bet_body)
            else:
                print("Enter an amount that you can cover, bud.")
                continue

            # dealer matches player's bet
            dealer_bet, pot = dealer.place_bet(**bet_body)
            print("Dealer will match bet")

            print(p1_bet)
            print(player1.chipset.show_chips())
        print(f"Pot: {pot}")
        print(f"Pot: {sum([v*num_mapping[k] for k, v in pot.items()])}")
        print_hand(player1)
        # SHOW ------------------------------------------------------------------------
        print_hand(player1)
        print_hand(dealer)
        winner = declare_winner([player1, dealer])
        print(f"{winner.name} WINS!")
        winner.collect_winnings(pot)
        playing = False

    if playing is False and len(bust) == len(players) - 1:  # all except 1 busted
        player_who_didnt_bust = list(set(players) - set(bust))[0]
        player_who_didnt_bust.collect_winnings(pot)
        bust = []
        break

    pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}
    print("RESET POT")
