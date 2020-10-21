from player import Player


def format_bet(pot, bet_amount):
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

    bet_amount_body = {"pot": pot, "ones": ones, "fives": fives, "tens": tens, "twentys": twentys, "fiftys": fiftys}
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
