from datetime import datetime as dt
import requests
import os
import pandas
from dotenv import load_dotenv
load_dotenv()

year = int(dt.now().strftime("%Y"))
month = int(dt.now().strftime("%m"))
if month < 6:
    year += 1
year = str(year)


day = dt.now().strftime("%Y-%m-%d")


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
        self.FOOTBAL_URL = "https://api-football-v1.p.rapidapi.com/v3/"

    def get_fixtures(self, league):
        fixtures = ""
        querystring = {"date": day, "league": league, "season": self.SEASON}
        res = requests.get(url=self.FOOTBAL_URL + "fixtures",
                           headers=headers, params=querystring)
        res.raise_for_status()
        data = res.json()
        fixture_list = data["response"]
        for fix in fixture_list:
            time = dt.fromisoformat(fix["fixture"]["date"]).strftime("%H:%M")
            referee = fix["fixture"]["referee"]
            venue = fix["fixture"]["venue"]["name"]
            status = fix["fixture"]["status"]["long"]
            elapsed = fix["fixture"]["status"]["elapsed"]
            comp = fix["league"]["name"]
            season = fix["league"]["season"]
            gameweek = fix["league"]["round"]
            home_team = fix["teams"]["home"]["name"]
            away_team = fix["teams"]["away"]["name"]
            home_goals = fix["goals"]["home"]
            away_goals = fix["goals"]["away"]
            fixtures += f"Match Time: {time}\nReferee in Charge: {referee}\nVenue: {venue}\nStatus: {status}\nTime Elapsed: {elapsed}\nCompetition: {comp} - Season {season} - Round {gameweek}\n{home_team}- {home_goals}:{away_goals} -{away_team}\n\n\n"
        return fixtures

    def get_table(self, league):
        standings = ""
        querystring = {"league": league, "season": self.SEASON}
        res = requests.get(url=self.FOOTBAL_URL + "standings",
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
            if "Manchester" in team_name:
                team_name = team_name.replace("Manchester", "Man")
            elif "Nottingham" in team_name:
                team_name = team_name.replace("Nottingham", "Nott")
            elif "Crystal Palace" in team_name:
                team_name = team_name.replace("Crystal", "")
            elif "Sheffield Utd" in team_name:
                team_name = team_name.replace("Sheffield Utd", "Sheffield")
            elif "Rayo Vallecano" in team_name:
                team_name = team_name.replace("Rayo Vallecano", "Rayo")
            elif "Real Sociedad" in team_name:
                team_name = team_name.replace("Real Sociedad", "Sociedad")
            elif "Borussia Dortmund" in team_name:
                team_name = team_name.replace("Borussia Dortmund", "Dortmund")
            elif "Union Berlin" in team_name:
                team_name = team_name.replace("Union Berlin", "Un-Berlin")
            elif "Eintracht Frankfurt" in team_name:
                team_name = team_name.replace(
                    "Eintracht Frankfurt", "Eintracht")
            elif "Bayern Munich" in team_name:
                team_name = team_name.replace("Bayern Munich", "Bayern")
            elif "Bayer Leverkusen" in team_name:
                team_name = team_name.replace("Bayer Leverkusen", "Leverkusen")
            elif "Werder Bremen" in team_name:
                team_name = team_name.replace("Werder Bremen", "Bremen")
            elif "VfL Wolfsburg" in team_name:
                team_name = team_name.replace("VfL Wolfsburg", "Wolfsburg")
            elif "Borussia Monchengladbach" in team_name:
                team_name = team_name.replace(
                    "Borussia Monchengladbach", "B-Gladbach")
            elif "1899 Hoffenheim" in team_name:
                team_name = team_name.replace("1899 Hoffenheim", "Hoffenheim")
            elif "VfB Stuttgart" in team_name:
                team_name = team_name.replace("VfB Stuttgart", "Stuttgart")
            elif "SV Darmstadt 98" in team_name:
                team_name = team_name.replace("SV Darmstadt 98", "Darmstadt")
            elif "FC Heidenheim" in team_name:
                team_name = team_name.replace("FC Heidenheim", "Heidenheim")
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
