class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def active_players(self):
        return [p for p in self.players if not p.down]