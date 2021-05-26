# Pregunta 1

## Solución
Podemos demostrarlo siguiendo el algoritmo para construir modelos descrito en la pregunta 3. Cualquier ejecución sobre $\Pi$ es claramente una ejecución parcial sobre $\Pi'$. Dicho de otro modo, al construir un modelo para $\Pi'$ primero consideramos las cláusulas solo en $\Pi$ y agregamos átomos al modelo. Una vez que no podemos seguir, consideramos las reglas que no están en $\Pi$ para seguir agregando más átomos en el modelo y así obtener un modelo que es un superconjunto del modelo de $\Pi$.


## Criterios de Puntaje:
1) La demostración es correcta y sigue una lógica consistente (no es estrictamente necesario que haya sido demostrada por contradicción).
2) Usa la definición de modelo de programa sin negación.


# Pregunta 2

## Solución
Siguiendo el razonamiento de la pregunta 1, cuando agregamos una regla Head <- Body a un programa $Pi$ tal que |Head| = 1, si M es un modelo, entonces obtenemos un modelo M' que es un superconjunto de M. Por otro lado, cuando agregamos una regla {} <-Body a un programa con un cierto modelo M, si es que Body está en M, entonces la regla en efecto 'filtra' M y por lo tanto M no es modelo del programa extendido; en caso contrario (Body no pertenece a M), M también es un modelo del programa extendido. Con estas dos observaciones, continuamos la demostración por inducción en el número de reglas del programa.

- Caso base es un programa con 0 reglas, que tiene un único modelo.
- Supongamos que $\Pi$, que tiene $n$ reglas, es un programa que tiene a lo más un modelo. Consideramos el programa $\Pi'=\Pi\cup Head \leftarrow Body$, y ahora, tomando en cuenta la observación anterior concluimos \Pi' tiene un modelo que es una extensión del modelo de Pi (con más átomos), o, simplemente la nueva regla filtra el modelo de Pi, quedando \Pi' con 0 modelos.




## Criterios de Puntaje:
1) Si no se demuestra por inducción la demostración debe ser correcta y tener lógica consistente.
2) Si se demuestra por inducción:
   1) Base Inductiva bien definida (para n=0, programa vacío).
   2) Hipótesis inductiva bien definida para n=k
   3) Tesis inductiva bien definida para n=k+1, donde se hace uso de la hipótesis inductiva.


# Pregunta 3

## Solución
Primero el algoritmo identifica los literales que aparecen negados en el modelo. Sea Neg ese conjunto de átomos. Ahora en la primera fase generamos agregamos a M algunos átomos de Neg. Hacemos esto usando un algoritmo estilo backtracking que, recursivamente puede generar todas las combinaciones posibles de átomos. Una vez hecho esto, corremos el algoritmo descrito en el enunciado. Al terminar, almacenamos el modelo candidato obtenido en un conjunto. Una vez terminado el proceso recursivo filtramos los modelos obtenidos, para asegurarnos que entregamos modelos minimales.

Ahora el análisis de complejidad. El algoritmo del enunciado puede ejecutar máximo |Pos| iteraciones, donde |Pos| es el conjunto de átomos no negados del programa original. Cada iteración supondremos toma cierto tiempo constante.

La complejidad de generar los modelos 2^|Neg| modelos candidatos es: 2^|Neg| * |Pos|
Para filtrar los modelos y quedarnos solo con los minimales, con un algoritmo ingenuo (no se necesitaba hacer nada más), nos podría tomar tiempo cuadrático en el número de modelos, es decir (2^|Neg|)^2 = 2^(2|Neg|). El tiempo total es O(2^(2|Neg|)).

En análisis puede cambiar si se propone otra estrategia pero es importante que se considere el paso final que es el de revisar que el conjunto de modelos solo considere modelos minimales.



## Criterios de Puntaje:
1) Algoritmo especificado consiste en un pseudocódigo
2) Pseudocódigo es recursivo
3) Pseudocódigo utiliza algoritmo del enunciado
4) Argumenta que su algoritmo es correcto utilizando al menos un ejemplo sencillo
   1) En el peor de los casos es exponencial en el número de átomos que aparecen negados en el programa
   2) Justifica eficiencia considerando que el algoritmo del enunciado retorna modelos minimales
