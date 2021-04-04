% Si queremos definir variables que representen varios años consecutivos podemos hacerlo a mano, de-
% clarando una sentencia para cada uno de sus valores, pero también podemos automatizarlo y resumir-
% lo con la siguiente sintáxis:
year(2019..2021).

% También se pueden definir variables en el programa para realizar lo anterior:
#const end_1 = 2021.
year_const(2019..end_1).

% También se puede hacer ingresando el valor de constantes mediante los flags en la terminal (si se 
% referencia la variable y no se ingresó su valor, entonces el programa se interrumpe):
year_flag(2019..end_2).
