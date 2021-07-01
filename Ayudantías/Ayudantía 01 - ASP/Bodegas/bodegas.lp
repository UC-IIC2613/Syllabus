% 1) Definir predicado para los instantes de tiempo con una cota superior dada por una constante:

% 2) Definir predicado con las acciones posibles que puede hacer un robot en un instante T:

% 3) Para cada instante T, cada robot R debe ejecutar una única acción de todas las posibles:

% 4) Definir predicado que determine el cómo se establecen las posiciones según las acciones hechas:

% 5) Definir un predicado que indique si un robot llegó o no a su objetivo:

% 6) Descartar modelos que no cumplan con restricciones lógicas:

% [NO BORRAR] El resto de líneas son necesarias para que el visualizador funcione correctamente:
goal(R,X,Y,T) :- goal(R,X,Y), time(T).
goal(R,X,Y,0) :- goal(R,X,Y).

#show on/4.
#show obstacle/2.
#show rangeX/1.
#show rangeY/1.
#show exec/3.
#show goal/4.
