import random
import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness
from strategic_voting import StrategicVote


"""
TVA3 doe not include rule 3: "Perfect knowledge". It does not know the true preference of all voters.
For TVA3 a voter only knows a percentage of other voter's true preferences.
E.g. Each voter knows 50% of the other voter's rankings.
"""
# WHat is the expected happiness of a voter given a certain ballot and a certain percentage of knowledge about other voters preferences.
def expected_happiness(voting_system, voter_id, ballot, known_voters, samples):
    true_preferences = voting_system.true_preferences #real preferences
    n = len(true_preferences) #number of voters
    total = 0 

    #Monte Carlo Simulation
    #Combine known preferences and random preferences for unknown voters.
    #Simulate the happiness.
    for _ in range(samples):
        simulated_situation = []
        for j in range(n):
            if j == voter_id: #Voter that is being evaluated
                simulated_situation.append(ballot)
            elif j in known_voters: #Voters of which tva3 has true knowledge
                simulated_situation.append(true_preferences[j])
            else:  #for the unknown voters simulate a random preference
                perm = list(true_preferences[j])
                random.shuffle(perm)
                simulated_situation.append(perm)
        simulated_situation = np.array(simulated_situation)

        winner = voting_system.vote(simulated_situation)[0][0] #COmpute Winner.

        hap = BasicHappiness(winner, true_preferences)  #Compute Happiness
        total += hap.get_happiness_single(true_preferences[voter_id], winner)                               
        
    return total / samples #Average over all simulations

#TVA3 knows 50% of the other pvoters preferences and runs 50 simulations.
def ATVA3_imperfect_knowledge(voting_system, strategy: StrategicVote, voter_id, samples=50, knowledge_percentage=0.5):
    true_preferences = voting_system.true_preferences
    n = len(true_preferences)

    other_voters = [i for i in range(n) if i != voter_id]
    k = int(len(other_voters) * knowledge_percentage)
    known_voters = set(random.sample(other_voters, k))

    column = true_preferences[voter_id]
    expected_honest_happiness = expected_happiness(voting_system, voter_id, column, known_voters, samples)

    best_ballot = column
    best_expected = expected_honest_happiness

    strategy_ballot, _, _ = strategy.find_strategy(voting_system, voter_id)
    if not np.array_equal(strategy_ballot, column):
        exp_hap = expected_happiness(voting_system, voter_id, strategy_ballot, known_voters, samples)
        if exp_hap > best_expected:
            best_ballot = strategy_ballot

    new_situation = list(true_preferences.copy())
    new_situation[voter_id] = best_ballot
    return np.array(new_situation)