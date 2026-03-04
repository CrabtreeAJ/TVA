from abc import ABC, abstractmethod

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
            hap.append(round(1-ind/(len(column)-1),2))
            #hap.append(len(column) - len(column)/2 -ind)
        return hap
    
    def get_happines_total(self, win):
        sit = self.situation
        
        hap=[]

        for column in sit:
            ind = column.index(win)
            hap.append(round(1-ind/(len(column)-1),2))
            #hap.append(len(column) - len(column)/2 -ind)
        return hap
    
    def get_happiness_single(self, col, win):

        col = list(col)
        
        ind = col.index(win)
        hap = (round(1-ind/(len(col)-1),2))
        #hap = (len(col) - len(col)/2 -ind)
        return hap