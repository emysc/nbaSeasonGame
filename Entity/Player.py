from Entity.Person import Person 
import random

class Player(Person):
    def __init__ (self, 
                  name,
                  height,
                  salary,
                  shirtNumber,
                  position,
                  points
                  ):
        super().__init__(name, height, salary)
        self.position = position
        self.shirtNumber = shirtNumber
        self.points = int(float(points))
    
    def to_string(self):
        return (f"({self.position}) #{self.shirtNumber} {self.name} : {self.get_points()} pts \n")
    
    def to_dict(self):
        return {
            "shirtNumber": self.shirtNumber,
            "name": self.name,
            "position": self.position,
            "height": self.height,
            "points": self.points,
        }
        
    # questão 1 c, polimorfismo
    def get_random_salary(self):
        return random.randint(50000, 500000)  # Jogadores ganham mais