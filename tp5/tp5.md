Ejercicio: **PROGRAMAS DE RADIO**

**Esquema de BD**

PROGRAMAS DE RADIO<radio, año, programa, conductor, gerente, frecuencia\_radio> con las restricciones:

1. Una radio se transmite por una única frecuencia (frecuencia\_radio) en un año determinado, y puede cambiarla en años diferentes.
1. Cada radio tiene un único gerente por año, pero el mismo gerente puede repetirse en la misma radio en diferentes años. Y la misma persona puede ser gerente de diferentes radios durante el mismo año.
1. Un mismo programa puede transmitirse por varias radios y en diferentes años.
1. Un programa transmitido en una radio en un año determinado tiene un solo conductor

**Paso 1: Determinar las Dependencias Funcionales (DFs)**

radio, año -> frecuencia\_radio: Cada radio se transmite en una única frecuencia en un año determinado, lo cual implica que la frecuencia depende de la combinación de radio y año.

radio, año -> gerente: Cada radio tiene un gerente único por año, por lo que el gerente depende de la combinación de radio y año.

radio, año, programa -> conductor: Un programa transmitido en una radio en un año específico tiene un único conductor, por lo tanto, el conductor depende de la combinación de radio, año y programa.

**Paso 2: Determinar las Claves Candidatas**

Para determinar las claves candidatas, buscamos un conjunto de atributos que identifiquen de forma única cada registro en la tabla PROGRAMA.

\1) radio, año, programa: Esta combinación de atributos es suficiente para identificar de

manera única cada registro en la tabla PROGRAMA, ya que:

- radio identifica la emisora.
- año identifica el año de transmisión.
- programa identifica de forma única el programa transmitido en una radio y año específicos.

Así, la clave candidata es:

- (radio, año, programa)

**Paso 3: Diseño en Tercera Forma Normal (3FN)**

Para llevar el esquema a Tercera Forma Normal (3FN), se deben eliminar las dependencias transitivas y asegurar que cada atributo no clave dependa únicamente de la clave primaria completa. Esto implica dividir la tabla PROGRAMA en varias tablas relacionadas para reducir la redundancia y asegurar la integridad de los datos.

Para lograrlo, dividimos la tabla PROGRAMA en tres tablas: Radio, Programa, y Transmision. Este diseño elimina dependencias transitivas y asegura que cada atributo no clave dependa únicamente de la clave primaria completa.

El nuevo diseño en 3FN sería el siguiente:

1) Tabla Transmision
   1. radio (Clave foránea que referencia a Radio)
   1. año
   1. programa (Clave foránea que referencia a Programa)
   1. conductor
   1. Clave primaria compuesta: (radio, año, programa)
1) Tabla Radio
   1. radio (Clave primaria)
   1. frecuencia\_radio (frecuencia en un año específico)
   1. año
   1. gerente
   1. Clave primaria compuesta: (radio, año)
1) Tabla Programa
- programa (Clave primaria)

Este proceso de normalización ayuda a reducir la redundancia y a mantener la consistencia de los datos en la base de datos. Cada tabla contiene solo la información relevante y depende completamente de su clave primaria, cumpliendo con los requisitos de la Tercera Forma Normal.

**Paso 4: Justificación de las Llaves Primarias:**

1. Tabla Transmision

Clave primaria: (radio, año, programa)

Justificación: La combinación (radio, año, programa) es la clave primaria en Transmision porque:

- Cada programa transmitido en una radio específica en un año específico tiene un único conductor, según las restricciones del enunciado.
- radio representa la emisora en la que se transmite el programa.
- año indica el año de la transmisión, y dado que una misma emisora puede cambiar sus frecuencias en años distintos, el año es crucial para la unicidad.
- programa representa el programa específico transmitido en esa radio y año.

Los tres atributos garantizan la unicidad de cada transmisión, asegurando que cada fila en Transmision sea única y no tenga duplicados, ya que no puede haber dos registros que tengan el mismo radio, año, y programa simultáneamente.

2. Tabla Radio

Clave primaria: (radio, año)

Justificación: La combinación (radio, año) es la clave primaria en la tabla Radio porque:

- Cada radio tiene una única frecuencia y un único gerente en un año dado, según las restricciones proporcionadas.
- radio representa la emisora y año permite distinguir las diferentes configuraciones de frecuencia y gerente que pueden cambiar de un año a otro.

La combinación de radio y año asegura que no haya duplicados en la tabla Radio, ya que en un mismo año no puede haber dos registros con la misma emisora (radio) y los mismos valores en el resto de los campos. La combinación es suficiente para identificar de forma única cada registro.

3. Tabla Programa

Clave primaria: programa

Justificación: programa es la clave primaria en la tabla Programa porque:

- Cada programa tiene un nombre único, independientemente de la radio o del año en el que se transmita, según el enunciado.

Esto garantiza la unicidad de cada programa en la tabla Programa, ya que no habrá duplicados de programa y permite identificar cada registro de manera única. Esta clave es la única necesaria para identificar un programa en cualquier otra tabla.
