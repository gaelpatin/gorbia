import random
from colorama import init, Fore, Style
init(autoreset=True)

from core.board import Board

BLOCK_DICE = ['POW', 'PUSH', 'PUSH', 'BOTH_DOWN', 'DODGE', 'DODGE']

class Game:
    def __init__(self, team1, team2):
        self.board = Board()
        self.teams = [team1, team2]
        self.current_team_idx = 0
        self.turn = 1
        self.ais = []
        self.last_action_log = ""
        self.coach_turns = [0, 0]  # un compteur de tour par équipe
        self.max_turns = 8

    def next_turn(self):
        self.current_team_idx = 1 - self.current_team_idx
        self.turn += 1
        for player in self.current_team().players:
            player.has_moved = False

    def current_team(self):
        return self.teams[self.current_team_idx]

    def opponent_team(self):
        return self.teams[1 - self.current_team_idx]

    def set_ais(self, ai1, ai2):
        self.ais = [ai1, ai2]

    def play_turn(self):
        team = self.current_team()
        ai = self.ais[self.current_team_idx]

        print(f"\n=== Tour {self.coach_turns[self.current_team_idx] + 1} - Équipe {team.name} ===")
        self.board.display()

        # Réinitialise les déplacements
        for player in team.players:
            player.has_moved = False

        # Tant qu’il reste des joueurs qui n’ont pas joué
        for player in team.active_players():
            action = ai.choose_action_for_player(self, player)

            if action:
                if action["type"] == "block":
                    attacker = action["attacker"]
                    defender = action["defender"]
                    self.attempt_block(attacker, defender)
                    attacker.has_moved = True
                    attacker.turns_played += 1
                elif action["type"] == "move":
                    self.board.move_player(action["player"], *action["to"])
                    print(Fore.YELLOW + f"{action['player'].name} avance vers {action['to']}." + Style.RESET_ALL)
                    action["player"].has_moved = True
                    action["player"].turns_played += 1

        # Fin du tour du coach
        self.coach_turns[self.current_team_idx] += 1
        if self.coach_turns[self.current_team_idx] >= self.max_turns:
            print(Fore.MAGENTA + f"🏁 Fin des tours pour l'équipe {team.name} !" + Style.RESET_ALL)

        self.current_team_idx = 1 - self.current_team_idx  # Changement d’équipe
        self.turn += 1

    def adjacent_enemies(self, player):
        x, y = player.position
        enemies = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < Board.WIDTH and 0 <= ny < Board.HEIGHT:
                neighbor = self.board.grid[ny][nx]
                if neighbor and neighbor.team != player.team:
                    enemies.append(neighbor)
        return enemies

    def attempt_block(self, attacker, defender):
        print(f"{attacker.name} tente un blocage contre {defender.name} !")
        str_a = attacker.strength
        str_d = defender.strength

        # Choix du nombre de dés
        if str_a >= 2 * str_d:
            dice = [random.choice(BLOCK_DICE) for _ in range(3)]
            choice_team = attacker.team
        elif str_a > str_d:
            dice = [random.choice(BLOCK_DICE) for _ in range(2)]
            choice_team = attacker.team
        elif str_d >= 2 * str_a:
            dice = [random.choice(BLOCK_DICE) for _ in range(3)]
            choice_team = defender.team
        elif str_d > str_a:
            dice = [random.choice(BLOCK_DICE) for _ in range(2)]
            choice_team = defender.team
        else:
            dice = [random.choice(BLOCK_DICE)]
            choice_team = attacker.team

        result = dice[0]

        # Résolution simple
        if result == 'POW' or result == 'BOTH_DOWN':
            defender.down = True
            self.last_action_log = f"{attacker.name} met {defender.name} au sol ! ({result})"
        elif result == 'PUSH':
            self.last_action_log = f"{attacker.name} repousse {defender.name}. (non implémenté)"
        elif result == 'DODGE':
            attacker.down = True
            self.last_action_log = f"{attacker.name} rate et tombe ! ({result})"
