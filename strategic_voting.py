from abc import abstractmethod, ABC
from typing import Tuple

import numpy as np
from itertools import permutations
from voting import VotingSystem
from happiness import BasicHappiness


class StrategicVote(ABC):
    @abstractmethod
    def find_strategy(self, voting_system: VotingSystem, voter_id: int) -> Tuple[np.ndarray, int, np.ndarray]:
        pass



""" NOTE: For both compromise and burying we only consider moving ONE candidate at a time according to rules, 
 all the other candidates are shifted due to the move of the considered candidate. So, during compromise we move UP only
 ONE candidate, all the other candidates are shifted DOWN accordingly. The similar logic is applied to burying."""

class CompromiseStrategy(StrategicVote):
    """Finds the best possible strategy by applying compromise"""
    def find_strategy(self, voting_system: VotingSystem, voter_id: int):
        try:
            voter_preference = voting_system.true_preferences[voter_id]
            best_strategy = voter_preference # initial best strategy is the true one
            best_situation = voting_system.true_preferences # initial best situation is true voting
            result_list = voting_system.true_result_list

            happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
            max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], result_list[0][0])
        except IndexError:
            raise IndexError(
                f"voting_system.true_results_list field seems to be empty, run voting_system.true_vote() first."
            )

        # If the most preferred candidate is already winning - no need to strategy vote
        if result_list[0][0] == voter_preference[0]:
            return best_strategy, max_happiness, best_situation

        if voting_system.scheme_name == "borda":
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
            # For plurality, voting for two and anti-plurality voting schemes we only consider compromising those candidates
            # that were not given points before(so those who were not included in the mask before).
            # E.g. given scheme vector [1, 1, 0, 0] only the last two would be considered for compromise.
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


class BuryingStrategy(StrategicVote):
    """Finds the best possible strategy by applying compromise"""
    def find_strategy(self, voting_system: VotingSystem, voter_id: int):
        try:
            voter_preference = voting_system.true_preferences[voter_id]
            best_strategy = voter_preference # initial best strategy is the true one
            best_situation = voting_system.true_preferences # initial best situation is true voting
            result_list = voting_system.true_result_list

            happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
            print("BBBB", voting_system.true_preferences)
            max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], result_list[0][0])
        except IndexError:
            raise IndexError(
            f"voting_system.true_results_list field seems to be empty, run voting_system.true_vote() first."
            )

        print(result_list, max_happiness, "ABABAB")

        # If the most preferred candidate is already winning - no need to strategy vote
        if result_list[0][0] == voter_preference[0]:
            return best_strategy, max_happiness, best_situation


        if voting_system.scheme_name == "borda":
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
            # For plurality, voting for two and anti-plurality voting schemes we only consider burying those candidates that
            # were given points before(so those who are under masked by voting scheme).
            # E.g. given scheme vector [1, 1, 0, 0] only the first two would be considered for burying.
            for i, candidate in enumerate(voter_preference):
                if voting_system.scheme_vector[i] == 0:
                    break
                # Voter tries to put every candidate in the first place of it's voting list
                new_vote = np.insert(np.delete(voter_preference, i), 0, candidate)

                happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)
                print(happiness, new_situation, "AAAAAA")

                # If happiness improved - save as the current best one
                if happiness > max_happiness:
                    max_happiness = happiness
                    best_strategy = new_vote
                    best_situation = new_situation


        return best_strategy, max_happiness, best_situation

class BulletStrategy(StrategicVote):
    """
    The way how bullet voting works is that a voter 'corrupts' every candidate except one by replacing it with a symbol
     unknown to the system. Voting system than ignores all 'corrupted' candidates and only considers one selected
    """
    def find_strategy(self, voting_system: VotingSystem, voter_id: int):
        try:
            voter_preference = voting_system.true_preferences[voter_id]
            best_strategy = voter_preference  # initial best strategy is the true one
            best_situation = voting_system.true_preferences  # initial best situation is true voting
            result_list = voting_system.true_result_list

            happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
            max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id],
                                                                  result_list[0][0])
        except IndexError:
            raise IndexError(
                f"voting_system.true_results_list field seems to be empty, run voting_system.true_vote() first."
            )

        # plurality voting considers at most one candidate, so there is no way to properly apply bullet voting
        if voting_system.scheme_name == "plurality":
            return best_strategy, max_happiness, best_situation

        # If the most preferred candidate is already winning - no need to strategy vote
        if result_list[0][0] == voter_preference[0]:
            return best_strategy, max_happiness, best_situation


        for i in range(len(voter_preference)):
            # for borda there is no point in 'corrupting' your top candidate,
            # so we only consider situation where voters corrupts every candidate except the top
            if voting_system.scheme_name == "borda" and  i > 0:
                return best_strategy, max_happiness, best_situation

            if voting_system.scheme_vector[i] == 0:
                break

            new_vote = np.array(voter_preference, dtype=np.str_)
            # Replace the unwanted candidates with invalid symbol, that would be ignored by the system
            for j in range(len(voter_preference)):
                if i == j: continue
                new_vote[j] = "-"

            happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

            # If happiness improved - save as the current best one
            if happiness > max_happiness:
                max_happiness = happiness
                best_strategy = new_vote
                best_situation = new_situation

        return best_strategy, max_happiness, best_situation


class BestStrategy(StrategicVote):
    """
    BestStrategy finds the most optimal preference list for the given voter, considering that it includes all candidates
    in the bulletin. This class doesn't consider situation where candidates can be corrupted in the submission
    """
    def find_strategy(self, voting_system: VotingSystem, voter_id: int):
        try:
            voter_preference = voting_system.true_preferences[voter_id]
            best_strategy = voter_preference  # initial best strategy is the true one
            best_situation = voting_system.true_preferences  # initial best situation is true voting
            result_list = voting_system.true_result_list

            happiness_engine = BasicHappiness(result_list[0][0], voting_system.true_preferences)
            max_happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id],
                                                                  result_list[0][0])
        except IndexError:
            raise IndexError(
                f"voting_system.true_results_list field seems to be empty, run voting_system.true_vote() first."
            )

        for new_vote in permutations(voter_preference):
            new_vote = np.array(new_vote)
            happiness, new_situation = test_new_vote(voting_system, happiness_engine, new_vote, voter_id)

            # If happiness improved - save as the current best one
            if happiness > max_happiness:
                max_happiness = happiness
                best_strategy = new_vote
                best_situation = new_situation

        return best_strategy, max_happiness, best_situation


def test_new_vote(voting_system, happiness_engine, new_vote, voter_id):
    # Run test vote and evaluate how happy voter will be with this change
    new_situation = np.insert(np.delete(voting_system.true_preferences, voter_id, axis=0), voter_id, new_vote,
                              axis=0)
    vote_result = voting_system.vote(new_situation)[0][0]
    happiness = happiness_engine.get_happiness_single(voting_system.true_preferences[voter_id], vote_result)

    return happiness, new_situation