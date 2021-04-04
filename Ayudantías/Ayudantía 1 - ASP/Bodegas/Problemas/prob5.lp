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
robot(1..4).
on(1,4,4,0).
on(2,5,4,0).
on(3,4,5,0).
on(4,5,5,0).

% El predicado goal(R,X,Y) indica que el robot R debe llegar a X,Y
goal(1,1,0).
goal(2,1,9).
goal(3,9,5).
goal(4,0,5).
