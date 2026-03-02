from happiness import BasicHappiness
from strategic_voting import compromise, burying, bullet_voting, strat_voting_all
from voting import VotingSystem
import numpy as np

def main():
    schema = [1, 1, 1, 0]
    true_preferences = [["A", "C", "B", "D"], ["B", "C", "A", "D"], ["C", "B", "D", "A"], ["C", "A", "B", "D"],
                        ["D", "C", "B", "A"]]

    VS = VotingSystem(np.array(true_preferences), ['A', 'B', 'C', 'D'], schema)

    winners = VS.true_vote()
    print("true voting:", winners)

    basic_happiness = BasicHappiness(winners[0][0], true_preferences)

    hap_metric = basic_happiness.get_happiness()

    print("happiness for true voting:", hap_metric)
    print("total happiness for true voting", sum(hap_metric))

    print("-----strategic voting testing-----")
    strategic_vote, max_happiness, new_situation = compromise(VS, 0)
    print("strategic vote result(compromise):", strategic_vote, "new happiness:", max_happiness, "\n", new_situation)

    print("situation with compromise voting:", VS.vote(new_situation))

    strategic_vote, max_happiness, new_situation = burying(VS, 0)
    print("strategic vote result(burying):", strategic_vote, "new happiness:", max_happiness, "\n", new_situation)

    print("situation with burying voting:", VS.vote(new_situation))

    strategic_vote, max_happiness, new_situation = bullet_voting(VS, 0)
    print("strategic vote result(bullet):", strategic_vote, "new happiness:", max_happiness, "\n", new_situation)

    print("situation with bullet voting:", VS.vote(new_situation))

    print("Optimal strategic vote(independent from specific strategy types):\n")
    strat_voting_all(VS, BasicHappiness, hap_metric)


if __name__ == "__main__":
    main()