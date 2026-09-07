#!/usr/bin/env python3
"""
EE: Programación Orientada a Objetos (UV)
Ejemplo Integrador v8: Panel HMI con más objetos
"""

import os
import random

# Lista global para simular un registrador de eventos (Event Logger)
historial_eventos = []

def registrar_evento(mensaje: str):
    """Agrega un evento al historial y mantiene solo los últimos 5 para que no desplace la pantalla."""
    historial_eventos.append(mensaje)
    if len(historial_eventos) > 5:
        historial_eventos.pop(0)

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo (cls para Windows, clear para Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ======================================================================
# CLASE ACTUADOR
# ======================================================================
class Actuador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.rango_operacion_min = 0.0
        self.rango_operacion_max = 100.0
        self.estado = False
        self.punto_operacion = 0.0

    def encender(self):
        self.estado = True
        registrar_evento(f"[+] {self.nombre} -> ENCENDIDO (ON)")

    def apagar(self):
        self.estado = False
        registrar_evento(f"[-] {self.nombre} -> APAGADO (OFF)")

    def ajustar(self, valor: float):
        if self.rango_operacion_min <= valor <= self.rango_operacion_max:
            self.punto_operacion = valor
            registrar_evento(f"[⚙] {self.nombre} -> Punto de operación ajustado al {self.punto_operacion:.1f}%")
        else:
            registrar_evento(f"[⚠️ ERROR] {self.nombre} -> Valor {valor}% fuera de rango (0% - 100%).")

    def info(self) -> str:
        estado_str = "ON" if self.estado else "OFF"
        return f"{self.nombre:<20} | Estado: {estado_str:<3} | Punto Op: {self.punto_operacion:>5.1f}% | Rango: [0.0% - 100.0%]"


# ======================================================================
# CLASE SENSOR
# ======================================================================
class Sensor:
    def __init__(self, nombre: str, variable_fisica: str, rango_min: float, rango_max: float, sensibilidad: float, decimales_medicion: int, unidad: str):
        self.nombre = nombre
        self.variable_fisica = variable_fisica
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.sensibilidad = sensibilidad
        self.decimales_medicion = decimales_medicion
        self.unidad = unidad

    def leer_valor_actual(self) -> float:
        valor_simulado = random.uniform(self.rango_min, self.rango_max)
        valor_redondeado = round(valor_simulado, self.decimales_medicion)
        lectura_str = f"{valor_redondeado:.{self.decimales_medicion}f} {self.unidad}"
        registrar_evento(f"[📊 LECTURA] {self.nombre}: {lectura_str} (Var: {self.variable_fisica})")
        return valor_redondeado

    def info(self) -> str:
        return f"{self.nombre:<20} | Var: {self.variable_fisica:<18} | Rango: [{self.rango_min:>4.1f} - {self.rango_max:>5.1f}] {self.unidad:<5} | Sensibilidad: {self.sensibilidad} | Dec: {self.decimales_medicion}"


# ======================================================================
# INTERFAZ HMI
# ======================================================================
def mostrar_interfaz_hmi(actuadores, sensores):
    print("=" * 85)
    print("                PANEL DE CONTROL INDUSTRIAL HMI (ESTÁTICO)")
    print("=" * 85)

    print(" [ACTUADORES]")
    for key, act in actuadores.items():
        print(f"   ► [{key:<9}] {act.info()}")
    print("-" * 85)

    print(" [SENSORES]")
    for key, sen in sensores.items():
        print(f"   ► [{key:<9}] {sen.info()}")
    print("=" * 85)

    print(" [REGISTRO DE EVENTOS EN VIVO]")
    if not historial_eventos:
        print("   (Sin actividad reciente)")
    else:
        for ev in historial_eventos:
            print(f"   {ev}")
    print("=" * 85)

    print(" COMANDOS DISPONIBLES:")
    print("   • encender <actuador>       (Ej: encender bomba, encender ventilador)")
    print("   • apagar <actuador>         (Ej: apagar valvula, apagar ventilador)")
    print("   • ajustar <actuador> <val>  (Ej: ajustar bomba 75.5)")
    print("   • leer <sensor>             (Ej: leer caudal, leer manometro, leer termometro)")
    print("   • terminar                  (Finaliza la simulación)")
    print("=" * 85)


# ======================================================================
# BUCLE PRINCIPAL
# ======================================================================
def main():
    # Actuadores
    bomba = Actuador("Bomba de Agua")
    valvula = Actuador("Válvula de Control")
    ventilador = Actuador("Ventilador Industrial")

    # Sensores
    medidor_caudal = Sensor("Medidor de Caudal", "Flujo Volumétrico", 0.0, 120.0, 0.01, 2, "L/min")
    manometro = Sensor("Manómetro Digital", "Presión Hidráulica", 0.0, 10.0, 0.001, 3, "Bar")
    termometro = Sensor("Termómetro Digital", "Temperatura Ambiente", -10.0, 50.0, 0.1, 1, "°C")

    actuadores = {"bomba": bomba, "valvula": valvula, "ventilador": ventilador}
    sensores = {"caudal": medidor_caudal, "manometro": manometro, "termometro": termometro}

    while True:
        limpiar_pantalla()
        mostrar_interfaz_hmi(actuadores, sensores)

        try:
            entrada = input("Ingrese comando >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n[+] Programa terminado.")
            break

        if not entrada:
            continue
        if entrada.lower() == "terminar":
            print("\n[+] Cerrando sistema de control... Programa finalizado con éxito.")
            break

        partes = entrada.split()
        comando = partes[0].lower()

        if comando == "encender":
            if len(partes) < 2:
                registrar_evento("[⚠️ ERROR] Especifica el actuador.")
                continue
            target = partes[1].lower()
            if target in actuadores:
                actuadores[target].encender()
            else:
                registrar_evento(f"[⚠️ ERROR] Actuador '{target}' no existe.")

        elif comando == "apagar":
            if len(partes) < 2:
                registrar_evento("[⚠️ ERROR] Especifica el actuador.")
                continue
            target = partes[1].lower()
            if target in actuadores:
                actuadores[target].apagar()
            else:
                registrar_evento(f"[⚠️ ERROR] Actuador '{target}' no existe.")

        elif comando == "ajustar":
            if len(partes) < 3:
                registrar_evento("[⚠️ ERROR] Faltan parámetros.")
                continue
            target = partes[1].lower()
            try:
                valor = float(partes[2])
                if target in actuadores:
                    actuadores[target].ajustar(valor)
                else:
                    registrar_evento(f"[⚠️ ERROR] Actuador '{target}' no existe.")
            except ValueError:
                registrar_evento("[⚠️ ERROR] El valor debe ser numérico.")

        elif comando == "leer":
            if len(partes) < 2:
                registrar_evento("[⚠️ ERROR] Especifica el sensor.")
                continue
            target = partes[1].lower()
            if target in sensores:
                sensores[target].leer_valor_actual()
            else:
                registrar_evento(f"[⚠️ ERROR] Sensor '{target}' no existe.")

        else:
            registrar_evento(f"[⚠️ ERROR] Comando '{comando}' no reconocido.")


if __name__ == "__main__":
    main()

