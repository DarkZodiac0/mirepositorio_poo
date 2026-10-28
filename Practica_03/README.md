### ***Bitácora de práctica 3***

**Encargados:**

| Integrantes | Nombre de usuario |
|:---|:---:|
| Pérez Montero Axel Arturo | @DarkZodiac0 |
| Bremont Limon Isaac Gabriel | @Isaaclimon14 |

---

### ***Checklist***

| Tarea | Estado |
|:---|:---:|
| Código en C++ modular | Completado (27/10/2026)|
| Arreglo de punteros | Completado (27/10/2026)|
| Prueba en hardware real | Completado (28//10/2026)|
| Reporte de evidencias PDF | Aun no se inicia |
| Estructura de GitHub | Completada ✅ |

*Estados: Aun no se inicia, En proceso, Completada ✅.*

---

### ***Resumen de avance***

* Empezamos del día 20 de octubre empezamos  con los códigos que iban a complementar al código original (20/10/2026). 
* Día 22 de octubre, finalizamos con la mayoría de los códigos usando algunas herencias y empezando a trabajar el código principal (22/10/2026). 
* Día 27 de octubre, finalizamos la parte del código principal y  comenzamos con el armado del circuito físico
* Día 28 de octubre, Finalizamos con el armado y se probo el circuito probando su funcionalidad, comprobando que función todo de manera correcta (28/10/2026).
(perdón si no habíamos subido nada, es que anduvimos algo ocupados 👌🏻)
### **Tareas a seguir**

* ### ***Primera parte: Código en C++ modular***
En esta parte se programan las clases en C++ para el ESP32: una clase base `NodoIoT` y dos clases hijas, una para el sensor y otra para el actuador. Se usa herencia, atributos privados (encapsulamiento) y métodos virtuales (polimorfismo). El código se divide en archivos de cabecera (`.h`) y de código (`.cpp`).

| ***Código*** | ***Función*** | ***Avance*** |
|:---|:---|---:|
| NodoIoT (`.h` y `.cpp`) | Clase padre con lo que comparten todos los nodos | Pendiente |
| NodoSensorFisico (`.h` y `.cpp`) | Nodo hijo que lee el sensor analógico y valida su umbral | Pendiente |
| NodoActuadorFisico (`.h` y `.cpp`) | Nodo hijo que controla la salida del actuador | Pendiente |
| practica03 (`.ino`) | Programa principal que crea los nodos y ejecuta el ciclo | Pendiente |


* ### ***Parte 2: Arreglo de punteros***
Una vez hechas las clases, se crea un arreglo de punteros a la clase base (`NodoIoT* red[N]`) que guarda el sensor y el actuador. El `loop()` recorre el arreglo y llama a `ejecutarAccion()` de cada nodo, sin preguntar de qué tipo es.

**Avance:** Terminado (27/10/2026)




* ### ***Parte 3: Prueba en hardware real***
Se arma el circuito con el ESP32, un sensor de luz (LDR) y un LED, y se comprueba que el LED responde cuando cambia la luz. Las lecturas se observan en el Monitor Serie a 115200 baudios.

**Avance:** Terminado (28/10/2026)




* ### ***Parte 4: Reporte de evidencias PDF***
Se integra en el reporte el esquemático de conexiones, las fotografías del circuito, las capturas del Monitor Serie y el enlace al video demostrativo (máximo 3 minutos).

**Avance:** Pendiente

### ***Problemas y soluciones***
|Problema | solucion |
|:---|:---:|
|Tuvimos un problema al momento de correr el programa en Arduino IDE nos marcaba un error de directorios ya que no encontraba los archivos de herencia| Juntamos todos los programas en una sola carpeta donde el IDE detectara los archivos|
|Otro problema que tuvimos fue con la ESP32 ya que no recibía el código y decía que tenia un problema de conexión| Resulta que problema era de los drivers de la placa por lo que tuvimos que actualizar los controladores | 

---

### ***Conclusión***
En conclusión, la funcionalidad usar herencias y punteros para esta practica ha sido bastante practica ya que evitamos usar otra funciones si no que solo pasamos de unas a otras, tambien el uso de herencias como se ha dicho, son funciones bastantes practicas con respecto a algunas características.
