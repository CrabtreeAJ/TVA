from happiness import BasicHappiness
from strategic_voting import compromise, burying, strat_voting_all
from voting import VotingSystem
import numpy as np

def main():
    schema = [1, 1, 1, 0]
    true_preferences = [["A", "C", "B", "D"], ["B", "D", "A", "C"], ["B", "D", "A", "C"], ["C", "D", "B", "A"],
                        ["D", "C", "A", "B"]]

    VS = VotingSystem(np.array(true_preferences), schema)

    winners = VS.true_vote()
    print("true voting:", winners)

    hap = BasicHappiness(winners[0][0], true_preferences)

    hap_metric = hap.get_happiness()

    print("happiness for true voting:", hap_metric)

    print("-----strategic voting testing-----")
    strategic_vote, max_happiness, new_situation = compromise(VS, 1)
    print("strategic vote result(compromise):", strategic_vote, max_happiness, new_situation)

    print("situation with compromise voting:", VS.vote(new_situation))

    strategic_vote, max_happiness, new_situation = burying(VS, 1)
    print("strategic vote result(burying):", strategic_vote, max_happiness, new_situation)

    print("situation with burying voting:", VS.vote(new_situation))

    print("Optimal strategic vote(independent from specific strategy types):\n")
    strat_voting_all(VS, hap, hap_metric)


if __name__ == "__main__":
    main()