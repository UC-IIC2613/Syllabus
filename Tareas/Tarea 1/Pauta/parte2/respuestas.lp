%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%               Pauta Parte 2                %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Este es un grafo de ejemplo, para la corrección
% pueden usar el que quieran.
arco(a,b).
arco(b,c).
arco(b,e).
arco(e,f).
% Descomentar para grafo ciclico.
% arco(b,a).

nodo(X) :- arco(X,_).
nodo(Y) :- arco(_,Y).


% PREGUNTA 1.
% Parte 1) La respuesta debe considerar el grounding que hace clingo (gringo) y como
% al contar con un grafo ciclico la instanciación se pone en todos los casos infinitamente.

% Parte 2)
% Largo no puede ser mayor a n en un grafo de n nodos.
camino(X,Y,Largo) :- arco(X,Y), Largo = 1.
camino(X,Y,Largo) :- camino(X,Z,L1), camino(Z,Y,L2), Largo = L1+L2, Largo <= #count{N : nodo(N)}.


% PREGUNTA 2.
% Descomentar para grafo no dirigido.
% arco(X,Y) :- arco(Y,X).

% Definimos predicado ilumunada/2.
% Todas las calles que llegan a esquina iluminada están iluminadas también.
ilumunada(X,Y) :- arco(X,Y), iluminado(X).

% Definimos conectado_k/3 recursivamente.
conectado_k(X,Y,0) :- arco(X,Y), ilumunada(X,Y).
conectado_k(X,Y,1) :- arco(X,Y), not ilumunada(X,Y).
conectado_k(X,Y,K) :-
            camino(X,Y,Largo), K < Largo,
            conectado_k(X,Z,K1),
            conectado_k(Z,Y,K2),
            K = K1 + K2.


% PREGUNTA 3.
% Definimos predicado camino_minimo/3.
% No es estrictamente necesario que lo hagan con el operador #min.
conectado_k_min(X,Y,K) :- conectado_k(X,Y,K), K = #min{N : conectado_k(X,Y,N)}.


% PREGUNTA 4.

% Para esta pregunta haremos un análisis de peor caso. Para esta pregunta conviene entonces
% considerar que habrá un camino de tamaño n o menos entre todo par de nodos.
%
% Así, al instanciar:
%
% * camino/2 se obtienen del orden de n^3 reglas.
% * iluminada/2 se obtienen del orden de n^2 reglas.
% * conectado_k: n^3 reglas
% * conectado_k_min/3: n^3 reglas
%
% Con esto se obtiene que el programa es cúbico en el número de nodos.
%
% Con el análisis de arriba es suficiente. Sin embargo existen maneras de involucrar
% al número de aristas en el análisis.
%
% * camino/2: Suponiendo (n m) es "n sobre m":
% el número de caminos que es posible hacer con n o menos aristas es del orden de
% (m n). Se obtiene lo mismo para conectado_k y para conectado_k_min.
%
% * iluminada/2 se obtienen del orden de n^2 reglas.


% PREGUNTA 5.
% Hay que solucionar el problema del alcalde.
% Nos ponemos en todos los casos de esquinas para iluminar.
{iluminado(X) : nodo(X)}

% Entre cada par de esquinas existe un camino con a lo más una calle sin iluminar.
:- conectado_k_min(X,Y,K), K > 1.

% Elegimos la opción que menos esquinas nos hace iluminar.
#minimize{1,X : iluminado(X)}.
