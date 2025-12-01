class TennisGame:
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    ADVANTAGE_LIMIT = 4

    SCORE_NAMES = {
        LOVE: "Love",
        FIFTEEN: "Fifteen",
        THIRTY: "Thirty",
        FORTY: "Forty"
    }

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            return self.handle_even()

        elif self.advantage():
            return self.handle_advantage()
        else:
            return f"{self.SCORE_NAMES.get(self.m_score1)}-{self.SCORE_NAMES.get(self.m_score2)}"

    def handle_even(self):
        if self.m_score1 < self.FORTY:
            return f"{self.SCORE_NAMES.get(self.m_score1)}-All"
        else:
            return "Deuce"
        
    def advantage(self):
        return self.m_score1 >= self.ADVANTAGE_LIMIT or self.m_score2 >= self.ADVANTAGE_LIMIT
        
    def handle_advantage(self):
        minus_result = self.m_score1 - self. m_score2
        if minus_result == 1:
            return f"Advantage {self.player1_name}"
        elif minus_result == -1:
            return f"Advantage {self.player2_name}"
        elif minus_result >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"