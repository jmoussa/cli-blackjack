pot = {"ones": 0, "fives": 0, "tens": 0, "twentys": 0, "fiftys": 0}


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

    def place_bet(self, pot: dict, ones: int = 0, fives: int = 0, tens: int = 0, twentys: int = 0, fiftys: int = 0):
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
        return (
            f"""
            Betting: ---------------
            1s  : {bet_amount_ones}
            5s  : {bet_amount_fives}
            10s : {bet_amount_tens}
            20s : {bet_amount_twentys}
            50s : {bet_amount_fiftys}
            ----------------------
            """,
            pot,
        )

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
