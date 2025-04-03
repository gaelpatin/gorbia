from core.board import Board
from core.player import Player
from core.team import Team
from core.game import Game
from ai.base_ai import BaseAI

def create_teams():
    humains = [Player(f"Humain{i+1}", "Humains", 3, 6) for i in range(3)]
    orcs = [Player(f"Orc{i+1}", "Orcs", 4, 5) for i in range(3)]
    return Team("Humains", humains), Team("Orcs", orcs)

def place_players(board, team, start_x, start_y):
    for i, player in enumerate(team.players):
        x = start_x + i
        y = start_y
        board.place_player(player, x, y)

def setup_game():
    team1, team2 = create_teams()
    board = Board()
    place_players(board, team1, 2, 3)  # humains à gauche
    place_players(board, team2, 21, 11)  # orcs à droite

    game = Game(team1, team2)
    game.board = board
    game.set_ais(BaseAI(team1), BaseAI(team2))
    game.board.ball_position = (13, 7)

    return game

def main():
    game = setup_game()
    max_turns = 16

    for _ in range(max_turns):
        game.play_turn()

if __name__ == "__main__":
    main()