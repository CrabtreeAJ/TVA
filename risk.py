import itertools
from abc import ABC, abstractmethod
from voting import Alphabet


#Risk: The number of voter who can benefit from voting strategically divided by total number of voters.

"""

#Outputs:
risk_value: A risk value between 0 and 1.
can_manipulate: A list of booleans showing which voters can manipulate the election by voting strategically.
can_benefit: A list of booleans showing which voters can benefit from voting strategically.

Example Input:
schema = [3, 2, 1, 0]
    true_preferences = [["A", "C", "B", "D"], ["B", "D", "A", "C"], ["B", "A", "D", "C"], ["C", "A", "D", "B"],
                        ["D", "C", "B", "A"]]

Example output:
{'risk_value': 0.6, 'can_manipulate': [True, True, True, True, True], 'can_benefit': [False, True, True, False, True]}

"""


class Risk(ABC):
    @abstractmethod
    def get_risk(self):
        pass

class BasicRisk(Risk):

    def __init__(self, winner, situation, schema):
        self.winner = winner
        self.situation = situation
        self.schema = schema

    def _total_score(self, situation):
        #dictionary with candidates as keys and total scores as values
        totals = {}
        for ballot in situation:
            for i, candidate in enumerate(ballot):
                totals[candidate] = totals.get(candidate, 0.0) + self.schema[i]
        return totals
    
    def _winner_from_totals(self, totals):
        max_score = max(totals.values())
        winners = [candidate for candidate, score in totals.items() if score == max_score]
        # Return the alphabetically first candidate in case of a tie (As in the document "Strategic_voting_description" -> "V. Additional remarks")
        winners.sort(key=lambda candidate: Alphabet.index(candidate))
        return winners[0] # Initially used: return sorted(winners)[0]
          
    def get_risk(self):
        
        n_voters = len(self.situation)
        if n_voters == 0:
            return {"risk_value": 0.0, "can_manipulate": [], "can_benefit": []}

        actual_winner = self._total_score(self.situation)
        actual_winner = self._winner_from_totals(actual_winner)

        can_manipulate = [False] * n_voters
        can_benefit = [False] * n_voters    

        candidates =list(self.situation[0])

        for i, ballot in enumerate(self.situation):
            ballot = list(ballot)

            # Generate all possible permutations of the ballot (not the original ballot)
            for perm in itertools.permutations(candidates):
                perm = list(perm)
                if perm == ballot:
                    continue
                
                new_situation = [list(b) for b in self.situation]
                new_situation[i] = perm
                
                new_totals = self._total_score(new_situation)
                new_winner = self._winner_from_totals(new_totals)
         
                if new_winner != actual_winner:
                    can_manipulate[i] = True
                    if ballot.index(new_winner) < ballot.index(actual_winner):
                        can_benefit[i] = True
                        break
        # Calculate the risk value
        # Only look at can benefit because we do not want to count voters who can manipulate but do not benefit from it.
        risk_value = sum(1 for x in can_benefit if x) / n_voters

        return{
            "risk_value": risk_value,
            "can_manipulate": can_manipulate,
            "can_benefit": can_benefit, 
        }
    
 