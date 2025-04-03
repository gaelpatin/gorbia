import random

DIRECTIONS = [
    (-1, -1), (0, -1), (1, -1),  # diagonales haut
    (-1,  0),          (1,  0),  # gauche / droite
    (-1,  1), (0,  1), (1,  1),  # diagonales bas
]

class BaseAI:
    def __init__(self, team):
        self.team = team

    def choose_action_for_player(self, game, player):
        if player.has_moved or player.down:
            return None

        enemies = game.adjacent_enemies(player)
        if enemies:
            return {
                "type": "block",
                "attacker": player,
                "defender": enemies[0]
            }

        board = game.board
        x, y = player.position

        # Parcours les 8 directions au hasard pour trouver une case libre
        random.shuffle(DIRECTIONS)  # Pour varier les choix
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.WIDTH and 0 <= ny < board.HEIGHT:
                if board.grid[ny][nx] is None:
                    return {
                        "type": "move",
                        "player": player,
                        "to": (nx, ny)
                    }

        return None  # Aucune case libre autour
