from happiness import BasicHappiness
from strategic_voting import CompromiseStrategy, BuryingStrategy, BulletStrategy, BestStrategy
from ATVA4 import ATVA4_compromise, ATVA4_burying, ATVA4_bullet_voting, ATVA4_strat_voting_all
from ATVA3 import ATVA3_imperfect_knowledge
from ATVA2 import atva2_sit
from voting import VotingSystem
from risk import BasicRisk
import numpy as np
import random
import string
import csv



def main(schema_type: str, strategy: str, TVA: str, iterations: int):

    
    risk_list = []

    for num_candidates in range(2, 11):
        for num_voters in range(2, 11):
            risk_list_iteration = []
            for iteration in range(iterations):

                

                schema = generate_voting_schema(schema_type, num_candidates)

                true_preferences = []

                for y in range(num_voters):
                    voter_pref = list(string.ascii_lowercase[:num_candidates])
                    random.shuffle(voter_pref)
                    true_preferences.append(voter_pref)

                #print(type(np.array(true_preferences)[0][0]))
                VS = VotingSystem(np.array(true_preferences), list(string.ascii_lowercase[:num_candidates]), schema)

                winners = VS.true_vote()
                #print(f"[candidates={num_candidates}, voters={num_voters}, iter={iteration}] true voting:", winners)

                basic_happiness_system = BasicHappiness(winners[0][0], true_preferences)
                happiness_metric = basic_happiness_system.get_happiness()

                #print("happiness for true voting:", happiness_metric)
                #print("total happiness for true voting", sum(happiness_metric))

                strategic_happiness_compiled = [0] * len(happiness_metric)

                if TVA == "ATVA4":
                    if strategy == "compromise":
                        new_situation = ATVA4_compromise(VS)
                    elif strategy == "bury":
                        new_situation = ATVA4_burying(VS)
                    elif strategy == "bullet":
                        new_situation = ATVA4_bullet_voting(VS)
                
                    winner = VS.vote(new_situation)[0][0]
                    strategic_happiness_system = BasicHappiness(winner, true_preferences)
                    strategic_happiness_metric = strategic_happiness_system.get_happiness()
                    strategic_happiness_compiled = np.diag(strategic_happiness_metric)
                
                elif TVA == "ATVA1":
                    if strategy == "compromise":
                        new_situation = ATVA4_compromise(VS)
                    elif strategy == "bury":
                        new_situation = ATVA4_burying(VS)
                    elif strategy == "bullet":
                        new_situation = ATVA4_bullet_voting(VS)

                    winner = VS.vote(new_situation)[0][0]
                    strategic_happiness_system = BasicHappiness(winner, true_preferences)
                    strategic_happiness_metric = strategic_happiness_system.get_happiness()
                    strategic_happiness_compiled = np.diag(strategic_happiness_metric)

                else:

                    for y in range(num_voters):

                        new_situation=""

                        if strategy == "compromise":
                            if TVA == "BTVA":
                                _, _, new_situation = CompromiseStrategy().find_strategy(VS, y)
                            elif TVA == "ATVA2":
                                new_situation = atva2_sit(VS, CompromiseStrategy(), y)
                            elif TVA == "ATVA3":
                                new_situation = ATVA3_imperfect_knowledge(VS, CompromiseStrategy(), y)
                            #print("-----Compromise voter ", y, "-----")
                            #print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric), ")")
                            #print("---")

                        elif strategy == "bury":
                            if TVA == "BTVA":
                                _, _, new_situation = BuryingStrategy().find_strategy(VS, y)
                            elif TVA == "ATVA2":
                                new_situation = atva2_sit(VS, BuryingStrategy(), y)
                            elif TVA == "ATVA3":
                                new_situation = ATVA3_imperfect_knowledge(VS, BuryingStrategy(), y)
                            #print("-----Bury voter ", y, "-----")
                            #print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric), ")")
                            #print("---")

                        elif strategy == "bullet":
                            if TVA == "BTVA":
                                _, _, new_situation = BulletStrategy().find_strategy(VS, y)
                            elif TVA == "ATVA2":
                                new_situation = atva2_sit(VS, BulletStrategy(), y)
                            elif TVA == "ATVA3":
                                new_situation = ATVA3_imperfect_knowledge(VS, BulletStrategy(), y)
                            #print("-----Bullet voter ", y, "-----")
                            #print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric), ")")
                            #print("---")

                        elif strategy == "best":
                            #print("Optimal strategic vote (independent from specific strategy types):\n")
                            _, _, new_situation = BestStrategy().find_strategy(VS, y)
                            #print("strategic vote result(any):", strategic_vote, "new happiness:", max_happiness, "\n", new_situation)
                            #print("Results with bullet voting:", VS.vote(new_situation))


                        winner = VS.vote(new_situation)[0][0]
                        strategic_happiness_system = BasicHappiness(winner, true_preferences)
                        strategic_happiness_metric = strategic_happiness_system.get_happiness()
                        strategic_happiness_compiled[y] = strategic_happiness_metric

                #print("-----risk output-----")

                b_risk = BasicRisk(winner, true_preferences, schema)
                risk = b_risk.get_risk_from_happiness(happiness_metric, strategic_happiness_compiled)
                #print(risk)
                risk_list_iteration.append(round(risk,2))
            
            risk_list.append({
                "num_candidates": num_candidates,
                "num_voters": num_voters,
                "total_risk": round(sum(risk_list_iteration),2),
                "avg_risk": round(sum(risk_list_iteration)/iterations,2),
                "n": iterations
            })            
            print(num_candidates, num_voters)

    save_results(risk_list, schema, strategy, f"{TVA}_{schema_type}_{strategy}")
    #print("risk_list", risk_list)    




