import numpy as np
from collections import Counter

Alphabet = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z")

class VotingSystem:
    def __init__(self, true_preferences: np.ndarray, candidates: list, scheme: list):
        self.true_preferences = true_preferences
        self.scheme_vector = scheme
        self.scheme_name = self.determine_scheme(scheme)
        self.true_result_list = []
        self.last_result_list = []
        self.candidates = candidates


    def true_vote(self):
        self.true_result_list = self.vote(self.true_preferences)

        return self.true_result_list


    def vote(self, situation):
        winner = []
        self.last_result_list.clear()

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
                self.last_result_list.append(candidate)

        return self.last_result_list


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







