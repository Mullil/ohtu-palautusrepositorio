import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    def test_search_finds_correct_player(self):
        player = self.stats.search("Gretzky")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")

    def test_search_returns_none_if_not_found(self):
        player = self.stats.search("123abc")
        self.assertIsNone(player)

    def test_team_returns_all_players_from_team(self):
        EDM_players = self.stats.team("EDM")
        names = [p.name for p in EDM_players]
        self.assertEqual(sorted(names), sorted(["Semenko", "Kurri", "Gretzky"]))

    def test_team_returns_empty_list_if_no_players(self):
        no_players = self.stats.team("a")
        self.assertEqual(no_players, [])

    def test_top_points_returns_correct_order(self):
        top_players = self.stats.top(2, SortBy.POINTS)
        self.assertEqual(len(top_players), 3)
        points = [p.points for p in top_players]
        self.assertEqual(points, sorted(points, reverse=True))
        self.assertEqual(top_players[0].name, "Gretzky")

    def test_top_goals_returns_correct_order(self):
        top_players = self.stats.top(1, SortBy.GOALS)
        self.assertEqual(len(top_players), 2)
        goals = [p.goals for p in top_players]
        self.assertEqual(goals, sorted(goals, reverse=True))
        self.assertEqual(top_players[0].name, "Lemieux")

    def test_top_assists_returns_correct_order(self):
        top_players = self.stats.top(0, SortBy.ASSISTS)
        self.assertEqual(len(top_players), 1)
        assists = [p.assists for p in top_players]
        self.assertEqual(assists, sorted(assists, reverse=True))
        self.assertEqual(top_players[0].name, "Gretzky")

    