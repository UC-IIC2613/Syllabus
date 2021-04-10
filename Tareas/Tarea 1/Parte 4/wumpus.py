from agent import Agent
from environment import Environment
from visualization.simulation_handler import write_simulation, ToWrite

MAXSTEPS = 1000
simulation_handler = ToWrite()

base_map = 'maps/map.txt'
env = Environment(base_map, False)  # segundo argumento indica si el número de wumpus y pits es observable
agt = Agent(env)
# mueve al agente a la posición inicial
next_action = ['goto', env.init_x, env.init_y]
steps = 0
shots = 0
while steps < MAXSTEPS:
    state = env.execute(next_action)
    env.show_map()
    if state == 'dead':
        print('Perdiste, estás muerto!!')
        break
    if state == 'illegal_shooting':
        print('Descalificado por disparar más de la cuenta!')
        break
    elif state == 'gold':
        print('Encontraste el oro en', steps, 'pasos!! Felicidades!')
        break
    else:
        # dada la posición actual
        # y la percepción en x, y
        # retorna una posición (x,y) donde moverse
        perceptions = env.get_perceptions()
        print('Perceptions:', perceptions)
        next_action = agt.get_action(perceptions)
        print('Agent juega:', next_action)
        simulation_handler.enter_action(next_action)
        if next_action[0] == 'goto' and not env.is_neighbor(next_action[1], next_action[2], env.agent_x, env.agent_y):
            print('jugada ilegal: no puedes moverte a una celda no vecina de la actual')
            break
        if next_action == ('unsolvable'):
            print(
                'Agente afirma que no se puede resolver este problema después de {} pasos.'.format(steps))
            break
    steps += 1

#### NO TOCAR ####
write_simulation(base_map)
simulation_handler.shots_calculator()
write_element = f'{simulation_handler.write_actions[:-1]}\n{simulation_handler.write_shots[:-1]}' \
    if simulation_handler.shots else f'{simulation_handler.write_actions[:-1]}'
write_simulation(write_element, True)
