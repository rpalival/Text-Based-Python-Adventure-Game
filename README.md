# Text-Based Adventure Game
[![Run Tests CI](https://github.com/rpalival/cs515-project2/actions/workflows/test.yml/badge.svg)](https://github.com/rpalival/cs515-project2/actions/workflows/test.yml)
## Author
- **Name**: Raj Palival
- **Stevens Login**: rpalival@stevens.edu
- **GitHub URL**: [GitHub Repository](https://github.com/rpalival/cs515-project2)

## Project Time Estimation
- Estimated Time: 30 hours

## Testing Methodology
The script `adventure.py` is executed using the `subprocess.run` function in Python, which allows the execution of a separate program (in this case, the script) from within the Python testing script. Here's how it's being done:

- **Command Construction**: The command to execute `adventure.py` is constructed, including the path to the Python executable (retrieved using `sys.executable` to ensure compatibility across different environments), the script name (`adventure.py`), and the additional argument `map_file` (`loop.map`).

- **Running the Script with Test Input**: The `subprocess.run` function is used to run this command with test inputs.

- **Capturing the Output**: The output generated by the script during its execution (what would normally appear on the console) is captured for comparison with the expected output.

- **Error Handling**: If the script encounters an error during execution, it will be captured in `completed_process.stderr` or may raise an exception. These errors are handled and reported in the test results.

By using `subprocess.run`, the testing framework can automate the execution of `adventure.py` with various inputs, capture its outputs, and compare these outputs with expected results to determine if the script behaves as intended.

## Known Issues
- While implementing the "Abbreviations for Verbs, Directions, and Items" extension, I faced challenges with consistency across all commands and items, leading to an inconsistent player experience and different output. Therefore, I chose to implement other extensions.

## Example of Issue Resolution
### Lack of Exit Command in Input Files
- Automated tests use `.in` files to simulate user inputs. If these files don't end with an exit command like 'quit', the game script keeps waiting for more input and doesn't terminate as expected. This causes the script to be stuck in an infinite loop during automated tests.
- **Solution**: Updated input files to ensure each `.in` file ends with a 'quit' or similar exit command.

### Improper Handling of 'Quit' Command
- The main loop in `adventure.py` script, which processes user input, did not correctly handle the 'quit' command. Even if 'quit' was entered, the loop didn't break due to a bug or oversight, leading the script to run indefinitely.
- **Solution**: Modified the game script to properly recognize and respond to the 'quit' command, allowing the main loop to break and the script to end gracefully.

## Implemented Extensions
### 1. Help Command
- **New Verb/Feature**: The "help" command is a new feature that provides players with information about available commands and their descriptions.
- **Exercise**: Players can type "help" during gameplay to view a list of available commands along with their descriptions. Help texts are generated dynamically from the commands dictionary.
- **Test Files**: `help.in` and `help.out` tests are included for reference.
- **example**:
if you enter "help," it will show a list like this:
You can run the following commands:
- go - Move in a direction and enter a new room
- get - Pick up an item and place it in your inventory
- look - Look around to know which room you are chilling in
- inventory - Show your current inventory
- quit - Quit the game, it's not your cuppa tea
- help - Show this help message to know what commands you can use!
- drop - Drop an item from your inventory into the current room

    help texts are generated by iterating through the commands dictionary and extracting the verb descriptions. This way, whenever you add or modify a command in the command list, it will       automatically be included in the help text without requiring manual updates.
    NOTE: I have added help.in and help.out tests for reference



### 2. Win or Lose Conditions
- **New Verb/Feature**: Added win and lose conditions to the game. These conditions determine when the player wins or loses the game and exits the game based on the items in their inventory before entering specific rooms (e.g., Beast Titan's Lair).
- **Exercise**: Players must collect specific items to trigger a win condition or avoid certain items to prevent a lose condition before entering the designated room.
- **Location in the Map**: Win and lose conditions are defined within specific rooms in the game map. Test files `win.in`, `win.out`, `lose.in`, and `lose.out` are included for reference.
**the fastest winning condition for my map is:**
- go north
- get 3d maneuver gear
- go east
- get blade
- go west
- go south
- go east
- go north
- go east
- get light crystal
- go north
- inventory
- go north
**the fastest losing condition is:**
- go east
- go north
- go east
- go north
- go north
- 
**the winning and losing conditions are mentioned in the loop.map file**
 {
    "name": "Beast Titan's Lair",
    "desc": "The ominous lair of the Beast Titan. The walls echo with the sounds of past battles and whispered secrets.",
    "exits": {"north": 0},
    "win_condition": ["3d maneuver gear", "blade", "light crystal"],
    "lose_condition": []
 }


### 3. Drop Command
- **New Verb/Feature**: The "drop" command allows players to drop items from their inventory into the current room.
- **Exercise**: Players can type "drop [item]" during gameplay to remove an item from their inventory and place it in the current room.
- **Location in the Map**: The "drop" command operates wherever the player is located. Test files `drop.in` and `drop.out` are included for reference.
