import requests
from rich.table import Table
from rich.console import Console

class PlayerReader:
    def __new__(self, url):
        response = requests.get(url).json()
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = []
    
    def top_scorers_by_nationality(self, nationality):
        for player in sorted(
            filter(lambda player: player.nationality == nationality, self.reader),
            key=lambda x: x.points, reverse=True):
            self.players.append(player)
        return self.players
    
    def display_players(players, nationality):
        console = Console()
        table = Table(title=f"Top {nationality} players")

        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Team", justify="center", style="magenta")
        table.add_column("Goals", justify="right", style="green")
        table.add_column("Assists", justify="right", style="yellow")
        table.add_column("Points", justify="right", style="bold white")

        for p in players:
            table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(p.points))

        console.print(table)


class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.goals = dict['goals']
        self.assists = dict['assists']
        self.team = dict['team']
        self.points = self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team:20} {self.goals} + {self.assists} = {self.points}"
