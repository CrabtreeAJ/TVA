from itertools import permutations
import numpy as np
from voting import VotingSystem
from happiness import BasicHappiness
from strategic_voting import CompromiseStrategy, BuryingStrategy, BulletStrategy, BestStrategy

def ATVA4_strat_voting_all(voting_system: VotingSystem, basic_happiness, happiness):

    voter_strats=[]

    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        best_strategy = None
        best_hap = happiness[x]

        for j in permutations(column):
            strat_vote_sit = np.insert(np.delete(true_preferences, x, axis=0), x, j, axis=0)
            strat_win = voting_system.vote(strat_vote_sit)[0][0]
            strat_hap = basic_happiness.get_happiness_single(column, strat_win)

            if strat_hap > best_hap:
                best_hap = strat_hap
                best_strategy = j
    
        voter_strats.append((x,best_strategy))

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
    combined_strat_hap = basic_happiness.get_happiness_total(combined_strat_win)

    print(f"Total happiness of voters with all strats in mind: {sum(combined_strat_hap)}\n")

    return 0


def ATVA4_compromise(voting_system: VotingSystem, voter_id: int, happiness, basic_happiness):

    voter_strats=[]
    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        best_strategy = None

        best_strategy, max_happiness, _ = CompromiseStrategy().find_strategy(voting_system, x)
        

        voter_strats.append((x,best_strategy))

        if best_strategy is not None:

            print(f"Best strategy: {best_strategy} for voter {x}\n"
                  f"Results with new strategy applied alone: {best_strategy}\n"
                  f"Individual happiness improvement: {max_happiness - happiness[x]}\n")
            
    strat_vote_sit = true_preferences
    for x,j in enumerate(voter_strats):
        strat_vote_sit = np.insert(np.delete(strat_vote_sit, x, axis=0), x, j, axis=0)
    
    combined_strat_win = voting_system.vote(strat_vote_sit)[0][0]
    combined_strat_hap = basic_happiness.get_happiness_total(combined_strat_win)

    print(f"Total happiness of voters with all strats in mind: {sum(combined_strat_hap)}\n")

    return 0


def ATVA4_burying(voting_system: VotingSystem, voter_id: int, happiness, basic_happiness):
    
    voter_strats=[]
    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        best_strategy = None

        best_strategy, max_happiness, _ = BuryingStrategy().find_strategy(voting_system, x)
        

        voter_strats.append((x,best_strategy))

        if best_strategy is not None:

            print(f"Best strategy: {best_strategy} for voter {x}\n"
                  f"Results with new strategy applied alone: {best_strategy}\n"
                  f"Individual happiness improvement: {max_happiness - happiness[x]}\n")
            
    strat_vote_sit = true_preferences
    for x,j in enumerate(voter_strats):
        strat_vote_sit = np.insert(np.delete(strat_vote_sit, x, axis=0), x, j, axis=0)
    
    combined_strat_win = voting_system.vote(strat_vote_sit)[0][0]
    combined_strat_hap = basic_happiness.get_happiness_total(combined_strat_win)

    print(f"Total happiness of voters with all strats in mind: {sum(combined_strat_hap)}\n")

    return 0



def ATVA4_bullet_voting(voting_system: VotingSystem, voter_id: int, happiness, basic_happiness):
    
    voter_strats=[]
    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        best_strategy = None

        best_strategy, max_happiness, _ = BulletStrategy().find_strategy(voting_system, x)
        

        voter_strats.append((x,best_strategy))

        if best_strategy is not None:

            print(f"Best strategy: {best_strategy} for voter {x}\n"
                  f"Results with new strategy applied alone: {best_strategy}\n"
                  f"Individual happiness improvement: {max_happiness - happiness[x]}\n")
            
    strat_vote_sit = true_preferences
    for x,j in enumerate(voter_strats):
        strat_vote_sit = np.insert(np.delete(strat_vote_sit, x, axis=0), x, j, axis=0)
    
    combined_strat_win = voting_system.vote(strat_vote_sit)[0][0]
    combined_strat_hap = basic_happiness.get_happiness_total(combined_strat_win)

    print(f"Total happiness of voters with all strats in mind: {sum(combined_strat_hap)}\n")

    return 0