import sys

from nodos_hijos import NodoActuador, NodoSensor

# --- Dispositivos de la red ---
sensor_temp = NodoSensor("TEMP-01", "192.168.1.10", "Sala de servidores",
                         "Temperatura", "°C", -40, 125, 24.5, 35.0, variacion=0.6)
actuador_ventilador = NodoActuador("VENT-01", "192.168.1.20", "Sala de servidores", "Ventilador")
sensor_luz = NodoSensor("LUZ-01", "192.168.1.11", "Sala de servidores",
                        "Luminosidad", "lx", 0, 100000, 350, 800, variacion=80)

sensores = [sensor_temp, sensor_luz]
actuadores = [actuador_ventilador]
red_iot = [sensor_temp, actuador_ventilador, sensor_luz]  # lista mixta

# Bucles polimórficos
def conectar_red() -> None:
    for dispositivo in red_iot:
        dispositivo.conectar()


def telemetria_red() -> None:
    for dispositivo in red_iot:
        dispositivo.enviar_telemetria()


# --- Utilidades de la HMI ---
def pedir_numero(mensaje: str, defecto=None) -> float:
    texto = input(mensaje).strip()
    if texto == "" and defecto is not None:
        return defecto
    try:
        return float(texto)
    except ValueError:
        raise ValueError("ingrese un número válido") from None

