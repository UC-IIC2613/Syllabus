% RECORDAR QUE ESTA PAUTA NO RESUELVE EL HECHO DE QUE SE TRANSMUTEN LAS POSICIONES DE LOS ROBOTS
% ADEMÁS, LOS 'bound' SEÑALADOS SON PARA CUANDO RESUELVAN DICHO PROBLEMA. ESTO QUEDA COMO DESAFÍO :)

% Existirá un máximo de instantes de tiempo, denotado por la constante bound que se puede ingresar 
% por consola o predefinirla:
time(1..bound).

% Los robots cuentan con 5 acciones posibles, moverse en las 4 direcciones o no hacer nada
action(up).
action(down).
action(left).
action(right).
action(wait).

% Para cada instante de tiempo T, cada robot R puede ejecutar una única acción de las 5 posibles:
1 {exec(R,A,T) : action(A)} 1 :- robot(R), time(T+1).

% El predicado 'on' indica que un robot R, está en una posición (X,Y) en un tiempo T. Por su parte, 
% el predicado 'exec' muestra que el robot R ejecuta la acción A en un tiempo T. Por lo tanto, se 
% puede definir la posición de un robot en T+1 según la acción A que se haya ejecutado:
on(R,X,Y+1,T+1) :- exec(R,up,T), on(R,X,Y,T), time(T+1).
on(R,X,Y-1,T+1) :- exec(R,down,T), on(R,X,Y,T), time(T+1).
on(R,X-1,Y,T+1) :- exec(R,left,T), on(R,X,Y,T), time(T+1).
on(R,X+1,Y,T+1) :- exec(R,right,T),on(R,X,Y,T), time(T+1).
on(R,X,Y,T+1)   :- exec(R,wait,T), on(R,X,Y,T), time(T+1).

% El predicado goal(R,X,Y) señala que el robot R debe llegar a (X,Y), por su parte, el predicado 
% at_goal(R,T) indica que el robot R está en su objetivo en el tiempo T:
at_goal(R,T) :- on(R,X,Y,T), goal(R,X,Y).

% Se descartan los modelos en los que un robot haya ejecutado una acción que lo sacaría del mapa:
:- on(R,X,Y,T), not rangeX(X).
:- on(R,X,Y,T), not rangeY(Y).

% Se descaartan los modelos en los que un robot haya ejecutado una acción que lo haga chocar:
:- on(R,X,Y,T), obstacle(X,Y).

% Se descartan los modelos donde, luego de ejecutar una acción, dos robots queden en el mismo lugar:
:- on(R1,X,Y,T), on(R2,X,Y,T), R1 != R2.

% Se descartan aquellos modelos en los que en el tiempo final el robot no esté en su objetivo:
:- robot(R), not at_goal(R,bound).

% [NO BORRAR] El resto de líneas son necesarias para que el visualizador funcione correctamente:
goal(R,X,Y,T) :- goal(R,X,Y), time(T).
goal(R,X,Y,0) :- goal(R,X,Y).

#show on/4.
#show obstacle/2.
#show rangeX/1.
#show rangeY/1.
#show exec/3.
#show goal/4.
