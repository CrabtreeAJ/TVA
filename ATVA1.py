import numpy as np
from itertools import permutations, combinations, product
from happiness import BasicHappiness

def atva1(voting_system):
    true_preferences = voting_system.true_preferences
    n = len(true_preferences)

    honest_profile = np.array(true_preferences.copy())
    honest_winner = voting_system.vote(honest_profile)[0][0]

    honest_happiness = []
    for i in range(n):
        hap_model = BasicHappiness(honest_winner, true_preferences)
        honest_happiness.append(
            hap_model.get_happiness_single(true_preferences[i], honest_winner)
        )

    #iterate over coalition sizes >= 2
    for size in range(2, n + 1):

        for coalition in combinations(range(n), size):

            coalition = list(coalition)

            #generate all ballot combinations for coalition members (this scales horribly)
            perm_lists = [
                list(permutations(true_preferences[i]))
                for i in coalition
            ]

            for perm_combo in product(*perm_lists):

                profile = np.array(true_preferences.copy())

                #apply coalition manipulation
                for idx, voter_id in enumerate(coalition):
                    profile[voter_id] = perm_combo[idx]

                winner = voting_system.vote(profile)[0][0]
                hap_model = BasicHappiness(winner, true_preferences)

                improvements = []

                for voter_id in coalition:
                    new_hap = hap_model.get_happiness_single(
                        true_preferences[voter_id], winner
                    )
                    improvements.append(new_hap > honest_happiness[voter_id])

                #check if ALL coalition members strictly improve
                if all(improvements):

                    print(f"Coalition {coalition} can manipulate.")
                    print(f"New winner: {winner}")
                    print("Ballots:")

                    for idx, voter_id in enumerate(coalition):
                        print(f"  Voter {voter_id}: {perm_combo[idx]}")

                    print()
                    return 0   #stop after first found

    print("No beneficial coalition found under ATVA-1.")
    return 0