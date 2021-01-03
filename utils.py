from player import Player
from card import Card

num_mapping = {"ones": 1, "fives": 5, "tens": 10, "twentys": 20, "fiftys": 50}
reverse_num_mapping = {1: "ones", 5: "fives", 10: "tens", 20: "twentys", 50: "fiftys"}


def construct_optimal_bet(bet_amount: int, chipset: list, memo: dict = {}):

    if f"{bet_amount}-{chipset}" in memo:
        return memo[f"{bet_amount}-{chipset}"]
    if bet_amount == 0:
        return []
    if bet_amount < 0:
        return None

    for i in list(reversed(range(len(chipset)))):
        remainder = bet_amount - chipset[i]
        last_chip = chipset[i]
        index_after = i + 1
        new_chipset = chipset[index_after:]
        remainder_result = construct_optimal_bet(remainder, new_chipset, memo)
        if remainder_result is not None:
            remainder_result.append(last_chip)
            memo[f"{bet_amount}-{chipset}"] = remainder_result
            return memo[f"{bet_amount}-{chipset}"]

    memo[f"{bet_amount}-{chipset}"] = None
    return memo[f"{bet_amount}-{chipset}"]


def expand_chipset(chipset: dict):
    res = []
    for d, c in chipset.items():
        subset = [num_mapping[d] for i in range(c)]
        for i in subset:
            res.append(i)
    return res


def compress_chipset(chipset: list):
    chipset_dict = {}
    for chip in chipset:
        if reverse_num_mapping[chip] in chipset_dict:
            chipset_dict[reverse_num_mapping[chip]] += 1
        else:
            chipset_dict[reverse_num_mapping[chip]] = 1

    return chipset_dict


def decision_generator(hand: list, dealer_up_card: Card) -> str:
    # based on the hand, decide to hit, stay or split:
    """
    hand is a list of card objects
    {'name': str, 'value': str, 'suit': str, 'color': str}
    """
    sum = 0
    sum_ace_hi = 0
    for card in hand:
        if type(card.value) == int:
            sum += card.value
            sum_ace_hi += card.value
        elif type(card.value) == tuple or card.name == "ace":
            sum += 1
            sum_ace_hi += 11
        else:
            sum += 10
            sum_ace_hi += 10

    # the   d e c i d e r
    # coding in basic strategy... it's an ongoing process
    if (
        sum >= 17
        or ((sum >= 9 and sum_ace_hi >= 19) and (sum <= 11 and sum_ace_hi <= 21))  # ace, 8-10
        or (((sum <= 16 or sum_ace_hi <= 16) and (sum >= 13 or sum_ace_hi >= 113)) and (dealer_up_card.value <= 6))
    ):
        decision = "stay"
    elif (((sum <= 16 or sum_ace_hi <= 16) and (sum >= 13 or sum_ace_hi >= 113)) and (dealer_up_card.value >= 7)) or (
        (sum >= 3 or sum_ace_hi >= 13) and (sum <= 7 or sum_ace_hi <= 17) or (sum >= 5 and sum <= 8)
    ):
        decision = "hit"
    elif ([card.name for card in hand].count("ace") > 1) or ([card.value for card in hand].count(8) > 1):
        decision = "split"
    else:
        decision = "stay"
    return decision


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


def print_hand(player: Player, override=False):
    if player.name != "Dealer" or override:
        print(f"{player.name}: {[str(card.name) + ' of ' + card.suit for card in player.hand]}")
        if len(player.split_hand) > 0:
            print(f"{player.name}: {[str(card.name) + ' of ' + card.suit for card in player.split_hand]}")
        print(f"Value: {get_hands_result(player.hand)}")
    else:
        print(f"{player.name}: {[str(card.name) + ' of ' + card.suit for card in player.hand[1:]]}")
