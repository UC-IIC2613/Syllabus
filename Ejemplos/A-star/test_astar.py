from puzzle import Puzzle
from astar import Astar


problems = []
init = Puzzle([0, 1, 5, 3, 6, 2, 7, 8, 4])  # a profundidad 14
problems.append(init)
init = Puzzle([0, 1, 8, 6, 2, 7, 5, 4, 3])  # a profundidad 18
problems.append(init)
init = Puzzle([5, 8, 0, 3, 7, 4, 6, 1, 2])  # a profundidad 22
problems.append(init)
init = Puzzle([5, 2, 1, 8, 7, 3, 4, 6, 0])  # a profundidad 26
problems.append(init)
init = Puzzle([0, 7, 6, 1, 4, 3, 2, 5, 8])  # a profundidad 30
problems.append(init)



# problems = []
# problems.append(Puzzle([1, 5, 2, 3, 4, 10, 14, 7, 8, 6, 0, 11, 12, 9, 13, 15]))  # a profundidad 10
# problems.append(Puzzle([4, 1, 2, 3, 5, 9, 11, 6, 8, 10, 0, 14, 12, 13, 15, 7]))  # a profundidad 12
# problems.append(Puzzle([1, 10, 5, 3, 8, 4, 2, 7, 0, 6, 14, 11, 12, 9, 13, 15]))  # a profundidad 14
# problems.append(Puzzle([4, 2, 6, 3, 8, 5, 7, 11, 12, 1, 9, 10, 13, 14, 15, 0]))  # a profundidad 16
# problems.append(Puzzle([4, 2, 3, 7, 5, 9, 10, 11, 8, 1, 14, 6, 12, 0, 13, 15]))  # a profundidad 18
# problems.append(Puzzle([5, 1, 0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
#problems.append(Puzzle([0, 1, 9, 7, 11, 13, 5, 3, 14, 12, 4, 2, 8, 6, 10, 15]))
#problems.append(Puzzle([14, 1, 9, 6, 4, 8, 12, 5, 7, 2, 3, 0, 10, 11, 13, 15]))

print('%10s%10s%10s%10s' % ('#exp', '#gen', '|sol|','tiempo'))
for init in problems:
    s = Astar(init, 'manhattan')
    result = s.search()
    print('%10d%10d%10d%10.2f' % (s.expansions, len(s.generated), result.g,s.end_time-s.start_time))
#    print(result.trace())
