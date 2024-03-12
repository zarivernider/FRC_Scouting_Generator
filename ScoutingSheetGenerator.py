from BlueAllianceAPI_Interface import BlueAllianceAPI
import pandas as pd
import re
from copy import deepcopy

# Year to pull data from
year = 2024
# Event key. Name can be found in URL when looking at the event on the Blue Alliance website
event = "2024mawne"
# File to load w relative path
base_question_path = f"Templates/{year}_SheetToDuplicate.csv"
# Create instance of the API calling
api = BlueAllianceAPI(event, year)
# Name for the output file
output_file = f"{year}_{event}"

# Outline for the header information. Format as a row
base_header_info = ["Team Number", "Name", "Location"]
# Outline for the different events. Format as columns
base_event_info = [["Event Key"], ["Event Link"], ["Event Results"], []]

# Remove the HTML bold syntac from the output description
def filterEventData(inp_str):
    # For each HTML bold syntax, replace with an empty string
    output = re.sub("<b>", "", inp_str)
    output = re.sub("</b>", "", output)
    return output

# List to hold all dataframes of each team
team_dataframes = []

# Get the list of all teams at an event
all_teams = api.getEventTeams()
# Sort by integers not string
all_teams.sort(key=lambda x: int(x["team_number"]))
# Generate a dataframe per each team
for team_info in all_teams:
    # Pull the key for the team
    team_key = team_info['key']
    # Get the number for the team (as a str)
    team_number = str(team_info["team_number"])

    # Get the data for the team at the event
    team_matches = api.getTeamEventData(team_key).json()
    # Generate the row of matches. Start with nothing to offset the columns
    match_list = [None]
    # Sort the team matches by integer and not strings
    team_matches.sort(key = lambda x : int(x["match_number"]))
    # Form the match list with properly named matches
    [match_list.append(f"Match {number}") for number in team_matches]

    # Form the dataframe for the base questions
    base_question_df = pd.read_csv(base_question_path, header=None)
    # Create a base dataframe that holds the questions and the match list
    base_df = pd.concat([pd.DataFrame([match_list]), base_question_df])

    # Form the dataframe for the header data 
    header_data = [team_number, 
                   team_info['nickname'], 
                   f"{team_info['city']}, {team_info['state_prov']}"]
    header_df = pd.DataFrame([base_header_info, header_data, []])

    # Start with an empty row as a buffer to not scrunch up the data
    # Create a datatype to hold the 
    team_stat_data = [[]]
    # Get all of the team stats for the given team
    team_stats = api.getTeamStats(team_key).json()
    # Iterate through the data from each event the team is registered for
    for event_key, event in team_stats.items():
        # Create a copy since lists are mutable
        temp_stat_data = deepcopy(base_event_info)
        # Form information for an event
        event_data = [event_key, f"https://www.thebluealliance.com/event/{event_key}", 
                    filterEventData(event['overall_status_str'])]
        # Loop through the event data and append in real time. Needed for proper formatting
        for idx, elem in enumerate(event_data):
            temp_stat_data[idx].append(elem)
        
        # Append the data so that the data is setup as columns
        [team_stat_data.append(data) for data in temp_stat_data.copy()]

    # Generate a dataframe for all of the stats for the team from previous comps this season
    team_stat_df = pd.DataFrame(team_stat_data)

    # Create a complete dataframe from all the gathered information
    team_df = pd.concat([header_df, base_df, team_stat_df])

    # Append to the complete list of dataframes that will later be printed to excel
    team_dataframes.append([team_number, team_df])
    
    # Alert the user of the status for the system
    print(f"Added team {team_number}")


# Generate excel writer to form a writers
with pd.ExcelWriter(f'{output_file}.xlsx', engine='xlsxwriter') as writer:
    # Create a sheet for each team
    for team_numb, df in team_dataframes:
        # Do not print the headers or index
        df.to_excel(writer, sheet_name=team_numb, header=False, index=False)
