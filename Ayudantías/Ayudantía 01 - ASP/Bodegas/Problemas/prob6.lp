% >> Definición del problema <<
% Este problema puede ser resuelto con bound=9

% Entre que valores se mueven X e Y (dimensiones del mapa)
rangeX(0..9).
rangeY(0..9).

% El predicado obstacle(X,Y) dice que (X,Y) es un obstáculo
obstacle(0,0).
obstacle(2..3,0).
obstacle(6..7,0).
obstacle(9,0).
obstacle(0,2).
obstacle(0,4).
obstacle(0,6).
obstacle(9,2).
obstacle(9,4).
obstacle(9,6).
obstacle(0,8..9).
obstacle(2..3,9).
obstacle(6..7,9).
obstacle(9,8..9).

% Se definen todos los robots del problema y sus posiciones iniciales en T=0
robot(1..12).
on(1,4,4,0).
on(2,5,4,0).
on(3,4,5,0).
on(4,5,5,0).
on(5,4,3,0).
on(6,5,3,0).
on(7,4,6,0).
on(8,5,6,0).
on(9,3,4,0).
on(10,3,5,0).
on(11,6,4,0).
on(12,6,5,0).

% El predicado goal(R,X,Y) indica que el robot R debe llegar a X,Y
goal(1,1,0).
goal(2,1,9).
goal(3,9,5).
goal(4,0,5).
goal(5,4,9).
goal(6,8,0).
goal(7,0,7).
goal(8,5,0).
goal(9,4,0).
goal(10,0,3).
goal(11,9,1).
goal(12,9,3).
