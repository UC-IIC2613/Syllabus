p ; q :- r.
r.

:- p. % es una restricción que dice que p no puede estar en un modelo
      % filtro: saca aquellos candidatos a modelo que contienen p
% antes de mirar la regla de la linea 4 estos podrían haber sido modelos:
%M={r,p}  NO
%M={r,q}
%M={r,p,q} NO


%M={p,q,r}


%z :- p.

%M = {r, p}
%M = {r, q}
%M = {r, p, q, z}  : no es minimal!!
