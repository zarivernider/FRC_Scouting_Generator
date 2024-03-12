# FRC_Scouting_Generator
Generate an excel spreadsheet of competition information to help teams scout.

# Setup Instructions
ToDo

# How to Use
ToDo

# Known Limitations
1. `BlueAllianceAPI_Interface.py` does not support multiple pages or any other header information than the bare minimum. Should not be an issue, but worth noting the tech debt.
2. `ScoutingSheetGenerator.py` does inefficient pandas operations that inhibit performance. Not refactored since timing is not critical for its operation.