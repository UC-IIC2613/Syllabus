cell(0..4,0..4).
alive(1,2).
alive(0,3).
alive(1,3).
alive(0,2).
sense_breeze(1,3).
sense_stench(0,2).
:- safe(0,1).
3 {pit(X,Y) : cell(X,Y)} 3.
1 {wumpus(X,Y) : cell(X,Y)} 1.
