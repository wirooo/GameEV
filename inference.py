from scraping import UggChampScraper

class GameInference:
    """
    Calculates the win rate of a champion, adjusting for additional factors \
        (matchups, duos, etc.) using Bayesian inference
    """
    total_games: int
    total_wr: float
    adjusted_wr: float
    web_scraper: UggChampScraper

    def __init__(self, champion: str) -> None:
        self.champion = champion.lower().strip()
        self.web_scraper = UggChampScraper(self.champion)
        stats = self.web_scraper.get_stats()
        self.total_games = stats.games
        self.total_wr = stats.wr
        self.adjusted_wr = self.total_wr

    def add_duo(self, champion: str) -> None:
        duo_stats = self.web_scraper.get_duo_stats(champion)
        self.add_factor(duo_stats.wr, duo_stats.games)

    def add_matchup(self, champion: str) -> None:
        matchup_stats = self.web_scraper.get_matchup_stats(champion)
        self.add_factor(matchup_stats.wr, matchup_stats.games)
        
    def add_factor(self, factor_wr: float, factor_games: float) -> None: 
        """
        Updates self.adjusted_wr given new information of win rate and sample size
        """
        self.adjusted_wr = GameInference.bayesian_posterior(
            likelihood = self.get_likelihood(factor_wr, factor_games),
            prior = self.adjusted_wr,
            marginal = self.get_marginal(factor_games)
        )

    def get_likelihood(self, wr_w_other: float, games_w_other: float) -> float:
        """
        Calculate likelihood probability (P(E|H)) given win rate and sample size of other factor
        """
        total_games_won = self.total_wr * self.total_games
        games_won_w_other = wr_w_other * games_w_other
        return games_won_w_other / total_games_won

    def get_marginal(self, games_w_other: float) -> float:
        """
        Calculate marginal probability (P(E)) given win rate and sample size of other factor
        """
        return games_w_other / self.total_games

    def get_wr(self) -> float:
        return self.adjusted_wr

    @staticmethod
    def bayesian_posterior(likelihood: float, prior: float, marginal: float) -> float:
        """
        Calculate the posterior probability using Bayes' Theorem: P(H|E) = (P(E|H)P(H))/P(E)
        """
        return likelihood * prior / marginal
        
