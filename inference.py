class GameInference:
    total_games: int
    total_wr: float
    total_pr: float
    adjusted_wr: float

    def __init__(self, champion: str) -> None:
        # scrape web here
        self.total_games = 92573
        self.total_wr = 0.4843
        self.total_pr = 0.062
        self.adjusted_wr = self.total_wr

    def add_duo(self, champion: str) -> None:
        # scrape here
        duo_wr = 0.5283
        duo_games = 1039

        self.add_factor(duo_wr, duo_games)

    def add_matchup(self, champion: str) -> None:
        # scrape here
        matchup_wr = 0.4701
        matchup_games = 1839

        self.add_factor(matchup_wr, matchup_games)
        
    def add_factor(self, factor_wr, factor_games) -> None: 
        self.adjusted_wr = GameInference.bayesian_posterior(
            likelihood = self.get_likelihood(factor_wr, factor_games),
            prior = self.adjusted_wr,
            marginal = self.get_marginal(factor_games)
        )

    def get_likelihood(self, wr_w_other: float, games_w_other: float) -> float:
        total_games_won = self.total_wr * self.total_games
        games_won_w_other = wr_w_other * games_w_other
        return games_won_w_other / total_games_won

    def get_marginal(self, games_w_other: float) -> float:
        return games_w_other / self.total_games

    def get_wr(self) -> float:
        return self.adjusted_wr

    @staticmethod
    def bayesian_posterior(likelihood: float, prior: float, marginal: float) -> float:
        return likelihood * prior / marginal

    
        