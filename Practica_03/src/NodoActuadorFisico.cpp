#include "NodoActuadorFisico.h"

static const int FRECUENCIA_PWM  = 5000;  // Hz
static const int RESOLUCION_PWM  = 8;     // bits -> 0 a 255

int NodoActuadorFisico::_contadorCanales = 0;

NodoActuadorFisico::NodoActuadorFisico(String id, int pinSalida, bool usarPWM)
    : NodoIoT(id, pinSalida), _estadoActivo(false), _potencia(255),
      _usaPWM(usarPWM), _canalPWM(usarPWM ? _contadorCanales++ : -1) {}

void NodoActuadorFisico::iniciar() {
    pinMode(pin, OUTPUT);
    if (_usaPWM) {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
        ledcAttach(pin, FRECUENCIA_PWM, RESOLUCION_PWM);
#else
        ledcSetup(_canalPWM, FRECUENCIA_PWM, RESOLUCION_PWM);
        ledcAttachPin(pin, _canalPWM);
#endif
    }
    aplicarSalida();
    NodoIoT::iniciar();
}

void NodoActuadorFisico::aplicarSalida() {
    if (_usaPWM) {
        int duty = _estadoActivo ? _potencia : 0;
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
        ledcWrite(pin, duty);
#else
        ledcWrite(_canalPWM, duty);
#endif
    } else {
        digitalWrite(pin, _estadoActivo ? HIGH : LOW);
    }
}

void NodoActuadorFisico::ejecutarAccion() {
    aplicarSalida();
    Serial.print("[" + idDispositivo + "] ");
    Serial.print(_estadoActivo ? "ENCENDIDO" : "APAGADO");
    if (_usaPWM) {
        Serial.print(" | PWM: " + String(_estadoActivo ? _potencia : 0) + "/255");
    }
    Serial.println();
}

void NodoActuadorFisico::encender(uint8_t potencia) {
    _estadoActivo = true;
    _potencia = potencia;
}

void NodoActuadorFisico::apagar() { _estadoActivo = false; }

bool    NodoActuadorFisico::estaActivo() const { return _estadoActivo; }
uint8_t NodoActuadorFisico::getPotencia() const { return _potencia; }
