################## NO TOCAR ####################
### Módulo para escribir archivo simulation.txt

class ToWrite:

    def __init__(self):
        self.actions = list()
        self.shots = list()
        self.write_actions = str()
        self.write_shots = str()

    def enter_action(self, action):
        if action[0] == 'goto':
            self.actions.append((action[2], action[1]))
            self.write_actions += f'{action[2]},{action[1]},'
        elif action[0] == 'shoot':
            self.shots.append((action[2], action[1]))

    def shots_calculator(self):
        for shot in self.shots:
            for action in self.actions:
                if (action[0] - 1, action[1]) == shot:
                    self.write_shots += f'{action[0]},{action[1]},'
                    break
                elif (action[0] + 1, action[1]) == shot:
                    self.write_shots += f'{action[0]},{action[1]},'
                    break
                elif (action[0], action[1] - 1) == shot:
                    self.write_shots += f'{action[0]},{action[1]},'
                    break
                elif (action[0], action[1] + 1) == shot:
                    self.write_shots += f'{action[0]},{action[1]},'
                    break



def write_simulation(base, append=False):
    ## Aca debo manejar: Si le disparo al wumpus, poner que sea
    ## cuando estoy al lado.
    if not append:
        # Esto esta bien.
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