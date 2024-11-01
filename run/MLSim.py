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

def main():
    with open('../data/options.json') as f:
        options = json.load(f)

    fetch_data = options.get("fetch_data")
    print(fetch_data)

    league_ids = options.get("league_ids")

    managers = fetch_player_ids(league_ids)
    with open('../data/managers.json', 'w') as f:
        json.dump(managers, f, indent=4)
        print("Created managers json file")

    for manager in managers:
        print(manager)
    
if __name__ == "__main__":
    main()