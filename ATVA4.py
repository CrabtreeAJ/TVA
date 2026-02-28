from itertools import permutations
import numpy as np
from voting import VotingSystem
from happiness import BasicHappiness

def strat_voting_all(voting_system: VotingSystem, hap, happiness):

    voter_strats=[]

    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        best_strategy = None
        best_hap = happiness[x]

        for j in permutations(column):
            strat_vote_sit = np.insert(np.delete(true_preferences, x, axis=0), x, j, axis=0)
            strat_win = voting_system.vote(strat_vote_sit)[0][0]
            strat_hap = hap.get_happiness_single(column, strat_win)

            if strat_hap > best_hap:
                best_hap = strat_hap
                best_strategy = j
    
        voter_strats.append((x,j))

        if best_strategy is not None:
            # print(
            #     f"({j}, {strat_win}, {strat_hap}, {happiness[x]}, |"f"{sum(happiness) - happiness[x] + strat_hap}, {sum(happiness)})")
            print(f"Best strategy: {best_strategy} for voter {x}\n"
                  f"Results with new strategy applied alone: {best_strategy}\n"
                  f"Individual happiness improvement: {best_hap - happiness[x]}\n")
            
    strat_vote_sit = true_preferences
    for x,j in enumerate(voter_strats):
        strat_vote_sit = np.insert(np.delete(strat_vote_sit, x, axis=0), x, j, axis=0)
    
    combined_strat_win = voting_system.vote(strat_vote_sit)[0][0]
    combined_strat_hap = hap.get_happiness_total(combined_strat_win)

    print(f"Total happiness of voters with all strats in mind: {sum(combined_strat_hap)}\n")

    return 0