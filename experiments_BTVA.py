from happiness import BasicHappiness
from strategic_voting import CompromiseStrategy, BuryingStrategy, BulletStrategy, BestStrategy
from voting import VotingSystem
from risk import BasicRisk
import numpy as np
import random
import string



def main(iterations: int, schema_type: str, strategy: str):

    risk_list=[]

    for x in range(iterations):
            
        num_candidates = random.randint(2,10)
        num_voters = random.randint(2,10)

        schema = generate_voting_schema(schema_type, num_candidates)

        true_preferences=[]

        for y in range(num_voters):

            voter_pref = list(string.ascii_lowercase[:num_candidates])
            random.shuffle(voter_pref)
            true_preferences.append(voter_pref)

        print(type(np.array(true_preferences)[0][0]))
        VS = VotingSystem(np.array(true_preferences), list(string.ascii_lowercase[:num_candidates]), schema)

        winners = VS.true_vote()
        print("true voting:", winners)



        basic_happiness_system = BasicHappiness(winners[0][0], true_preferences)

        happiness_metric = basic_happiness_system.get_happiness()

        print("happiness for true voting:", happiness_metric)
        print("total happiness for true voting", sum(happiness_metric))

        strategic_happiness_compiled = [0] * len(happiness_metric)

        for y in range(num_voters):


            if(strategy == "compromise"):
                strategic_vote, max_happiness, new_situation = CompromiseStrategy().find_strategy(VS, y)
                print("-----Compromise voter ", y,"-----")
                winner = VS.vote(new_situation)[0][0]
                strategic_happiness_system = BasicHappiness(winner, true_preferences)
                strategic_happiness_metric = strategic_happiness_system.get_happiness()
                strategic_happiness_compiled[y] = strategic_happiness_metric
                print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric),")")
                print("---")

            elif(strategy == "bury"):
                strategic_vote, max_happiness, new_situation = BuryingStrategy().find_strategy(VS, y)
                print("-----Bury voter ", y,"-----")
                winner = VS.vote(new_situation)[0][0]
                strategic_happiness_system = BasicHappiness(winner, true_preferences)
                strategic_happiness_metric = strategic_happiness_system.get_happiness()
                strategic_happiness_compiled[y] = strategic_happiness_metric
                print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric),")")
                print("---")

            elif(strategy == "bullet"):
                strategic_vote, max_happiness, new_situation = BulletStrategy().find_strategy(VS, y)
                print("-----Bullet voter ", y,"-----")
                winner = VS.vote(new_situation)[0][0]
                strategic_happiness_system = BasicHappiness(winner, true_preferences)
                strategic_happiness_metric = strategic_happiness_system.get_happiness()
                strategic_happiness_compiled[y] = strategic_happiness_metric
                print("(", strategic_vote, winner, strategic_happiness_metric[y], happiness_metric[y], sum(strategic_happiness_metric), sum(happiness_metric),")")
                print("---")

            elif(strategy == "best"):
                print("Optimal strategic vote(independent from specific strategy types):\n")
                strategic_vote, max_happiness, new_situation = BestStrategy().find_strategy(VS, y)
                strategic_happiness_compiled[y] = strategic_happiness_metric
                print("strategic vote result(any):", strategic_vote, "new happiness:", max_happiness, "\n", new_situation)
                print("Results with bullet voting:", VS.vote(new_situation))

        print("-----risk output-----")

        b_risk = BasicRisk(winner, true_preferences, schema)
        risk = b_risk.get_risk_from_happiness(happiness_metric, strategic_happiness_compiled)
        print(risk)
        risk_list.append(risk)
    
    print("risklist",risk_list)

    #print(risk.get_risk())


    


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
    
    main(1, borda, compromise)