#include "NodoSensorFisico.h"
#include "NodoActuadorFisico.h"

NodoSensorFisico::NodoSensorFisico(String id, int pinADC, int umbral)
    : NodoIoT(id, pinADC), _umbralAlerta(ADC_MAX / 2), _ultimaLectura(0),
      _actuadorAlerta(nullptr) {
    setUmbralAlerta(umbral);   // el valor inicial también pasa por la validación
}

void NodoSensorFisico::iniciar() {
    pinMode(pin, INPUT);
    NodoIoT::iniciar();
}

bool NodoSensorFisico::setUmbralAlerta(int umbral) {
    if (umbral < 0 || umbral > ADC_MAX) {
        Serial.println("[" + idDispositivo + "] Umbral " + String(umbral) +
                       " rechazado: debe estar entre 0 y " + String(ADC_MAX));
        return false;
    }
    _umbralAlerta = umbral;
    return true;
}

void NodoSensorFisico::ejecutarAccion() {
    _ultimaLectura = analogRead(pin);
    bool alerta = _ultimaLectura > _umbralAlerta;

    Serial.print("[" + idDispositivo + "] ADC = " + String(_ultimaLectura) +
                 " (umbral " + String(_umbralAlerta) + ")");
    if (alerta) Serial.print(" -> ALERTA");
    Serial.println();

    if (_actuadorAlerta != nullptr) {
        if (alerta) {
            // Más lectura por encima del umbral = más potencia (80 a 255)
            _actuadorAlerta->encender((uint8_t) map(_ultimaLectura, _umbralAlerta, ADC_MAX, 80, 255));
        } else {
            _actuadorAlerta->apagar();
        }
    }
}

int NodoSensorFisico::getUmbralAlerta() const { return _umbralAlerta; }
int NodoSensorFisico::getUltimaLectura() const { return _ultimaLectura; }
void NodoSensorFisico::vincularAlerta(NodoActuadorFisico* actuador) { _actuadorAlerta = actuador; }
