from BlueAllianceAPI_Interface import BlueAllianceAPI
import pandas as pd
import re
from copy import deepcopy
from pandas.io.formats import excel

year = 2024
event = "2024mawne"
# File to load w relative path
base_question_path = f"Templates/{year}_SheetToDuplicate.CSV"
api = BlueAllianceAPI(event, year)

output_file = f"{year}_{event}"
# strip key
# strip_team_key = lambda inp : re.sub("frc", "", inp)
base_header_info = ["Team Number", "Name", "Location"]
base_event_info = [["Event Key"], ["Event Link"], ["Event Results"], []]

# Refine team data
def filterEventData(inp_str):
    output = re.sub("<b>", "", inp_str)
    output = re.sub("</b>", "", output)
    return output

team_dataframes = []

# team_key = "61"
all_teams = api.getEventTeams()
sorted_teams = [[int(team["team_number"]), team] for team in all_teams]
sorted_teams.sort(key=lambda x: x[0])
for team_number, team_info in sorted_teams:
    team_key = team_info['key']
    # Convert back to a string after sorting
    team_number = str(team_number)
# team_info = api.getTeamData(team_key).json()

    team_matches = api.getTeamEventData(team_key).json()
    match_list = [None]
    # Numerate the matches
    sorted_matches = [int(elem["match_number"]) for elem in team_matches]
    sorted_matches.sort()
    [match_list.append(f"Match {number}") for number in sorted_matches]

    base_question_df = pd.read_csv(base_question_path, header=None)
    base_df = pd.concat([pd.DataFrame([match_list]), base_question_df])

    header_data = [team_number, team_info['nickname'], f"{team_info['city']}, {team_info['state_prov']}"]
    header_df = pd.DataFrame([base_header_info, header_data, []])

    # Start with an empty row as a buffer
    team_stat_data = [[]]
    team_stats = api.getTeamStats(team_key).json()
    for event_key, event in team_stats.items():
        # Create a mutable copy
        temp_stat_data = deepcopy(base_event_info)
        # Form data info
        event_data = [event_key, f"https://www.thebluealliance.com/event/{event_key}", 
                    filterEventData(event['overall_status_str'])]
        for idx, elem in enumerate(event_data):
            temp_stat_data[idx].append(elem)
        
        [team_stat_data.append(data) for data in temp_stat_data.copy()]

    team_stat_df = pd.DataFrame(team_stat_data)

    team_df = pd.concat([header_df, base_df, team_stat_df])

    team_dataframes.append([team_number, team_df])
    print(f"Added team {team_number}")

# team_df.to_csv('test.csv', index=False, header=False)  
# pip install xslxwriter
# excel.ExcelFormatter.header_style = None

with pd.ExcelWriter(f'{output_file}.xlsx', engine='xlsxwriter') as writer:
    for team_numb, df in team_dataframes:
        df.to_excel(writer, sheet_name=team_numb, header=False, index=False)







# Logical steps: 
    # Generate one sample page
    # Gen the rest


