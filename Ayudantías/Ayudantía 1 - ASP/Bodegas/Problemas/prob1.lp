% >> Definición del problema <<
% Este problema puede ser resuelto con bound=13

% Entre que valores se mueven X e Y (dimensiones del mapa)
rangeX(0..6).
rangeY(0..7).

% El predicado obstacle(X,Y) dice que (X,Y) es un obstáculo
obstacle(1,1..6).
obstacle(3,1..6).
obstacle(5,1..6).

% Se definen todos los robots del problema y sus posiciones iniciales en T=0
robot(1..8).
on(1,0,0,0).
on(2,2,0,0).
on(3,4,0,0).
on(4,6,0,0).
on(5,0,7,0).
on(6,2,7,0).
on(7,4,7,0).
on(8,6,7,0).

% El predicado goal(R,X,Y) indica que el robot R debe llegar a X,Y
goal(1,0,7).
goal(2,2,7).
goal(3,4,7).
goal(4,6,7).
goal(5,0,0).
goal(6,2,0).
goal(7,4,0).
goal(8,6,0).
