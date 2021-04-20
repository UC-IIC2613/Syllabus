planta(tomate).
planta(durazno).
planta(uva).
planta(oregano).

regador(r1).
regador(r2).
regador(r3).

% riega(R,P) el regador R riega a la planta P
riega(r1, durazno).
riega(r1, uva).
riega(r2, tomate).
riega(r3, oregano).
riega(r2, oregano).

% encendido(R) expresa el regador R está encendido

% expreso que quiero generar modelos en donde un regador esté encendido
1 {encendido(r1); encendido(r2); encendido(r3)} 1.

regada(P) :- planta(P), riega(R, P), encendido(R).

:- not regada(tomate).

#show regada/1.
#show encendido/1.
