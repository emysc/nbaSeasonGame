class Conference:
    def __init__(self, name, teams=None):
        self.name = name
        self.teams = teams if teams else []

    def addTeam(self, team):
        self.teams.append(team)
    def to_dict(self):
        return {
            "name": self.name,
            "teams": [team.to_dict() for team in self.teams],
        }