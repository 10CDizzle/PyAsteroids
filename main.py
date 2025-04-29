# main.py

from game import Game

def main():
    """
    The entry point of the game. Initializes the game, displays the title screen, and starts the main game loop.
    """
    game = Game()
    game.title_screen( )
    game.main_game()

if __name__ == "__main__":
    main()
