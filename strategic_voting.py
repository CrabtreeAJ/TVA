import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness


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

    # NOTE: There seems to be no reason to put compromised candidate NOT in the first place, so we only consider that
    break_flag = False
    for index, candidate in enumerate(result_list):
        if voting_system.scheme_name == "anti_plurality":
            # For anti-plurality voting we can only 'move up' the last candidate, it doesn't matter to which position we move it,
            # as the second-to-last candidate becomes the last one in any case, so we only run the loop once.
            new_vote = voter_preference[:len(voter_preference)-1]
            new_vote = np.insert(new_vote, -1, voter_preference[-1], axis=0)

            break_flag = True # set the flag to break the loop
        else:
            # Voter tries to put every candidate in the first place of it's voting list
            new_vote = [x for x in voter_preference if x != candidate[0]]
            new_vote.insert(0, candidate[0])
            new_vote = np.array(new_vote)

        # Run test vote and evaluate how happy voter will be with this change
        new_situation = np.insert(np.delete(voting_system.true_preferences, voter_id, axis=0), voter_id, new_vote, axis=0)
        vote_result = voting_system.vote(new_situation)[0][0]
        happiness = happiness_engine.get_happiness_single(voter_preference, vote_result)

        # If happiness improved - save as the current best one
        if happiness > max_happiness:
            max_happiness = happiness
            best_strategy = new_vote
            best_situation = new_situation

        if break_flag:
            break

    return best_strategy, max_happiness, best_situation


def strat_voting_all(voting_system: VotingSystem, hap, happiness):
    true_preferences = voting_system.true_preferences

    for x, column in enumerate(true_preferences):
        for j in permutations(column):
            strat_vote_sit = np.insert(np.delete(true_preferences, x, axis=0), x, j, axis=0)
            strat_win = voting_system.vote(strat_vote_sit)[0][0]
            strat_hap = hap.get_happiness_single(column, strat_win)
            if (happiness[x] < strat_hap):
                print(
                    f"({j}, {strat_win}, {strat_hap}, {happiness[x]}, "f"{sum(happiness) - happiness[x] + strat_hap}, {sum(happiness)})")
    return 0