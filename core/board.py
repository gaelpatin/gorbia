from colorama import Fore, Style

class Board:
    WIDTH = 26
    HEIGHT = 15

    def __init__(self):
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.ball_position = (13, 7)  # milieu du terrain par défaut

    def place_player(self, player, x, y):
        player.position = (x, y)
        self.grid[y][x] = player

    def move_player(self, player, new_x, new_y):
        old_x, old_y = player.position
        self.grid[old_y][old_x] = None
        self.grid[new_y][new_x] = player
        player.position = (new_x, new_y)
        player.has_moved = True

        # Ramassage automatique si balle
        if (new_x, new_y) == self.ball_position:
            player.has_ball = True
            self.ball_position = None
            print(Fore.YELLOW + f"{player.name} ramasse la balle !" + Style.RESET_ALL)

    def display(self):
        # Affichage de la ligne des numéros de colonne
        header = "    " + " ".join(f"{x:02}" for x in range(self.WIDTH))
        print(header)

        for y in range(self.HEIGHT):
            line = f"{y:02}  "  # Numéro de ligne
            for x in range(self.WIDTH):
                cell = self.grid[y][x]
                if cell:
                    symbol = self.get_symbol(cell)
                elif (x, y) == self.ball_position:
                    symbol = Fore.YELLOW + "●" + Style.RESET_ALL
                elif x == 0:
                    symbol = Fore.RED + "=" + Style.RESET_ALL
                elif x == self.WIDTH - 1:
                    symbol = Fore.CYAN + "=" + Style.RESET_ALL
                else:
                    symbol = "."
                line += f"{symbol}  "  # double espace fixe
            print(line)
        print()

    def get_symbol(self, player):
        if player.has_ball:
            return Fore.YELLOW + "●" + Style.RESET_ALL

        if player.team == "Humains":
            char = 'h' if not player.down else 'H'
            color = Fore.BLUE
        else:
            char = 'o' if not player.down else 'O'
            color = Fore.GREEN

        return color + char + Style.RESET_ALL