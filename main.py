from pyeasyga import pyeasyga
import pycosat

from os import path

from timer import Timer



__CNF__ = [
    [ -1,  2,  4 ],
    [ -2,  3,  4 ],
    [  1, -3,  4 ],
    [  1, -2, -4 ],
    [  2, -3, -4 ],
    [ -1,  3, -4 ],
    [  1,  2,  3 ],
    [  1,  2,  5 ]
]

__CNF_DIRECTORY__ = 'CBS_k3_n100_m403_b10'
__CNF_FILENAME__  = 'CBS_k3_n100_m403_b10_0.cnf'
__VARIABLES__     = 100
__CLAUSES__       = 403


def load_cnf():
    """
    @author Michał Łopaciuch
    @description function that loads .cnf file and returns data as python matrix
    """
    data = []
    with open(path.join(__CNF_DIRECTORY__, __CNF_FILENAME__), 'r') as f:
        for line in f.readlines():
            if line[0] in ['c', 'p']:
                continue
            splitted_line = ' '.join(line.split()).split(' ')
            for element in splitted_line:
                element = int(element)
            data.append(splitted_line)
        return data


def _cnf_to_py(cnf, candidates):
    """
    @author Michał Łopaciuch
    @description function that converts CNF format to python boolean format
    @param cnf is the matrix which contains clauses
    @param candidates is array of genetic algorithm individual's values
    """
    __clauses__ = []
    for clause in cnf:
        temp = [None] * 3
        i = 0
        for rule in clause:
            if rule > len(candidates):
                raise Exception(f'Individual CNF value: {rule} references to undefined value.')
            if rule < 0:
                temp[i] = not bool(candidates[-1 * rule - 1])
            else:
                temp[i] = bool(candidates[rule - 1])
            i += 1
        __clauses__.append(temp[0] or temp[1] or temp[2])
    return sum([1 for res in __clauses__ if res])

print(_cnf_to_py(__CNF__, [1, 1, 1, 0, 0]))

def get_score(x1, x2, x3, x4):
    __CLAUSES__ = [
        ((not x1) or x2 or x4),
        ((not x2) or x3 or x4),
        (x1 or (not x3) or x4),
        (x1 or (not x2) or (not x4)),
        (x2 or (not x3) or (not x4)),
        ((not x1) or x3 or (not x4)),
        (x1 or x2 or x3)
    ]
    return sum([1 for res in __CLAUSES__ if res])


ga = pyeasyga.GeneticAlgorithm(
    [0, 1, 2, 3, 4],
    mutation_probability=0.05,
    population_size=200,
    generations=100,
    elitism=True
)


def fitness(member, data):
    # return get_score(member[0], member[1], member[2], member[3])
    return _cnf_to_py(__CNF__, member)



def get_combinations():
    chars = '01'
    for current in range(5):
        a = [i for i in chars]
        for y in range(current):
            a = [x+i for i in chars for x in a]
    return a


def brute_force():
    for combination in get_combinations():
        if _cnf_to_py(__CNF__, combination) == len(__CNF__):
            return combination
    return -1


def main():
    ga.fitness_function = fitness
    t1 = Timer('Genetic algorithm')
    ga.run()
    t1.stop()
    print(ga.best_individual(), t1.get_interval())

    t2 = Timer('DPLL algorithm')
    dpll_res = pycosat.solve(__CNF__)
    t2.stop()
    print(dpll_res, t2.get_interval(100))

    t3 = Timer('Brute force')
    bf_res = brute_force()
    t3.stop()
    print(bf_res, t3.get_interval(100))


if __name__ == '__main__':
    main()
