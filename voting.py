import numpy as np
from collections import Counter


Alphabet = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z")
Alphabet2 = ("Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F",
             "E", "D", "C", "B", "A")


class VotingSystem:
    def __init__(self, true_preferences: np.ndarray, scheme: list):
        self.true_preferences = true_preferences
        self.scheme_vector = scheme
        self.scheme_name = self.determine_scheme(scheme)
        self.true_result_list = []
        self.last_result_list = []

    def true_vote(self):
        self.true_result_list = self.vote(self.true_preferences)

        return self.true_result_list


    def vote(self, situation):
        winner = ""

        match self.scheme_name:
            case "plurality":
                unique, count = np.unique(situation[:, 0], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], 27 - Alphabet.index(x[0])), reverse=True)
            case "voting_for_two":
                unique, count = np.unique(situation[:, [0, 1]], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], 27 - Alphabet.index(x[0])), reverse=True)
            case "anti_plurality":
                unique, count = np.unique(situation[:, :-1], return_counts=True)
                winner = sorted(dict(zip(unique, count)).items(),
                                key=lambda x: (x[1], 27 - Alphabet.index(x[0])), reverse=True)
            case "burda":
                dictionary = {}
                for x in self.scheme_vector:
                    unique, count = np.unique(situation[:, [self.scheme_vector.index(x)]], return_counts=True)
                    temp_dict = dict(zip(unique, count * x))
                    dictionary = Counter(dictionary) + Counter(temp_dict)
                winner = sorted(dictionary.items(), key=lambda x: (x[1], 27 - Alphabet.index(x[0])), reverse=True)

        self.last_result_list = winner

        return winner


    def determine_scheme(self, scheme_vector: list):
        if scheme_vector.count(1) == 1 and scheme_vector.count(2) == 0:  # Plurality voting
            return "plurality"
        elif scheme_vector.count(1) == 2:  # Voting for two
            return "voting_for_two"
        elif scheme_vector.count(1) > 1 and scheme_vector.count(0) == 1:  # Anti-plurality voting
            return "anti_plurality"
        elif scheme_vector.count(2) > 0:  # Burda voting
            return "burda"

        return ""







