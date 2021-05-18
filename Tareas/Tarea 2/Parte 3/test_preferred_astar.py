print('Iniciando NN')
from puzzle_nn_new import Puzzle
from preferred_astar import PrefAstar

def load_problems(problems):  ## carga los problemas en memoria
    f = open('problems.txt')
    while f:
        line = f.readline()
        line = line.rstrip()
        numlist = line.split(' ')
        if len(numlist) < 15:
            return
        problems.append(Puzzle([int(x) for x in numlist[1:]]))


show_solutions = False        # mostramos las soluciones?

heuristic = Puzzle.zero_heuristic  # h = 0 -- búsqueda ciega
heuristic = Puzzle.manhattan       # heuristica basda en distancia manhattan
#heuristic = Puzzle.linear_conflicts

print('%5s%10s%10s%10s%10s%10s' % ('#prob','#exp', '#gen', '|sol|', 'tiempo','maxsubopt'))
problems = []
load_problems(problems)
total_time = 0
total_cost = 0
total_expansions = 0
num_problems = len(problems)   # comentar si no quieres ejecutar sobre todos los problemas (y descomentar línea siguiente)
#num_problems = 10             # solo ejecutamos los primeros 10 problemas
for prob in range(0, num_problems):
    init = problems[prob]
    s = PrefAstar(init, heuristic, 9, 10, 1.6)
    result = s.search()
    print('%5d%10d%10d%10d%10.2f%10.2f' % (prob+1, s.expansions, len(s.generated), result.g, s.end_time-s.start_time, s.estimate_suboptimality()))
    total_time += s.end_time - s.start_time
    total_cost += result.g
    total_expansions += s.expansions
    if show_solutions:
        print(result.trace())
print('Tiempo total:        %.2f'%(total_time))
print('Expansiones totales: %d'%(total_expansions))
print('Costo total:         %d'%(total_cost))
