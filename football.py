from datetime import datetime as dt, timedelta
import requests
import os
import pandas
from dotenv import load_dotenv
load_dotenv()

year = int(dt.now().strftime("%Y"))
month = int(dt.now().strftime("%m"))
if month < 6:
    year -= 1
year = str(year)


day = dt.now().strftime("%Y-%m-%d")
seven_days_ago = (dt.now() - timedelta(days=7)).strftime("%Y-%m-%d")

headers = {
    "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
    "X-RapidAPI-Host": os.getenv("X-RapidAPI-Host")
}


class Football:
    def __init__(self):
        self.PL = 39
        self.LA_LIGA = 140
        self.SERIE_A = 135
        self.BUNDESLIGA = 78
        self.EFL = 46
        self.FA_CUP = 45
        self.EUROPA = 3
        self.UCL = 2
        self.SEASON = year
        self.FOOTBALL_URL = "https://api-football-v1.p.rapidapi.com/v3/"

    def get_fixtures(self, league):
        querystring = {"date": day, "league": league, "season": self.SEASON}
        res = requests.get(url=f"{self.FOOTBALL_URL}fixtures",
                           headers=headers, params=querystring)
        res.raise_for_status()
        data = res.json()
        fixture_list = data.get("response", [])

        def get_fixture_info(fixtures):
            return "\n\n\n\n".join([
                f"{dt.fromisoformat(fix['fixture']['date']).strftime('%B %d %Y')}\n\n"
                f"Match Time: {dt.fromisoformat(fix['fixture']['date']).strftime('%H:%M')}\n"
                f"Referee in Charge: {fix['fixture']['referee']}\n"
                f"Venue: {fix['fixture']['venue']['name']}\n"
                f"Status: {fix['fixture']['status']['long']}\n"
                f"Time Elapsed: {fix['fixture']['status']['elapsed']}\n"
                f"Competition: {fix['league']['name']} - Season {fix['league']['season']} - {fix['league']['round']} Gameweek\n"
                f"{fix['teams']['home']['name']} - {fix['goals']['home']}:{fix['goals']['away']} - {fix['teams']['away']['name']}"
                for fix in fixtures
            ])
        if not fixture_list:
            querystring = {"league": league, "season": self.SEASON,
                           "from": seven_days_ago, "to": day}
            res = requests.get(url=self.FOOTBALL_URL + "fixtures",
                               headers=headers, params=querystring)
            res.raise_for_status()
            old_fixtures = res.json().get("response", [])
            return f"There are no fixtures today in the league but here are the fixtures from last week.\n\n\n\n\n{get_fixture_info(old_fixtures)}"
        else:
            return get_fixture_info(fixture_list)

    def get_table(self, league):
        team_name_replacements = {
            "Manchester": "Man",
            "Nottingham": "Nott",
            "Crystal Palace": "Palace",
            "Sheffield Utd": "Sheffield",
            "Rayo Vallecano": "Rayo",
            "Real Sociedad": "Sociedad",
            "Borussia Dortmund": "Dortmund",
            "Union Berlin": "Un-Berlin",
            "Eintracht Frankfurt": "Eintracht",
            "Bayern Munich": "Bayern",
            "Bayer Leverkusen": "Leverkusen",
            "Werder Bremen": "Bremen",
            "VfL Wolfsburg": "Wolfsburg",
            "Borussia Monchengladbach": "B-Gladbach",
            "1899 Hoffenheim": "Hoffenheim",
            "VfB Stuttgart": "Stuttgart",
            "SV Darmstadt 98": "Darmstadt",
            "Atletico Madrid": "Atletico",
            "FC Heidenheim": "Heidenheim"
        }
        standings = ""
        querystring = {"league": league, "season": self.SEASON}
        res = requests.get(url=self.FOOTBALL_URL + "standings",
                           headers=headers, params=querystring)
        res.raise_for_status()
        data = res.json()
        league_table = data["response"][0]["league"]
        league_name = league_table["name"]
        league_season = league_table["season"]
        league_member = league_table["standings"][0]
        standings += f"{league_name}-{league_season}\n\n"
        combined_df = []
        for team in league_member:
            rank = team["rank"]
            team_name = team["team"]["name"]

            for find, replace in team_name_replacements.items():
                team_name = team_name.replace(find, replace)
            team_points = team["points"]
            goal_diff = team["goalsDiff"]
            match_played = team["all"]["played"]
            match_won = team["all"]["win"]
            match_draw = team["all"]["draw"]
            match_lost = team["all"]["lose"]
            goals_for = team["all"]["goals"]["for"]
            goals_against = team["all"]["goals"]["against"]
            d = {"Team": team_name, "P": match_played, "W": match_won, "D": match_draw,
                 "L": match_lost, "+": goals_for, "-": goals_against, "GD": goal_diff, "PTS": team_points}
            df = pandas.DataFrame(data=d, index=[rank])
            combined_df.append(df)
        league_standings = pandas.concat(combined_df)
        output = standings+league_standings.to_string()
        return output


ball = Football()
print(ball.get_fixtures(ball.PL))
