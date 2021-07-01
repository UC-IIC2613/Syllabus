% >> Definición del problema <<
% Este problema puede ser resuelto con bound=14

% Entre que valores se mueven X e Y (dimensiones del mapa)
rangeX(0..9).
rangeY(0..9).

% El predicado obstacle(X,Y) dice que (X,Y) es un obstáculo
obstacle(1,1..3).
obstacle(1,5..8).

obstacle(3..6,1..3).
obstacle(3..6,5..8).

obstacle(8,1..3).
obstacle(8,5..8).

% Se definen todos los robots del problema y sus posiciones iniciales en T=0
robot(1..10).
on(1,0,0,0).
on(2,9,0,0).
on(3,2,5,0).
on(4,9,9,0).
on(5,0,9,0).
on(6,8,4,0).
on(7,1,4,0).
on(8,9,5,0).
on(9,2,3,0).
on(10,3,4,0).

% El predicado goal(R,X,Y) indica que el robot R debe llegar a X,Y
goal(1,0,7).
goal(2,2,7).
goal(3,9,0).
goal(4,7,8).
goal(5,9,9).
goal(6,6,0).
goal(7,3,0).
goal(8,7,5).
goal(9,1,0).
goal(10,0,9).
