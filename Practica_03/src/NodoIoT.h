#ifndef NODO_IOT_H
#define NODO_IOT_H

#include <Arduino.h>

// Superclase base: lo que comparten todos los dispositivos conectados al ESP32.
class NodoIoT {
protected:
    String idDispositivo;
    int    pin;
    bool   conectado;

public:
    NodoIoT(String id, int pinHardware);
    virtual ~NodoIoT() {}

    // Cada subclase configura su pin (pinMode) y luego llama a NodoIoT::iniciar().
    virtual void iniciar();

    // Método polimórfico puro: cada tipo de nodo define su acción.
    virtual void ejecutarAccion() = 0;

    String getId() const;
    int    getPin() const;
    bool   estaConectado() const;
};

#endif
