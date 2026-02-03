import numpy
from collections import Counter
from happiness import basic_happiness

from itertools import permutations

Alphabet = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
Alphabet2 = ("Z","Y","X","W","V","U","T","S","R","Q","P","O","N","M","L","K","J","I","H","G","F","E","D","C","B","A")


def vote(scheme, situation):

    winner = ""

    situation = numpy.array(situation)

    if scheme.count(1)==1 and scheme.count(2)==0: # Plurality voting
        test = situation[:,0]
        unique, count = numpy.unique(situation[:,0], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]
    elif scheme.count(1)==2: # Voting for two
        unique, count = numpy.unique(situation[:,[0,1]], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]
    elif scheme.count(1)>1 and scheme.count(0)==1: # Anti-plurality voting
        unique, count = numpy.unique(situation[:,:-1], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]
    elif scheme.count(2)>0: # Burda voting
        dictionary={}
        for x in scheme:
            unique, count = numpy.unique(situation[:,[scheme.index(x)]], return_counts=True)
            temp_dict = dict(zip(unique, count*x))
            dictionary = Counter(dictionary)+Counter(temp_dict)
        winner = sorted(dictionary.items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]

    return winner

def strat_voting_all(scheme, situation, hap, happiness):
    situation = numpy.array(situation)

    for x, column in enumerate(situation):
        for j in permutations(column):
            strat_vote_sit = numpy.insert(numpy.delete(situation, x, axis=0), x, j, axis = 0)
            strat_win = vote(scheme, strat_vote_sit)
            strat_hap = hap.get_happiness_single(column, strat_win)
            if(happiness[x]<strat_hap):
                print(f"({j}, {strat_win}, {strat_hap}, {happiness[x]}, "f"{sum(happiness) - happiness[x] + strat_hap}, {sum(happiness)})")
    return 0




def main():

    schema = [3,2,1,0]
    situation = [["A","C","B","D"],["B","D","A","C"], ["B","A","D","C"], ["C","A","D","B"], ["D","C","B","A"]]

    winner = vote(schema, situation)
    print(winner)

    hap = basic_happiness(winner, situation)

    hap_metric = hap.get_happiness()

    print(hap_metric)

    strat_voting_all(schema, situation, hap, hap_metric)


if __name__=="__main__":
    main()