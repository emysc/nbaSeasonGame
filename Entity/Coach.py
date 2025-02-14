from Person import Person 
import random

class Coach(Person):
    def __init__(self, name, height, salary):
        super().__init__(name, height, salary)
        self.salary = salary

    def to_string(self):
        return f"{self.name}\n"

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "name": self.name,
        }
    
    # questão 1 c, polimorfismo
    def get_random_salary(self):
        return random.randint(70000, 300000)  # Técnicos têm uma faixa diferente 

    
