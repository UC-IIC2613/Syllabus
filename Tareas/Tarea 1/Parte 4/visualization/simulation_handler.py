################## NO TOCAR ####################
### Módulo para escribir archivo simulation.txt

def write_simulation(base, append=False):
    if not append:
        with open('simulation.txt', 'w') as f:
            player = str()
            pits = str()
            wumpus = str()
            gold = str()
            with open(base, 'r') as f_two:
                lines = f_two.readlines()
                dimensions = [int(x) for x in lines[0].split(',')]
                for x in range(dimensions[1]):
                    for y in range(dimensions[0]):
                        c = lines[1+y][x]
                        if c == '@':
                            pits += f'{x},{y},'
                        elif c == 'W':
                            wumpus += f'{x},{y},'
                        elif c == 'G':
                            gold += f'{x},{y},'
                        elif c == 'I':
                            player += f'{x},{y}'
            f.write(f'{dimensions[0]},{dimensions[1]}\n')
            f.write(f'{player}\n')    
            f.write(f'{gold[:-1]}\n')
            f.write(f'{wumpus[:-1]}\n')
            f.write(f'{pits[:-1]}\n')
    else:
        with open('simulation.txt', 'a') as f:
            f.write(base)