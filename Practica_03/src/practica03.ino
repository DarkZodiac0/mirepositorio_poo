/*
  Práctica 3: Implementación física de nodos IoT heterogéneos (ESP32, C++)

  Conexiones:
    Sensor analógico (potenciómetro o LDR con divisor) -> GPIO 34 (ADC1)
    Actuador (LED con resistencia de 220 ohm)          -> GPIO 25
*/
#include "NodoIoT.h"
#include "NodoSensorFisico.h"
#include "NodoActuadorFisico.h"

const int N = 2;
NodoIoT* red[N];   // arreglo polimórfico de punteros a la superclase

void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println("=== Practica 3: red de nodos IoT en ESP32 ===");

    NodoSensorFisico*   sensor   = new NodoSensorFisico("SENS_LUZ", 34, 2500);
    NodoActuadorFisico* actuador = new NodoActuadorFisico("ACT_LED", 25, true);  // true = PWM
    sensor->vincularAlerta(actuador);

    red[0] = sensor;
    red[1] = actuador;

    for (int i = 0; i < N; i++) {
        red[i]->iniciar();
    }

    // Prueba del encapsulamiento: el setter rechaza valores fuera del rango del ADC
    Serial.println("--- Prueba del setter ---");
    sensor->setUmbralAlerta(5000);
    sensor->setUmbralAlerta(2500);
    Serial.println("-------------------------");
}

void loop() {
    for (int i = 0; i < N; i++) {
        red[i]->ejecutarAccion();   // polimorfismo: sin preguntar el tipo
    }
    Serial.println();
    delay(500);
}
