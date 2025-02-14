from Entity.Player import Player 
from Entity.Coach import Coach 
from functools import singledispatchmethod

class Team:
    def __init__ (self, name, conference, coach, isSelected = False):
        self.name = name
        self.conference = conference
        self.players = []
        self.isSelected = isSelected
        self.coach = coach
        
        
    @singledispatchmethod
    def addPerson(person):
        pass

    @addPerson.register   
    def _(self, player : Player):
        self.players.append(player)

    @addPerson.register
    def _(self, coach: Coach):
        self.coach = coach
    
    def to_dict(self):
        return {
            "name": self.name,
            "coach": self.coach.to_dict(),
            "players": [player.to_dict() for player in self.players],
        }    

