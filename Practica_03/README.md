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
| Código en C++ modular | Aun no se inicia |
| Arreglo de punteros | Aun no se inicia |
| Prueba en hardware real | Aun no se inicia |
| Reporte de evidencias PDF | Aun no se inicia |
| Estructura de GitHub | Completada ✅ |

*Estados: Aun no se inicia, En proceso, Completada ✅.*

---

### ***Resumen de avance***

La estructura del repositorio ya está lista. Falta programar el código en C++, armar el circuito y hacer el reporte.

[Actualizar este resumen después de cada sesión de trabajo.]

### **Tareas a seguir**

* ### ***Primera parte: Código en C++ modular***
En esta parte se programan las clases en C++ para el ESP32: una clase base `NodoIoT` y dos clases hijas, una para el sensor y otra para el actuador. Se usa herencia, atributos privados (encapsulamiento) y métodos virtuales (polimorfismo). El código se divide en archivos de cabecera (`.h`) y de código (`.cpp`).

| ***Código*** | ***Función*** | ***Avance*** |
|:---|:---|---:|
| NodoIoT (`.h` y `.cpp`) | Clase padre con lo que comparten todos los nodos | Pendiente |
| NodoSensorFisico (`.h` y `.cpp`) | Nodo hijo que lee el sensor analógico y valida su umbral | Pendiente |
| NodoActuadorFisico (`.h` y `.cpp`) | Nodo hijo que controla la salida del actuador | Pendiente |
| practica03 (`.ino`) | Programa principal que crea los nodos y ejecuta el ciclo | Pendiente |

[Anotar aquí los problemas que tuvimos .]


* ### ***Parte 2: Arreglo de punteros***
Una vez hechas las clases, se crea un arreglo de punteros a la clase base (`NodoIoT* red[N]`) que guarda el sensor y el actuador. El `loop()` recorre el arreglo y llama a `ejecutarAccion()` de cada nodo, sin preguntar de qué tipo es.

**Avance:** Pendiente




* ### ***Parte 3: Prueba en hardware real***
Se arma el circuito con el ESP32, un sensor de luz (LDR) y un LED, y se comprueba que el LED responde cuando cambia la luz. Las lecturas se observan en el Monitor Serie a 115200 baudios.

**Avance:** Pendiente




* ### ***Parte 4: Reporte de evidencias PDF***
Se integra en el reporte el esquemático de conexiones, las fotografías del circuito, las capturas del Monitor Serie y el enlace al video demostrativo (máximo 3 minutos).

**Avance:** Pendiente

---

### ***Conclusión***

