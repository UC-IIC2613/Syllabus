% "Programación en Lógica" -> Deducción
% Answer Set Programming
% El "answer" del programa contiene todos los atomos que se deducen
% del programa
% Al answer también se le llama 'modelo'


% todos los gatos son animales
animal(X) :- gato(X).  % Si X es un gato entonces X es un animal
%gato(X) :- animal(X).  % Si X es un gato entonces X es un animal
gato(felix).           % felix es un gato ASP (Answer set programming)
gato(gordo).
animal(jorge).


mamifero(X) :- perro(X).
mamifero(X) :- gato(X).
perro(pluto).
%respira(X) :- mamifero(X). % esto es una "regla" o "sentencia"


% p(a).
% p(b).
% q(b).
% s(b).
% s(a).
%
% %cabeza :- cuerpo.
% r(X,Y) :- p(X), q(Y), s(X).  % cuando se da p(X) y q(Y) deduzco r(X,Y)

equipoA(a).
equipoA(b).
equipoB(a).
equipoB(b).

%cabeza :- cuerpo.
amigo(X,Y) :- equipoA(X), equipoB(Y), X!=Y.  % cuando se da p(X) y q(Y) deduzco r(X,Y)
