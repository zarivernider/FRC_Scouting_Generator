import requests as rq
import re
from BlueAllianceAuthKey import TBA_Read_Auth_Key

class BlueAllianceAPI:

    # Class to perform API calls to the Blue Alliance

    # Base URL for the API to reach the blue alliance
    base_url = "https://www.thebluealliance.com/api/v3"
    # Headers for the API call
        # X-TBA-Auth-Key : Authentication key to access the blue alliance
    headers = {"X-TBA-Auth-Key" : TBA_Read_Auth_Key}

    # Event key for the competition. Example here will be overwritten in constructor
    event_key = "2024mabri"
    # Year to pull data from. Example here will be overwritten in constructor
    year = 2024

    # Lambda function to assure that all numbers are keys to properly query the API
    team_numb_to_key = lambda self, inp : inp if re.search(f"frc", inp)  else f"frc{inp}"

    # Generate constructor
    def __init__(self, event_key : str, year : int) -> None:
        self.event_key = event_key
        self.year = year

    # Send the GET to the API. Include the "/" in param
    def _getAPI(self, url_addendum : str):
        response =  rq.get(f"{self.base_url}{url_addendum}", headers=self.headers)
        if response.status_code == 200:
            return response
        else: 
            raise Exception(f"Response returns error code: {response.status_code} because {response.text}")

    # Get the basic data from the team. Location, name, school, etc.
    def getTeamData(self, team_numb : str):
        # If a team number is inputted, but not a key. Make it a key
        team_numb = self.team_numb_to_key(team_numb)
        team_data = self._getAPI(f"/team/{team_numb}")
        return team_data

    # Get the team event data. It is the simplified match data for a team at an event
    def getTeamEventData(self, team_numb : str):
        # If a team number is inputted, but not a key. Make it a key
        team_numb = self.team_numb_to_key(team_numb)
        match_data = self._getAPI(f"/team/{team_numb}/event/{self.event_key}/matches/simple")
        return match_data

    # Get a list of all the teams at an event
    def getEventTeams(self) -> list:
        all_teams = self._getAPI(f"/event/{self.event_key}/teams")
        return all_teams.json()
    
    # Get a dictionary where the keys are the event key and the value is the return data struct
    # Has a multitude of information including statistics, performance, and achievements. 
    def getTeamStats(self, team_numb: str) -> dict:
        team_numb = self.team_numb_to_key(team_numb)
        team_status = self._getAPI(f"/team/{team_numb}/events/{self.year}/statuses")
        return team_status