def save_results(risk_list: list, schema_type: str, strategy: str, filename: str = None):
    if filename is None:
        filename = f"risk_results_{schema_type}_{strategy}.csv"
    
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_candidates", "num_voters", "avg_risk"])
        
        for i, risk in enumerate(risk_list):
            num_candidates = (i // 9) + 2
            num_voters = (i % 9) + 2
            writer.writerow([num_candidates, num_voters, risk])
    
    print(f"Saved to {filename}")


def generate_voting_schema(schema_type: str, size: int) -> list:
    schema_type = schema_type.lower().replace(" ", "_")
    
    if schema_type == "plurality":
        return [1] + [0] * (size - 1)
        
    elif schema_type == "voting_for_two":
        if size < 2: return [1] * size
        return [1, 1] + [0] * (size - 2)
        
    elif schema_type == "anti_plurality":
        if size < 1: return []
        return [1] * (size - 1) + [0]
        
    elif schema_type == "borda":
        return [i for i in range(size - 1, -1, -1)]
        
    else:
        raise ValueError(f"Unknown strategy: {schema_type}")





if __name__ == "__main__":

    plurality = "plurality"
    voting_for_two = "voting_for_two"
    anti_plurality = "anti_plurality"
    borda = "borda"

    compromise = "compromise"
    bury = "bury"
    bullet = "bullet"
    best = "best"

    BTVA = "BTVA"
    ATVA1 = "ATVA1"
    ATVA2 = "ATVA2"
    ATVA3 = "ATVA3"
    ATVA4 = "ATVA4"

    
    main(borda, bullet, ATVA1, 50)
    main(borda, compromise, ATVA1, 50)
    main(borda, bury, ATVA1, 50)
    main(anti_plurality, bullet, ATVA1, 50)
    main(anti_plurality, compromise, ATVA1, 50)
    main(anti_plurality, bury, ATVA1, 50)
    main(voting_for_two, bullet, ATVA1, 50)
    main(voting_for_two, compromise, ATVA1, 50)
    main(voting_for_two, bury, ATVA1, 50)
    main(plurality, bullet, ATVA1, 50)
    main(plurality, compromise, ATVA1, 50)
    main(plurality, bury, ATVA1, 50)