#ifndef NODO_ACTUADOR_FISICO_H
#define NODO_ACTUADOR_FISICO_H

#include "NodoIoT.h"

// Actuador conectado a una salida digital o PWM (LED, relé, zumbador, ventilador).
class NodoActuadorFisico : public NodoIoT {
private:
    bool    _estadoActivo;
    uint8_t _potencia;          // 0 a 255 (ciclo de trabajo PWM de 8 bits)
    bool    _usaPWM;
    int     _canalPWM;
    static int _contadorCanales;

    void aplicarSalida();       // escribe el estado real en el pin

public:
    NodoActuadorFisico(String id, int pinSalida, bool usarPWM = false);

    void iniciar() override;
    void ejecutarAccion() override;

    void    encender(uint8_t potencia = 255);
    void    apagar();
    bool    estaActivo() const;
    uint8_t getPotencia() const;
};

#endif
