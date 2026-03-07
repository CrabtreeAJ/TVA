import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness
from strategic_voting import StrategicVote

"""
TVA2 doe not include rule 2: "Counter-strategic voting". For ATVA-2, a voter assumes that if they vote tactically, other voters may react strategically as well.
E.g. If voter i changes their ballot to improve the outcome, the other voters may adjust their ballots in response to protect their own interests.
ATVA-2 therefore evaluates manipulation while taking into account possible best responses from the other voters.
"""

def apply_counter_responses(voting_system, profile, excluding_voter):
    """
    Apply one round of best responses
    for all voters except excluding_voter.
    """
    n = len(profile)

    for j in range(n):
        if j != excluding_voter:
            response = best_response(voting_system, profile, j)
            profile[j] = response

    return profile

def best_response(voting_system, profile, voter_id):
    """
    Compute best response ballot for a voter
    given current profile.
    """
    true_preferences = voting_system.true_preferences
    true_ballot = true_preferences[voter_id]

    current_winner = voting_system.vote(profile)[0][0]
    happiness_model = BasicHappiness(current_winner, true_preferences)
    current_happiness = happiness_model.get_happiness_single(
        true_ballot, current_winner
    )

    best_ballot = profile[voter_id]
    best_happiness = current_happiness

    for perm in permutations(true_ballot):
        temp_profile = profile.copy()
        temp_profile[voter_id] = perm

        winner = voting_system.vote(temp_profile)[0][0]
        hap_model = BasicHappiness(winner, true_preferences)
        new_happiness = hap_model.get_happiness_single(
            true_ballot, winner
        )

        if new_happiness > best_happiness:
            best_happiness = new_happiness
            best_ballot = perm

    return best_ballot


def atva2(voting_system):
    true_preferences = voting_system.true_preferences
    n = len(true_preferences)

    for voter_id, true_ballot in enumerate(true_preferences):

        #honest baseline WITH counter responses (I believe)
        honest_profile = np.array(true_preferences.copy())
        honest_profile = apply_counter_responses(
            voting_system, honest_profile, voter_id
        )

        honest_winner = voting_system.vote(honest_profile)[0][0]
        happiness_model = BasicHappiness(honest_winner, true_preferences)

        honest_happiness = happiness_model.get_happiness_single(
            true_ballot, honest_winner
        )

        best_strategy = None
        best_happiness = honest_happiness

        for perm in permutations(true_ballot):

            profile = np.array(true_preferences.copy())
            profile[voter_id] = perm

            #apply counter responses symmetrically
            profile = apply_counter_responses(
                voting_system, profile, voter_id
            )

            final_winner = voting_system.vote(profile)[0][0]
            hap_model = BasicHappiness(final_winner, true_preferences)

            final_happiness = hap_model.get_happiness_single(
                true_ballot, final_winner
            )

            if final_happiness > best_happiness:
                best_happiness = final_happiness
                best_strategy = perm

        #if best_strategy is not None and best_strategy != tuple(true_ballot):
            #print(f"Voter {voter_id} can increase happiness under ATVA-2.")
            #print(f"Best strategy: {best_strategy}")
            #print(f"Happiness improvement: {best_happiness - honest_happiness}\n")

    return 0


def atva2_sit(voting_system: VotingSystem, strategy: StrategicVote, voter_id: int):
    true_preferences = voting_system.true_preferences
    n = len(true_preferences)

    #for voter_id, true_ballot in enumerate(true_preferences):

        #honest baseline WITH counter responses (I believe)

    true_ballot = true_preferences[voter_id]
    honest_profile = np.array(true_preferences.copy())
    honest_profile = apply_counter_responses(
        voting_system, honest_profile, voter_id
    )

    honest_winner = voting_system.vote(honest_profile)[0][0]
    happiness_model = BasicHappiness(honest_winner, true_preferences)

    honest_happiness = happiness_model.get_happiness_single(
        true_ballot, honest_winner
    )

    best_strategy = true_ballot
    best_happiness = honest_happiness

    strategies = strategy.find_all_strategies(voting_system, voter_id)

    for strat in strategies:

        profile = np.array(true_preferences.copy())
        profile[voter_id] = strat

        #apply counter responses symmetrically
        profile = apply_counter_responses(
            voting_system, profile, voter_id
        )

        final_winner = voting_system.vote(profile)[0][0]
        hap_model = BasicHappiness(final_winner, true_preferences)

        final_happiness = hap_model.get_happiness_single(
            true_ballot, final_winner
        )

        if final_happiness > best_happiness:
            best_happiness = final_happiness
            best_strategy = strat

    #if best_strategy is not None and best_strategy != tuple(true_ballot):
        #print(f"Voter {voter_id} can increase happiness under ATVA-2.")
        #print(f"Best strategy: {best_strategy}")
        #print(f"Happiness improvement: {best_happiness - honest_happiness}\n")


    new_situation = list(true_preferences.copy())
    new_situation[voter_id] = best_strategy

    return np.array(new_situation)