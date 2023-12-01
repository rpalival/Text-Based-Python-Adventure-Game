import json
import sys

class AdventureGame:
    class CommandInfo:
        def __init__(self, target, description):
            self.target = target
            self.description = description
    
    commands = {
        'go': CommandInfo(True, 'Move in a direction and enter a new room'),
        'get': CommandInfo(True, 'Pick up an item and place it in your inventory'),
        'look': CommandInfo(False, "Look around to know which room you are chilling in"),
        'inventory': CommandInfo(False, 'Show your current inventory'),
        'quit': CommandInfo(False, "Quit the game, it's not your cuppa tea"),
        'help': CommandInfo(False, 'Show this help message to know what commands you can use!'),
        'drop': CommandInfo(True, "Drop an item from your inventory into the current room")
        # Add more commands as needed
    }

    def reset_game(self):
        # Reset the game state to its initial settings
        self.map = self.load_map(self.map_file)  # Reload the map
        self.player_location = 0
        self.player_inventory = []

    def __init__(self, map_file):
        self.map_file = map_file
        self.map = self.load_map(map_file)
        self.player_location = 0
        self.player_inventory = []

    def show_help(self):
        print("You can run the following commands:")
        for command, info in AdventureGame.commands.items():
            command_format = f"{command} ..." if info.target else command
            print(f"  {command_format} - {info.description}")

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: File '{filename}' is not a valid JSON file.")
        return None

    def start_game(self):
        # This function starts the game loop.
        self.show_current_room()
        while True:
            try:
                command = input("What would you like to do? ")
                command = ' '.join(command.strip().lower().split())  # Cleaning the input command
                if command == "quit":
                    print("Goodbye!")
                    break
                else:
                    self.process_command(command)
                    
            except EOFError:
                print("\nUse 'quit' to exit.")  # EOF (Ctrl-D) handling

            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")  # Keyboard Interrupt (Ctrl-C) handling
                break
    

    def show_current_room(self):
        # Display the current room's details, including items if any.
        room = self.map[self.player_location]
        print(f"\n> {room['name']}\n\n{room['desc']}\n")
        if "items" in room and room["items"]:
            items = ", ".join(room["items"])
            print(f"Items: {items}\n")
        exits = " ".join(room["exits"].keys())
        print(f"Exits: {exits}\n")

    def process_command(self, command):
        # This function processes the player's command.
        command_statement = command.split()
        verb = command_statement[0] if command_statement else ''

        if verb in AdventureGame.commands:
            if verb == "go":
                if len(command_statement) > 1:
                    direction = command_statement[1]
                    self.move(direction)
                else:
                    print("Sorry, you need to 'go' somewhere.")

            elif verb == "help":
                self.show_help()

            elif verb == "look":
                self.show_current_room()

            elif verb == "get":
                if len(command_statement) > 1:
                    item = ' '.join(command_statement[1:])
                    self.get_item(item)
                else:
                    print("Sorry, you need to 'get' something.")

            elif verb == "drop":
                if len(command_statement) > 1:
                    item = ' '.join(command_statement[1:])
                    self.drop_item(item)
                else:
                    print("Sorry, you need to 'drop' something.")

            elif verb == "inventory":
                self.show_inventory()
        else:
            print("I don't understand that command.")

    def check_win_lose_conditions(self):
        current_room = self.map[self.player_location]
        if "win_condition" in current_room:
            if all(item in self.player_inventory for item in current_room["win_condition"]):
                print("Congratulations! You have won the game!")
                self.reset_game()
            else:
                print("You have been defeated! Game over.")
                self.reset_game()

    def move(self, direction):
        # Move the player in the specified direction if possible.
        current_room = self.map[self.player_location]
        if direction in current_room["exits"]:
            self.player_location = current_room["exits"][direction]
            print(f"You go {direction}.")
            self.show_current_room()
            self.check_win_lose_conditions()
        else:
            print(f"There is no way to go {direction}.")
            

    def get_item(self, item):
        # Add an item to the player's inventory if it's in the room.
        room = self.map[self.player_location]
        if "items" in room and item in room["items"]:
            self.player_inventory.append(item)
            room["items"].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} here.")
    
    def drop_item(self, item):
        # Check if the item is in the player's inventory
        if item in self.player_inventory:
            self.player_inventory.remove(item)
            # Add the item to the current room
            current_room = self.map[self.player_location]
            if "items" not in current_room:
                current_room["items"] = []
            current_room["items"].append(item)
            print(f"You drop the {item}.")
        else:
            print(f"You don't have a {item} to drop.")


    def show_inventory(self):
        # Show the items in the player's inventory.
        if self.player_inventory:
            print("Inventory:")
            for item in self.player_inventory:
                print(f"  {item}")
        else:
            print("You are not carrying anything.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py <map_file>")
        sys.exit(1)

    map_file = sys.argv[1]
    # This is a basic structure. To run the game, create an instance of AdventureGame with a map file and call start_game.
    # For example:
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()