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
def elegir(dispositivos, titulo: str):
    print(f"\n{titulo}")
    for numero, dispositivo in enumerate(dispositivos, start=1):
        print(f"  {numero}. {dispositivo.id_dispositivo} ({dispositivo.ubicacion})")
    try:
        indice = int(input("Opción: ")) - 1
        if indice < 0:
            raise IndexError
        return dispositivos[indice]
    except (ValueError, IndexError):
        print("Selección no válida.")
        return None


def cambiar_limite() -> None:
    sensor = elegir(sensores, "Sensores disponibles:")
    if sensor is None:
        return
    try:
        nuevo = pedir_numero(f"Nuevo límite de alerta [{sensor.get_limite_alerta()}]: ")
        sensor.set_limite_alerta(nuevo)
        print(f"Límite actualizado a {sensor.get_limite_alerta()} {sensor.unidad}")
    except (TypeError, ValueError) as error:
        print(f"Rechazado: {error}")


def controlar_actuador() -> None:
    actuador = elegir(actuadores, "Actuadores disponibles:")
    if actuador is None:
        return
    print("  1. Encender   2. Apagar   3. Ajustar potencia PWM")
    accion = input("Acción: ").strip()
    try:
        if accion == "1":
            actuador.encender(pedir_numero("Potencia PWM (0-100) [100]: ", 100))
        elif accion == "2":
            actuador.apagar()
        elif accion == "3":
            actuador.set_potencia_pwm(pedir_numero("Nueva potencia PWM (0-100): "))
            print(f"Potencia ajustada a {actuador.get_potencia_pwm()} %")
        else:
            print("Acción no válida.")
    except (TypeError, ValueError, RuntimeError) as error:
        print(f"Rechazado: {error}")


MENU = {
    "1": ("Conectar todos los nodos", conectar_red),
    "2": ("Enviar telemetría de toda la red", telemetria_red),
    "3": ("Cambiar límite de alerta de un sensor", cambiar_limite),
    "4": ("Controlar un actuador", controlar_actuador),
}


def hmi() -> None:
    while True:
        print("\n===== HMI - RED IoT =====")
        for clave, (texto, _) in MENU.items():
            print(f"{clave}. {texto}")
        print("0. Salir")
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            print("Fin de la simulación.")
            break
        entrada = MENU.get(opcion)
        if entrada:
            entrada[1]()
        else:
            print("Opción no válida.")


def demo() -> None:
    print("=== DEMO: red IoT ===\n--- Conexión ---")
    conectar_red()
    print("\n--- Telemetría inicial ---")
    telemetria_red()
    print("\n--- Se enciende el ventilador al 75 % ---")
    actuador_ventilador.encender(75)
    telemetria_red()
    print("\n--- Pruebas del setter (encapsulamiento) ---")
    for valor in (30.0, 500.0, "alto"):
        try:
            sensor_temp.set_limite_alerta(valor)
            print(f"Límite aceptado: {sensor_temp.get_limite_alerta()} °C")
        except (TypeError, ValueError) as error:
            print(f"Rechazado ({valor!r}): {error}")
    try:
        actuador_ventilador.set_potencia_pwm(150)
    except ValueError as error:
        print(f"Rechazado (150): {error}")
    print("\n--- Se apaga el ventilador y se repite la telemetría ---")
    actuador_ventilador.apagar()
    telemetria_red()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        hmi()
