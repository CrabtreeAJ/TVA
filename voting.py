import numpy

Alphabet = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
Alphabet2 = ("Z","Y","X","W","V","U","T","S","R","Q","P","O","N","M","L","K","J","I","H","G","F","E","D","C","B","A")


def vote(scheme, situation):

    winner = ""

    situation = numpy.array(situation)

    if scheme.count(1)==1:
        unique, count = numpy.unique(situation[:,0], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]
    elif scheme.count(1)==2:
        unique, count = numpy.unique(situation[:,[0,1]], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]
    elif scheme.count(1)>1 & scheme.count(0)==1:
        unique, count = numpy.unique(situation[:,[0,1]], return_counts=True)
        winner = sorted(dict(zip(unique, count)).items(), key=lambda x: (x[1], 27-Alphabet.index(x[0])), reverse=True)[0][0]

    return winner


def main():

    schema = [1,1,1,0]
    situation = [["A","C","C"],["A","D","B"], ["B","B","B"], ["B","C","B"]]

    print(vote(schema, situation))


if __name__=="__main__":
    main()