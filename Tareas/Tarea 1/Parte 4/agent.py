import sys
import os
import queue

class Agent:
    def __init__(self, env):
        self.env = env
        self.x = env.init_x      # tamaño de la grilla
        self.y = env.init_y
        self.visited = set()     # celdas ya visitadas
        self.visited.add((self.x, self.y))
        self.frontier = set()    # al profesor le fue util mantener esta variable
        for n in env.neighbors(self.x, self.y):
            self.frontier.add(n)
        self.path = []           # self.path es el camino que estamos siguiendo
                                 # no es necesario que uses este atributo, pero al
                                 # profe le fue útil



    # get_action(self, perceptions) supone que perceptions es una lista de
    # strings [s1,...,sn] donde si es sense_breeze(x,y) o sense_stench(x,y) para algúun x,y
    # debe retornar:
    #   - una tupla de la forma ('goto',x,y) para hacer que el agente se mueva a (x,y)
    #   - una tupla de la forma ('shoot',x,y) para hacer que el agente dispare a (x,y)
    #   - una tupla de la forma ('unsolvable') cuando el agente ha demostrado que el problema
    #     no tiene una solución segura
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


        def unsat_without(atom):
            # Consiedera completar e implementar este método
            # No es obligatorio que lo hagas, pero al profesor le fue útil.
            # Dado un cierto atom, arma un archivo extra.lp, el método retorna True
            # si y solo si el programa que resulta de considerar wumpus.lp y extra.lp
            # es tal que NO tiene modelos que no contienen a atom

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

            # COMPLETAR - aquí se eliminaron 13 líneas de la solución (incluyendo comentarios)
            fextra = open('extra.lp', 'w')
            fextra.write(extra)
            fextra.close()
            os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> /dev/null')
            # si usas Windows, la siguiente línea debiera funcionar
            # os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> NUL')
            models = get_models('out.txt')
            return models == []

        # COMPLETAR - aquí se eliminaron 29 líneas de la solución (incluyendo comentarios)
