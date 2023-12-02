import json
import sys

class GameEngine:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.current_room = 0
        self.inventory = []

    def load_map(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def start_game(self):
        while True:
            self.display_current_room()
            command = input("What would you like to do? ").strip().lower()
            if command == 'quit':
                print("Goodbye!")
                break
            self.process_command(command)

    def display_current_room(self):
        room = self.map[self.current_room]
        print(f"\n> {room['name']}\n\n{room['desc']}\n")
        print("Exits:", ' '.join(room['exits'].keys()))

    def process_command(self, command):
        if command.startswith('go '):
            self.handle_go_command(command[3:])
        # Add more command processing here (e.g., 'get', 'look', etc.)

    def handle_go_command(self, direction):
        current_exits = self.map[self.current_room]['exits']
        if direction in current_exits:
            self.current_room = current_exits[direction]
        else:
            print("There's no way to go", direction)

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    map_file = sys.argv[1]
    game = GameEngine(map_file)
    game.start_game()