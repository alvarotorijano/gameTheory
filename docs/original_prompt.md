# Prompt Original - Dilema del Prisionero (Español)

*Este archivo preserva el prompt original del usuario en español, tal como fue proporcionado.*

---

Ok, antes de ponernos a desarrollar te cuento que vamos a hacer y como quiero proceder.

Todo el código en inglés.
Claude no puede hacer operaciones de escritura en git.
Cada función tiene que estar documentada con docstrings.
EL proyecto es una práctica sencilla del dilema del prisionero.

Cada alumno escribirá el código y luego los pondremos a competir entre ellos, por tanto tiene que haber un código de ejemplo que les permita escribir su primer código y correrlo contra un adversario ficticio. Este adversario originalmente hará movimientos random. El código de ejemplo es un agente que simplemente copia los movimientos de su contrario.

Necesitamos también un mecanismo para poder recopiar todos los forks de este proyecto y luego ponerlos a correr unos contra otros. Habrá partido de ida y de vuelta. En el partido de IDA el jugador A empieza primero, en el partido de vuelta el jugador B empieza primero.

Una vez terminados todos los partidos hay que analizar cuantos puntos ha recibido cada uno.

El juego transcurre de la siguiente forma: Si los dos jugadores cooperan ambos reciben 3 puntos, cantidad que quiero que sea configurable en un archivo JSON. Si ninguno coopera entonces ambos reciben un punto. Si uno coopera pero el otro no el que cooperó no recibe nada, pero el que no lo hizo recibe 5 puntos.

Quiero que cada agente con cada estrategia sea un archivo por separado, de tal forma que cuando los alumnos se descarguen el proyecto haya una carpeta de agentes donde puedan agregar el suyo.

En el caso de ejemplo haremos 3 agentes: uno que haga movimientos al azar, otro que copie los movimientos del contrario y otro que si recibe una no cooperación entonces vuelva a cooperar, pero que si recibe una no cooperación por segunda vez entonces deje de cooperar en el siguiente turno pero vuelva a cooperar en el siguiente, como si solo recordara dos jugadas atras.

A mayores en el proyecto tiene que haber otro script que nos permita hacer correr un agente contra otro y nos muestre el resultado de la ida y de la vuelta y el promedio total de los dos partidos para ver quien es el que saca mas puntos.

Luego quiero otro script que corra todos los agentes uno contra otro que haya en la carpeta agentes y genere un archivo .csv con los puntos que sacó cada agente en cada partido, la cantidad de veces que cooperó después de haber recibido una no cooperación, la cantidad de veces que no cooperó habiendo recibido una no cooperación, la cantidad de veces que cooperó habiendo recibido una cooperación y la cantidad de veces que no cooperó habiendo recibido una cooperación.

También tienes que marcar como true o false si su primer movimiento es la cooperación o la no cooperación. También tienes que sacar cuantas cooperaciones y no cooperaciones hay por cada jugador y por cada partido.

La cantidad de rondas se le pueden indicar al agente o no (pasarle un null).

Cada agente tiene que tener un archivo readme.md que explique su árbol de decisión con un diagrama de mermaid, por tanto cada agente debe estar en una subcarpeta dentro de la carpeta agentes. Cada script debe estar en una carpeta dentro de otra llamada utils con su respectivo README.md.

En el repositorio principal tiene que haber otro archivo README.md que explique para que sirve cada script, como se utiliza el juego, una guía rápida de programación, una guía rápida de instalación si es necesario. Si hay que instalar librerías extra entonces usa un pyenv y explica como inicializar el entorno e instalar las dependencias. Puedes usar un archivo de dependencias como se hace en python típicamente.

Crea otra carpeta docs con toda la documentación de las cosas que vamos a hacer.
Crea también un archivo claude.md con las reglas o restricciones que he impuesto.
Guarda este prompt.

Crea un plan de implementación porque luego vas a escribir tu todo este código y herramientas.

Primero siempre haremos un plan de implementación, luego empezaremos a implementar.

Todo esto correrá en local, no hace falta ninguna herramienta externa.

Haz otra herramienta extra a la que le pueda pasar la lista de repositorios donde los alumnos han subido sus agentes y haga un clone y meta a cada agente nuevo que cada alumno haya hecho. Los alumnos podrían escribir más de un agente y eso tienes que tenerlo en cuenta.

Simplemente lo que hará esa herramienta es coger a los agentes que no sean los de ejemplo y meterlos en la carpeta agentes del repo en el que se ejecute el script porque es posible que algún alumno no sepa utilizar git y simplemente me entregue el archivo de código.

Ahora haz primero la documentación y el plan de implementación, y cuando te lo diga empezaremos con toda la implementación que la harás autonomamente.

Luego hazme también un set de pruebas para y alguna herramienta que las ejecute todas para que podamos ver que cada funcionalidad funciona según lo esperado y para que podamos hacer cambios y comprobar que nada se rompe. Esto va en una carpeta test.

Adelante con la planificación del proyecto y la documentación.
