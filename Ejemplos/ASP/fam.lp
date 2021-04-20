padre(luis, jorge). % luis es padre de jorge
padre(luis, ximena).
madre(maria, luis).
madre(maria, ximena).
padre(jorge, benjamin).
padre(jorge, valentina).
madre(ximena, matias).
madre(ximena, camila).

progenitor(X,Y) :- madre(X,Y).
progenitor(X,Y) :- padre(X,Y).

hermano(X,Y) :- progenitor(Z,X), progenitor(Z,Y).


abuele(X,Y) :- progenitor(X, Z), progenitor(Z, Y).
abuela(X,Y) :- madre(X, Z), progenitor(Z, Y).

% predicado hermanx
% predicado primo/a
