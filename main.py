# by Benjamin Alias Kratos 
from utils import *
from game import Game
from caracter import Player


MENU_CHOICE = [
    lambda : play(),
    lambda : show_leaderboard(),
    lambda : exit()
]

def menu():
    print("=========== Welcome to God of War  ===========\n\n")

    print("1. Start a new game\n2. Show leaderboard\n3. Exit (already giving up ?)\n")

    choice = verify_player_input("> ", 1, 3)

    MENU_CHOICE[choice - 1]()

    print("========== Goodbye ==========")


def play():
    player_name = verify_player_name()
    player = Player(player_name)

    game = Game(player)
    game.init_deck()
    game.clash()
    update_leaderboard(player)
    

def show_leaderboard():
    print("\n\n====== Leaderboard ======\n")
    for player in db.players.find().sort("score", -1).limit(3):
        print(f"{player['name']} : {player['score']} points")

if __name__ == "__main__":
    menu()