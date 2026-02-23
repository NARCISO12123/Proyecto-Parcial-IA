# Proyecto-parcial-IA

## Nombre:
    Narciso Beras 

## Matrícula:
    24-EISN-2-026 

## Proyecto:

    Propuesta de Juego

    La propuesta consiste en desarrollar un juego de supervivencia 
    tipo roguelike con vista superior, inspirado en mecánicas de juegos como Brotato, 
    Vampire Survivors entre otros juegos del genero,
    pero con un diseño propio y diferenciado.

    - Brotato GamePlay: https://youtube.com/shorts/KppVhxz7430?si=AGM0WoaQO3xLbgiA 

    - Vampire Survivors GamePlay: https://youtube.com/shorts/33IK8aVvQzs?si=d2zr33-g9j1xbA4I

    El jugador controla a un personaje que debe sobrevivir a oleadas de enemigos (zombies) dentro de un único 
    escenario que cambia en cada ronda. El objetivo principal es resistir hasta la ronda 10, donde aparece
    un jefe final. Al derrotarlo, se desbloquea un modo infinito como recompensa, 
    idea inspirada en la progresión utilizada en Balatro.

    Funcionamiento del Juego

    1- El jugador controla únicamente el movimiento del personaje.
    2- El disparo es automático y se dirige al enemigo más cercano.
    3- Los enemigos aparecen en oleadas progresivas.
    4- Al eliminar enemigos, el jugador obtiene oro.
    5- El juego termina cuando el jugador pierde toda su vida.

    En cada ronda, el mundo se genera nuevamente utilizando un generador de mapas,
    creando obstáculos en posiciones distintas. Esto hace que cada partida sea diferente
    y obliga tanto al jugador como a los enemigos a adaptarse al entorno.

    Enemigos

    Inicialmente, el juego contará con dos tipos de enemigos:

    1- Zombie básico

    Persigue al jugador.

    Ataca al estar a corta distancia.

    2- Zombie gordo explosivo

    Se mueve más lentamente.

    Persigue al jugador.

    Explota al estar en rango crítico, causando daño en área.

    Está planeado añadir más tipos de enemigos en el futuro para aumentar la variedad y dificultad.
    En la ronda 10 aparece un zombie jefe, que representa el enfrentamiento final del juego base.

    - Uso del Algoritmo A*

    Debido a que el mapa contiene obstáculos generados de forma procedural en cada ronda,
    los enemigos no pueden desplazarse directamente hacia el jugador.
    Para resolver esto, los enemigos utilizan el algoritmo A* para:

    1- Calcular la mejor ruta posible hacia el jugador.

    2- Evitar obstáculos del mapa.

    3- Adaptarse a la distribución cambiante del escenario.

    El algoritmo A* se basa en la implementación trabajada en los laboratorios de la asignatura y se utiliza exclusivamente para la navegación de los enemigos.

    Uso del Árbol de Comportamiento

    La toma de decisiones de los enemigos se implementa mediante un Árbol de Comportamiento

    El Árbol de Comportamiento permite que cada enemigo decida qué acción realizar según su estado y el del jugador.
    De forma general, el comportamiento sigue esta lógica:

    Si el jugador está en rango de ataque → Atacar.

    Si el jugador no está en rango → Perseguir usando A*.

    Si el enemigo es explosivo y está en rango crítico → Explotar.

    Si el enemigo es un jefe → Ejecutar comportamientos más complejos. (ideas en desarrollo)

    - Progresión y Mejoras

    El juego incluye una máquina de mejoras donde el jugador puede gastar oro para obtener mejoras aleatorias, como aumento de vida o velocidad. Esto añade un componente estratégico y de progresión al juego.

    Conclusión

    Aunque lo inspire un poco en los juegos que me gustas creo que marco ciertas diferencias claves, 
    Más ideas serán añadidas durante el desarrollo, pero este documento 
    presenta el planteamiento principal del proyecto, el cual podrá estar sujeto a mejoras y ajustes.