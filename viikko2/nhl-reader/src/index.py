from player import PlayerReader, PlayerStats

def main():
    season = input("Anna kausi: ").strip()
    nationality = input("Anna kansallisuus: ").strip()
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)
    PlayerStats.display_players(players, nationality)

if __name__ == "__main__":
    main()
