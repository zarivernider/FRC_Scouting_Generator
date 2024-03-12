import requests as rq
import re

class BlueAllianceAPI:
    # Base URL to reach the blue alliance
    base_url = "https://www.thebluealliance.com/api/v3"
    # Authentication headers
    headers = {"X-TBA-Auth-Key" : "1jqi04hmw6UnW7UG6Z0vYZBnwR1qr9ZxtEsPnEv5EdHqxRvOz9lUAuu7582FzAPs"}

    event_key = "2024mabri"
    year = 2024
    team_numb_to_key = lambda self, inp : inp if re.search(f"frc", inp)  else f"frc{inp}"

    # Generate constructor
    def __init__(self, event_key : str, year : int) -> None:
        self.event_key = event_key
        self.year = year

    # Send the GET to the API. Include the "/" in param
    def _getAPI(self, url_addendum : str):
        response =  rq.get(f"{self.base_url}{url_addendum}", headers=self.headers)
        # TODO Add header handling / learning

        #TODO Investigate worth adding exceeding a page
        if response.status_code == 200:
            return response
        else: 
            raise Exception(f"Response returns error code: {response.status_code} because {response.text}")

    def getTeamData(self, team_numb : str):
        # If a team number is inputted, but not a key. Make it a key
        team_numb = self.team_numb_to_key(team_numb)
        team_data = self._getAPI(f"/team/{team_numb}")
        return team_data

    def getTeamEventData(self, team_numb : str):
        # If a team number is inputted, but not a key. Make it a key
        team_numb = self.team_numb_to_key(team_numb)
        match_data = self._getAPI(f"/team/{team_numb}/event/{self.event_key}/matches/simple")
        return match_data

    def getEventTeams(self) -> list:
        all_teams = self._getAPI(f"/event/{self.event_key}/teams")
        return all_teams.json()
    
    def getTeamStats(self, team_numb: str) -> dict:
        team_numb = self.team_numb_to_key(team_numb)
        team_status = self._getAPI(f"/team/{team_numb}/events/{self.year}/statuses")
        return team_status

# api = BlueAllianceAPI()

# api._getTeamData("61")

