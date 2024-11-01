import json
import random
import requests
import time

def fetch_player_ids(league_ids):
    managers = []
    seen_manager_ids = set()

    for league_id in league_ids:

        page = 1
        has_next = True

        while has_next:
            url = f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}'
            response = requests.get(url)
            data = response.json()

            standings = data['standings']['results']

            for entry in standings:
                manager_name = entry['player_name']
                manager_id = entry['entry']

                if manager_id not in seen_manager_ids:
                    manager = {
                        'manager_id': manager_id,
                        'manager_name': manager_name,
                        'gameweek_history': [],
                        'player_picks': []
                    }

                    managers.append(manager)
                    seen_manager_ids.add(manager_id)

            has_next = data['standings']['has_next']
            page += 1

        sleeptime = random.randint(1, 3)
        time.sleep(sleeptime)

    return managers

def fetch_manager_history_and_picks(managers, gameweek):
    for manager in managers[:1]:
        manager_id = manager['manager_id']

        url = f'https://fantasy.premierleague.com/api/entry/{manager_id}/history/'
        response = requests.get(url)
        data = response.json()
        
        gameweeks = data['current']
        gameweek_history = []

        for gw in gameweeks:
            gameweek = gw['event']
            points = gw['points']

            gameweek_data = {
                "gameweek": gameweek,
                "points": points
            }

            gameweek_history.append(gameweek_data)

        manager['gameweek_history'] = gameweek_history

        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)

        url = f'https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/'
        response = requests.get(url)
        data = response.json()

        players = data['picks']
        players_data = []

        for player in players:
            player_id = player['element']
            position = player['position']
            multiplier = player['multiplier']

            player_data = {
                "player_id": player_id,
                "position": position,
                "multiplier": multiplier
            }

            players_data.append(player_data)

        manager['player_picks'] = players_data

        print(manager)

def main():
    with open('../data/options.json') as f:
        options = json.load(f)

    fetch_data = options.get("fetch_data", True)
    if fetch_data == True:
        league_ids = options.get("league_ids")
        managers = fetch_player_ids(league_ids)

        with open('../data/managers.json', 'w') as f:
            json.dump(managers, f, indent=4)

    with open('../data/managers.json') as f:
        managers = json.load(f)

    gameweek = options.get("gameweek")

    # This should be done in the other loop when done
    managers = fetch_manager_history_and_picks(managers, gameweek)
    
if __name__ == "__main__":
    main()