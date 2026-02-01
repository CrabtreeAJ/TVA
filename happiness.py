from abc import ABC, abstractmethod

class happiness(ABC):
    @abstractmethod
    def get_happiness(self, winner, situation):
        pass


class basic_happiness(happiness):

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