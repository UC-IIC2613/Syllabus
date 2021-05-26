neigh(X,Y,Xp,Yp) :- cell(X,Y), cell(Xp,Yp), |Xp-X|+|Yp-Y|=1.

1 {pit(Xp,Yp)    : neigh(X,Y,Xp,Yp)} :- sense_breeze(X,Y).
1 {wumpus(Xp,Yp) : neigh(X,Y,Xp,Yp)}1 :- sense_stench(X,Y).

{pit(Xp,Yp)    : neigh(X,Y,Xp,Yp)} 0 :- alive(X,Y), not sense_breeze(X,Y).
{wumpus(Xp,Yp) : neigh(X,Y,Xp,Yp)} 0 :- alive(X,Y), not sense_stench(X,Y).

% no puede haber un pit y un wumpus en la misma posición
:- cell(X,Y), wumpus(X,Y), pit(X,Y).

safe(X,Y) :- cell(X,Y), not pit(X,Y), not wumpus(X,Y).

:- pit(X,Y), alive(X,Y).
:- wumpus(X,Y), alive(X,Y).

% at position 0,0 alive and sensing nothing
#show safe/2.
#show pit/2.
#show wumpus/2.
