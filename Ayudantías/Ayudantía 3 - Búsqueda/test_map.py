from map import Map
from cell import Cell
from blind_search import GenericSearch

m = Map('small_maze.txt')
init = Cell(m.init_x, m.init_y, m)
s = GenericSearch(init, 'bfs')
result = s.search(steps=True)
print("expansions:", s.expansions)
print("Size of Open:", len(s.open))
print("Size of Generated:", len(s.generated))
if result:
    print('Solution depth:', result.depth)
    trace = result.trace()
    open_positions = set()
    for c in s.open.items: # agregamos estados de la open
        open_positions.add((c.state.x, c.state.y))
    generated_positions = set()
    for c in s.generated:
        pos = (c.x, c.y)
        if pos not in open_positions: # agregamos de la closed (Generated - Open)
            generated_positions.add(pos)
    m.draw_solution(trace, generated_positions, open_positions)
else:
    print('no hay solucion')
