from abc import ABC, abstractmethod

"""
   Calculates happiness. Part of the output in testing.py (main). 
"""

class happiness(ABC):
    @abstractmethod
    def get_happiness(self):
        pass


class BasicHappiness(happiness):

    def __init__(self, winner, situation):
        self.winner = winner
        self.situation = situation

    def get_happiness(self):
        sit = self.situation
        win = self.winner

        hap=[]

        for column in sit:
            ind = column.index(win)
            hap.append(len(column) - len(column)/2 -ind)
        return hap
    
    def get_happiness_single(self, col, win):

        col = list(col)
        
        ind = col.index(win)
        hap = (len(col) - len(col)/2 -ind)
        return hap