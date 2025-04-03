class Player:
    def __init__(self, name, team, strength, movement):
        self.name = name
        self.team = team
        self.strength = strength
        self.movement = movement
        self.position = None
        self.has_moved = False
        self.down = False
        self.has_ball = False  # ← Nouveau
        self.turns_played = 0

    def __repr__(self):
        return f"{self.name[0]}({self.team[0]})"