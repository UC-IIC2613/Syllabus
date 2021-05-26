import sys
import os
import queue

class Agent:
    def __init__(self, env):
        self.env = env
        self.x = env.init_x
        self.y = env.init_y
        self.visited = set()
        self.visited.add((self.x, self.y))
        self.frontier = set()
        for n in env.neighbors(self.x, self.y):
            self.frontier.add(n)
        self.path = []  # camino que estamos siguiendo
    
    def get_action(self, perceptions):

        def find_path(startx, starty, goalx, goaly, safe_area):
            # encuentra un camino entre (startx,starty) a (goalx,goaly)
            # pasando solo por celdas de safe_area
            
            if (startx, starty) == (goalx, goaly):
                return True, []
            closed = set()
            fr = queue.Queue()
            fr.put((startx, starty, []))
            while not fr.empty():
                (x, y, path) = fr.get()
                closed.add((x,y))
                for (nx, ny) in self.env.neighbors(x, y):
                    if (nx, ny) in closed:
                        continue
                    newpath = path + [(nx, ny)]
                    if (nx, ny) == (goalx, goaly):
                        return True, newpath
                    else:
                        if (nx, ny) in safe_area:
                            fr.put((nx, ny, newpath))
            return False, []
            
        ''' unsat_without(atom)
            computa modelos de wumpus.lp + información de percepcion 
            tales que *no* contienen a atom
            retorna True si el programa resultante no tiene modelos
            retorna False en caso contrario
       ''' 
        def unsat_without(atom):     
            def get_models(filename):  # extrae los modelos desde filename
                f = open(filename, 'r')
                lines = f.readlines()
                lines = [l.strip() for l in lines]
                if 'SATISFIABLE' in lines:
                    answers = []
                    i = 0
                    while True:
                        while i < len(lines) - 1 and lines[i].find('Answer:', 0) == -1:
                            i += 1
                        if i == len(lines) - 1:
                            return answers
                        i += 1
                        answers.append(lines[i].split(' '))
                    return answers                    
                elif 'UNSATISFIABLE' in lines:
                    return []
                print(filename, 'no es un output legal de clingo')
                return []

            extra = 'cell(0..{},0..{}).\n'.format(self.env.get_size_x(), self.env.get_size_y())
            # agregamos a extra las reglas que expresan las percepciones
            for (vx, vy) in self.visited:
                extra += 'alive({},{}).\n'.format(vx, vy)
            if perceptions != []:
                extra += ".\n".join(perceptions) + ".\n"
            extra += ":- {}.\n".format(atom)
            # si el ambiente es observable, sabemos cuántos pozos y wumpus hay
            if self.env.is_observable():
                num_pits = self.env.get_num_pits()
                num_wumpus = self.env.get_num_wumpus()
                extra += str(num_pits)   + ' {pit(X,Y) : cell(X,Y)} '    + str(num_pits)+ '.\n'
                extra += str(num_wumpus) + ' {wumpus(X,Y) : cell(X,Y)} ' + str(num_wumpus)+ '.\n'
            # llevamos el contenido de extra al archivo extra.lp
            fextra = open('extra.lp', 'w')
            fextra.write(extra)
            fextra.close()
            os.system('clingo -n 0 wumpus.lp extra.lp > out.txt')
            models = get_models('out.txt')
            #print('MODELS=', models)
            return models == []

        if self.path != []:
            print('PATH=', self.path)
            (next_x, next_y) = self.path.pop(0)
            return ('goto', next_x, next_y)
        else:
            # we are going to move now; compute the frontier
            found_safe = False
            print('FRONTIER = ', self.frontier)
            for (nx, ny) in self.frontier:
                #print('Checking safety of ({},{})'.format(nx, ny))
                if unsat_without('safe({},{})'.format(nx, ny)):
                    is_found, path = find_path(self.x, self.y, nx, ny, self.visited)
                    assert is_found
                    print('found path to ({},{}) is {}'.format(nx,ny, path))
                    self.path = path
                    found_safe = True
                    break
            if found_safe:
                (x, y) = self.path[-1]
                self.visited.add((x, y))
                self.frontier.remove((x, y))
                for n in self.env.neighbors(x, y):
                    if n not in self.visited:
                        self.frontier.add(n)
                self.x = x
                self.y = y
                next_x, next_y = self.path.pop(0)
                return ('goto', next_x, next_y)
            else:
                for (nx, ny) in self.frontier:
                    if unsat_without('wumpus({},{})'.format(nx, ny)):
                        return (('shoot', nx, ny))
                return (('unsolvable'))
