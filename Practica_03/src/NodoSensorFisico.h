#ifndef NODO_SENSOR_FISICO_H
#define NODO_SENSOR_FISICO_H

#include "NodoIoT.h"

class NodoActuadorFisico;   // declaración adelantada

// Sensor analógico (LDR, LM35, potenciómetro) conectado a un pin ADC del ESP32.
class NodoSensorFisico : public NodoIoT {
private:
    int _umbralAlerta;                    // en cuentas del ADC (0 a 4095)
    int _ultimaLectura;
    NodoActuadorFisico* _actuadorAlerta;  // actuador que reacciona a la alerta

public:
    static const int ADC_MAX = 4095;      // ADC de 12 bits del ESP32

    NodoSensorFisico(String id, int pinADC, int umbral = 2048);

    void iniciar() override;
    void ejecutarAccion() override;

    bool setUmbralAlerta(int umbral);     // valida el rango; devuelve false si lo rechaza
    int  getUmbralAlerta() const;
    int  getUltimaLectura() const;
    void vincularAlerta(NodoActuadorFisico* actuador);
};

#endif
