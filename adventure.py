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
    }

    def __init__(self, map_file):
        self.map_file = map_file
        self.map = self.load_map(map_file)
        self.player_location = 0
        self.player_inventory = []

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: File '{filename}' is not a valid JSON file.")
            sys.exit(1)
        return None

    def start_game(self):
        self.show_current_room()
        while True:
            try:
                command = input("What would you like to do? ").strip().lower()
                if command:
                    self.process_command(command)
                if command == "quit":
                    break
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted. Goodbye!")
                break

    def process_command(self, command):
        parts = command.split(maxsplit=1)
        verb = parts[0]
        argument = parts[1] if len(parts) > 1 else None

        if verb in self.commands:
            if self.commands[verb].target and argument:
                getattr(self, verb)(argument)
            elif not self.commands[verb].target:
                getattr(self, verb)()
            else:
                print(f"Sorry, you need to provide an argument for '{verb}'.")
        else:
            print("I don't understand that command.")

    def show_current_room(self):
        room = self.map[self.player_location]
        print(f"\n> {room['name']}\n\n{room['desc']}\n")
        if "items" in room and room["items"]:
            print(f"Items: {', '.join(room['items'])}\n")
        print(f"Exits: {', '.join(room['exits'].keys())}\n")

    def go(self, direction):
        current_room = self.map[self.player_location]
        if direction in current_room["exits"]:
            self.player_location = current_room["exits"][direction]
            print(f"You go {direction}.")
            self.show_current_room()
            self.check_win_lose_conditions()

        else:
            print(f"There is no way to go {direction}.")


    def get(self, item):
        room = self.map[self.player_location]
        if "items" in room and item in room["items"]:
            self.player_inventory.append(item)
            room["items"].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} here.")

    def look(self):
        self.show_current_room()

    def inventory(self):
        if self.player_inventory:
            print("Inventory:")
            for item in self.player_inventory:
                print(f"  {item}")
        else:
            print("You are not carrying anything.")

    def quit(self):
        print("Goodbye!")

    def help(self):
        self.show_help()

    def drop(self, item):
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

    def show_help(self):
        print("You can run the following commands:")
        for command, info in self.commands.items():
            print(f"  {command} - {info.description}")

    def check_win_lose_conditions(self):
        current_room = self.map[self.player_location]

        # win condition
        if "win_condition" in current_room:
            if all(item in self.player_inventory for item in current_room["win_condition"]["items"]):
                print("Congratulations! You have won the game!")
                sys.exit(0)

        # lose condition
        if "lose_condition" in current_room:
            if not all(item in self.player_inventory for item in current_room["lose_condition"]["items"]):
                print("You have been defeated! Game over.")
                sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py <map_file>")
        sys.exit(1)

    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()
