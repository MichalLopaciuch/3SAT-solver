from pyeasyga import pyeasyga
import pycosat
from os import path
from timer import Timer


# __CNF_DIRECTORY__ = 'CBS_k3_n100_m403_b10'
__CNF_FILENAME__  = 'CBS_k3_n100_m403_b10_0.cnf'
__CNF_DIRECTORY__ = 'data'
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
            int_line = []
            for element in splitted_line:
                if element == '0': continue
                int_line.append(int(element))
            data.append(int_line)
        return data


__CNF__ = load_cnf()


def _cnf_to_py(cnf, candidates):
    """
    @author Michał Łopaciuch
    @description function that converts CNF format to python boolean format
    @param cnf is the matrix which contains clauses
    @param candidates is array of genetic algorithm individual's values
    """
    __clauses__ = []
    for clause in cnf:
        """ 3 because its 3SAT :) """
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


ga = pyeasyga.GeneticAlgorithm(
    list(range(0, __VARIABLES__)),
    crossover_probability=0.8,
    mutation_probability=0.5,
    population_size=200,
    generations=500,
    elitism=True
)


def fitness(member, data):
    return _cnf_to_py(__CNF__, member)



def get_combinations():
    chars = '01'
    for current in range(__VARIABLES__):
        a = [i for i in chars]
        for y in range(current):
            a = [x+i for i in chars for x in a]
    return a


def brute_force():
    combs = get_combinations()
    for combination in combs:
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
