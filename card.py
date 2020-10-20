class Card:
    def __init__(self, name, suit):
        value_mapping = {"ace": (11, 1), "king": 10, "queen": 10, "jack": 10}
        self.name = name
        self.value = name if name not in ("ace", "king", "queen", "jack") else value_mapping[name]
        self.suit = suit
        self.color = "red" if self.suit in ("heart", "diamonds") else "black"
