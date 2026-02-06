import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness


def compromise(voting_system: VotingSystem, voter_id: int):
    voter_preference = voting_system.true_preferences[voter_id]
    best_strategy = voter_preference # initial best strategy is the true one
    best_situation = voting_system.true_preferences # initial best situation is true voting
    result_list = voting_system.true_result_list
    candidates_len = voter_preference.size

    delta_vote_count = [candidate[1] - result_list[0][1] for candidate in result_list]
    happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
    max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], result_list[0][0])


    # if result_list[0][0] == voter_preference[0]:
    #     return voter_preference

    match voting_system.scheme_name:
        case "plurality":
            print("check")
            pass
        case "voting_for_two":
            pass
        case "anti_plurality":
            pass
        case "burda":
            # In burda voter can increase points of a candidate by |candidates| - 'candidate rank in true preference'
            for index, candidate in enumerate(result_list):
                max_improvement = candidates_len - np.where(voter_preference == candidate[0])[0]

                if 0 < abs(delta_vote_count[index]) <= max_improvement:
                    new_vote = [x for x in voter_preference if x != candidate[0]]
                    new_vote.insert(0, candidate[0])
                    new_vote = np.array(new_vote)

                    new_situation = np.insert(np.delete(voting_system.true_preferences, voter_id, axis=0), voter_id, new_vote, axis=0)
                    vote_result = voting_system.vote(new_situation)[0][0]
                    happiness = happiness_engine.get_happiness_single(new_vote, vote_result)

                    if happiness > max_happiness:
                        max_happiness = happiness
                        best_strategy = new_vote
                        best_situation = new_situation

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