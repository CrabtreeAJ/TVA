from happiness import BasicHappiness
from voting import VotingSystem
import numpy as np

def main():
    schema = [3, 2, 1, 0]
    true_preferences = [["A", "C", "B", "D"], ["B", "D", "A", "C"], ["B", "A", "D", "C"], ["C", "A", "D", "B"],
                        ["D", "C", "B", "A"]]

    VS = VotingSystem(np.array(true_preferences), schema)

    winner = VS.true_vote()[0][0]
    print(winner)

    hap = BasicHappiness(winner, true_preferences)

    hap_metric = hap.get_happiness()

    print(hap_metric)

    print("-----strategic voting testing-----")

    # strat_voting_all(schema, true_preferences, hap, hap_metric)


if __name__ == "__main__":
    main()