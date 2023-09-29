# Chat de calculadora de insulina

Para la diabetes tipo 1, un tratamiento comun consiste en hacer conteo de carbohidratos, luego inyectarse insulina segun una tabla para compensar la subida de glicemia.

Con esta herramienta se puede describir la alimentacion con lenguaje natural, y se retorna un resumen de cada uno de los alimentos, sus carbohidratos correspondientes, y la cantidad de insulina necesaria para este.

# Ejemplo

## Input:
```
Tengo glicemia de 120. Voy a comer 3 naranjas, 1 barra de chocolate quaker y un huevo.

```
## Output:
```
Lo que vas a comer es: 3 fruta de Naranjas, 45 carbohidratos, 
 1 unidades de 100 gramos de Barra de chocolate quaker, 67 carbohidratos, 
 1 grande de Huevo, 0 carbohidratos, 
 El total de carbohidratos es de: 112.
 Tienes 120 de glicemia, asi que vas a necesitar 9 unidades de insulina
```
# Funcionamiento

- Se recibe el prompt
- Se usa la API de ChatGPT para estructurarlo en una tabla
- Se ordena la informacion en un diccionario
- En base a este se busca cada uno de los alimentos haciendo web-scraping en fatsecret
- Se calculan los carbohidratos segun las medidas dadas
- Se crea un texto de salida con toda la informacion