import random
from typing import override
import numpy as np
from collections import Counter
from typing import TYPE_CHECKING

# !!! THIS IS ONLY FOR IDE TYPE CHECKING, IF IT CAUSES ANY ERRORS YOU CAN COMMENT IT OUT !!!
# Directly importing from strategic_voting causes circular import issue, so have to apply this workaround
if TYPE_CHECKING:
    from strategic_voting import StrategicVote


class VotingSystem:
    """
    System that simulates votings and stores results.

    IMPORTANT: Run .true_vote() before any simulations, as .simulate() needs self.true_result_list to be filled
    """
    def __init__(self, true_preferences: np.ndarray, candidates: list, scheme: list):
        self._true_preferences = true_preferences
        self._scheme_vector = scheme
        self._scheme_name = self.determine_scheme(scheme)
        self._true_result_list = []
        self._last_result_list = []
        self._candidates = candidates

    @property
    def true_preferences(self):
        """Returns the true preferences."""
        return self._true_preferences.copy()

    @property
    def scheme_vector(self):
        """Returns the scheme vector."""
        return self._scheme_vector

    @property
    def scheme_name(self):
        """Returns the name of the scheme."""
        return self._scheme_name

    @property
    def true_result_list(self):
        """Returns the initial result list."""
        return self._true_result_list.copy()

    @property
    def last_result_list(self):
        """Returns the most recent result list."""
        return self._last_result_list.copy()

    @property
    def candidates(self):
        """Returns the list of candidates."""
        return self._candidates.copy()

    def true_vote(self):
        """Initiates voting with only true preferences. Additionally, updates true_result_list with vote results"""
        self._true_result_list = self.vote(self.true_preferences).copy()
        return self.true_result_list

    def vote(self, situation):
        """Calculates winners for the given situation according to the defined scheme"""

        winner = []
        self._last_result_list.clear()

        match self.scheme_name:
            case "plurality":
                unique, count = np.unique(situation[:, 0], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], ord('A') - ord(x[0])), reverse=True)
            case "voting_for_two":
                unique, count = np.unique(situation[:, [0, 1]], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], ord('A') - ord(x[0])), reverse=True)
            case "anti_plurality":
                unique, count = np.unique(situation[:, :-1], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], ord('A') - ord(x[0])), reverse=True)
            case "borda":
                dictionary = {}
                for x in self.scheme_vector:
                    unique, count = np.unique(situation[:, [self.scheme_vector.index(x)]], return_counts=True)
                    temp_dict = dict(zip(unique, count * x))
                    dictionary = Counter(dictionary) + Counter(temp_dict)
                winner = sorted(dictionary.items(), key=lambda x: (x[1], ord('A') - ord(x[0])), reverse=True)

        # if there are any candidates that were not declared for this voting system - they should be ignored
        for candidate in winner:
            if candidate[0] in self.candidates:
                self._last_result_list.append(candidate)

        return self._last_result_list

    def simulate(self, strategy_type: "StrategicVote", cheating_probs: None|list[float] = None, to_print: bool = True):
        """Simulates strategic voting. Apart from cheater's vote,
         other votes are true preferences

        Args:
            strategy_type (StrategicVote): The specific strategy a cheating
                voter will attempt to apply.

            cheating_probs (list[float], optional): List of probabilities of cheating for every voter,
             where cheater[voter_id] = prob. If None, a voter who attempts to cheat
             will be selected uniformly at random.

            to_print (bool, optional): Flag to define whether runtime prints are allowed or not
        """

        cheater_id = random.choices([i for i in range(len(self.true_preferences))], cheating_probs)

        # situation where voter with `cheater_id` applied strategy of `strategy_type`
        cheater_strategy, cheater_happiness, situation = strategy_type.find_strategy(self, cheater_id)

        if self.true_preferences[cheater_id] != cheater_strategy:
            print(f"Voter with {cheater_id} cheated! Theirs new strategy is {cheater_strategy}"
                  f" and new individual happiness is {cheater_happiness}.")


        return self.vote(situation)


    def determine_scheme(self, scheme_vector: list):
        if scheme_vector.count(1) == 1 and scheme_vector.count(2) == 0:  # Plurality voting
            return "plurality"
        elif scheme_vector.count(1) == 2:  # Voting for two
            return "voting_for_two"
        elif scheme_vector.count(1) > 1 and scheme_vector.count(0) == 1:  # Anti-plurality voting
            return "anti_plurality"
        elif scheme_vector.count(2) > 0:  # Borda voting
            return "borda"

        return ""


class VotingSystemATVA4(VotingSystem):
    @override
    def simulate(self, strategy_type: "StrategicVote", cheating_probs: None|list[float] = None, to_print: bool = True):
        situation = self.true_preferences

        # Let every voter try to cheat
        for cheater_id in range(len(self.true_preferences)):
            # situation where voter with `cheater_id` applied strategy of `strategy_type`
            cheater_strategy, cheater_happiness, _ = strategy_type.find_strategy(self, cheater_id)

            # update situation with strategies that include cheating for every voter
            situation = np.insert(np.delete(situation, cheater_id, axis=0), cheater_id, cheater_strategy, axis=0)

            if self.true_preferences[cheater_id] != cheater_strategy:
                print(f"Voter with {cheater_id} cheated! Theirs new strategy is {cheater_strategy}"
                      f" and new individual happiness is {cheater_happiness}.")

        return self.vote(situation)




