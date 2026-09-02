# Project Prompts

This file saves all prompts and instructions given to Claude during project development.
Each entry is timestamped for reference.

---

## Prompt 1: Initial Project Specification (2026-09-01)

### Language: Spanish

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

---

## Prompt 2: Path Constraints & Documentation Reorganization (2026-09-01)

### Language: Spanish

ok, añade a tus notas que nunca escribiremos en ningun archivo del proyecto rutas locales de la maquina en la que estoy desarrollando, solamente rutas relativas dentro del propio proyecto.

Añade esto a tu claude.md y modifica los archivos que contengan rutas absolutas.

En el checklist mete en el archivo de claude.md todo lo que sean instrucciones, guias de estilo etc y deja solamente los aspectos tecnicos que hay que implementar. Mueve el fichero también a docs porque estos son nuestros requisitos. Llamalo requirements o algo similar. Luego implementaremos el resto. 

Guarda este prompt junto al primero en otro archivo llamado prompts. Cada prompt que te de guardalo en ese fichero (que tambien va en docs)

---

## Prompt 3: Implementation Phase & Core Library (2026-09-01)

### Language: Spanish

ok, procede con la implementacion. Iremos paso a paso de tal forma que pueda ir commiteando cada cosa por separado. 
Revisa el checklist porque veo algunos puntos del core project setup que ya han sido llevadoa cabo. El resto de proyectos ni si

### Intent

User approved starting the implementation phase. Emphasis on:
1. Step-by-step implementation with separate commits per phase
2. Verification of completed documentation phase items
3. Begin Phase 1: Core Library

---

## Prompt 4: Phase 1 Complete - Beginning Phase 2 (2026-09-01)

### Language: Spanish

ok, explicame un poco que has implementado. Veo un agent base que actua a modo de clase abstracta y exige al programador implementar los metodos de play e init. Porque tenemos el discover agents mezclado con esto en el archivo __init__.py?

Continuamos con el paso 2, example agents. Veo que no estas actualizando el archivo de prompts. Tienes que hacerlo para que los alumnos puedan ver como se ha ido contruyendo el proyuecto a base de IA. Ahora quiero que hagas los 3 ejemplos que pedí en el prompt inicial. A saber: Uno que juegue aleatorio, otro que replique las jugadas del contrincante y otro que no coopere soolo si recibe dos no-cooperaciones del contrincante.

### Intent

User requests:
1. Clarification on Phase 1 architecture (Agent base class, discover_agents function placement)
2. Update prompts.md with all prompts to show AI-driven development progression
3. Begin Phase 2: Create three example agents:
   - **random_agent** — random move strategy
   - **copycat_agent** — tit-for-tat (replicate opponent's last move)
   - **second_chance_agent** — forgive first defection, retaliate on second defection, then forgive again

---

## Intent & Summary

**Prompt 1** establishes the complete specification for an Iterated Prisoner's Dilemma tournament platform for student programming assignments.

**Prompt 2** adds path constraints and documentation reorganization, with requirement to save all prompts.

**Prompt 3** initiates implementation phase with step-by-step, committable approach.

**Prompt 4** requests Phase 1 clarification, prompt file updates, and Phase 2 agent implementation.

---

## Guidelines for Future Prompts

When adding new prompts to this file:
1. Include the timestamp (date)
2. Specify the language
3. Preserve the prompt verbatim
4. Add a brief "Intent" section describing what the user requested

This file serves as a historical record of project evolution and requirements changes, demonstrating how the project was built iteratively with AI assistance.
