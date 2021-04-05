% >> Definición del problema <<
% Este problema puede ser resuelto con bound=3

% Entre que valores se mueven X e Y (dimensiones del mapa)
rangeX(0..2).
rangeY(0..2).

% El predicado obstacle(X,Y) dice que (X,Y) es un obstáculo
obstacle(1,1).

% Se definen todos los robots del problema y sus posiciones iniciales en T=0
robot(1..2).
on(1,0,0,0).
on(2,2,0,0).

% El predicado goal(R,X,Y) indica que el robot R debe llegar a X,Y
goal(1,2,0).
goal(2,0,0).
