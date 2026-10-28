#include "NodoIoT.h"

NodoIoT::NodoIoT(String id, int pinHardware)
    : idDispositivo(id), pin(pinHardware), conectado(false) {}

void NodoIoT::iniciar() {
    conectado = true;
    Serial.println("[" + idDispositivo + "] iniciado en el pin " + String(pin));
}

String NodoIoT::getId() const { return idDispositivo; }
int    NodoIoT::getPin() const { return pin; }
bool   NodoIoT::estaConectado() const { return conectado; }
