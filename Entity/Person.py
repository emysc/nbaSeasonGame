from abc import ABC, abstractmethod
import random

class Person(ABC):
    def __init__ (self, 
                  name,
                  height,
                  salary
                  ):
        self.name = name
        self.height = height
        self.salary = salary if salary is not None else self.get_random_salary()
        
    @abstractmethod
    def to_string(self):
        pass
    
    # questão 1 c, polimorfismo
    def get_random_salary(self):
        return random.randint(30000, 100000) 