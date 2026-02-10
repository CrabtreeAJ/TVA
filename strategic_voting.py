import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness


""" NOTE: For both compromise and burying we only consider moving ONE candidate at a time according to rules, 
 all the other candidates are shifted due to the move of the considered candidate. So, during compromise we move UP only
 ONE candidate, all the other candidates are shifted DOWN accordingly. The similar logic is applied to burying."""

def compromise(voting_system: VotingSystem, voter_id: int):
    voter_preference = voting_system.true_preferences[voter_id]
    best_strategy = voter_preference # initial best strategy is the true one
    best_situation = voting_system.true_preferences # initial best situation is true voting
    result_list = voting_system.true_result_list

    happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
    max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], result_list[0][0])

    # If the most preferred candidate is already winning - no need to strategy vote
    if result_list[0][0] == voter_preference[0]:
        return best_strategy, max_happiness, best_situation

    if voting_system.scheme_name == "burda":
        # Voter tries to put every candidate above its current position
        for old_index, candidate in enumerate(voter_preference):
            for new_index in range(old_index):
                new_vote = np.insert(np.delete(voter_preference, old_index), new_index, candidate)

                happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

                # If happiness improved - save as the current best one
                if happiness > max_happiness:
                    max_happiness = happiness
                    best_strategy = new_vote
                    best_situation = new_situation

    else:
        # For plurality, voting for two and anti-plurality voting schemes we only consider compromising those candidates that were not given points before
        # (so those who were not included in the mask before). E.g. given scheme vector [1, 1, 0, 0] only the last two would be considered for compromise.
        for i, candidate in enumerate(voter_preference):
            if voting_system.scheme_vector[i] == 1:
                continue
            # Voter tries to put every candidate in the first place of it's voting list
            new_vote = np.insert(np.delete(voter_preference, i), 0, candidate)

            happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

            # If happiness improved - save as the current best one
            if happiness > max_happiness:
                max_happiness = happiness
                best_strategy = new_vote
                best_situation = new_situation

    return best_strategy, max_happiness, best_situation


def burying(voting_system: VotingSystem, voter_id: int):
    voter_preference = voting_system.true_preferences[voter_id]
    best_strategy = voter_preference # initial best strategy is the true one
    best_situation = voting_system.true_preferences # initial best situation is true voting
    result_list = voting_system.true_result_list

    happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
    max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], result_list[0][0])

    # If the most preferred candidate is already winning - no need to strategy vote
    if result_list[0][0] == voter_preference[0]:
        return best_strategy, max_happiness, best_situation


    if voting_system.scheme_name == "burda":
        # Voter tries to put every candidate above its current position
        for old_index, candidate in enumerate(voter_preference):
            for new_index in range(old_index, voter_preference.size):
                new_vote = np.insert(np.delete(voter_preference, old_index), new_index, candidate)

                happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

                # If happiness improved - save as the current best one
                if happiness > max_happiness:
                    max_happiness = happiness
                    best_strategy = new_vote
                    best_situation = new_situation
    else:
        # For plurality, voting for two and anti-plurality voting schemes we only consider burying those candidates that were given points before
        # (so those who are under masked by voting scheme). E.g. given scheme vector [1, 1, 0, 0] only the first two would be considered for burying.
        for i, candidate in enumerate(voter_preference):
            if voting_system.scheme_vector[i] == 0:
                break
            # Voter tries to put every candidate in the first place of it's voting list
            new_vote = np.insert(np.delete(voter_preference, i), 0, candidate)

            happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

            # If happiness improved - save as the current best one
            if happiness > max_happiness:
                max_happiness = happiness
                best_strategy = new_vote
                best_situation = new_situation



    return best_strategy, max_happiness, best_situation


def strat_voting_all(voting_system: VotingSystem, hap, happiness):
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

        if best_strategy is not None:
            # print(
            #     f"({j}, {strat_win}, {strat_hap}, {happiness[x]}, |"f"{sum(happiness) - happiness[x] + strat_hap}, {sum(happiness)})")
            print(f"Best strategy: {best_strategy} for voter {x}\n"
                  f"Results with new strategy applied: {best_strategy}\n"
                  f"Individual happiness improvement: {best_hap - happiness[x]}\n")
    return 0


def test_new_vote(voting_system, happiness_engine, new_vote, voter_id):
    # Run test vote and evaluate how happy voter will be with this change
    new_situation = np.insert(np.delete(voting_system.true_preferences, voter_id, axis=0), voter_id, new_vote,
                              axis=0)
    vote_result = voting_system.vote(new_situation)[0][0]
    happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], vote_result)

    return happiness, new_situation