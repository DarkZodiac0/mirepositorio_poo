

import math
import random

from nodo_iot import NodoIoT


def _validar_porcentaje(valor) -> int:

    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"La potencia debe ser numérica, se recibió {type(valor).__name__}")
    if math.isnan(valor) or not 0 <= valor <= 100:
        raise ValueError("La potencia PWM debe estar entre 0 y 100 %")
    return int(valor)


class NodoSensor(NodoIoT):
   
    def __init__(self, id_dispositivo: str, ip: str, ubicacion: str, magnitud: str,
                 unidad: str, rango_min: float, rango_max: float,
                 lectura_inicial: float, limite_alerta: float, variacion: float = 1.0) -> None:
        super().__init__(id_dispositivo, ip, ubicacion)  # reutiliza el constructor del padre
        self.magnitud = magnitud
        self.unidad = unidad
        self.__rango_min = float(rango_min)   # límites físicos reales del sensor
        self.__rango_max = float(rango_max)
        self.__variacion = abs(float(variacion))  # cambio máximo por lectura simulada
        self.lectura_actual = min(max(float(lectura_inicial), self.__rango_min), self.__rango_max)
        self.__limite_alerta = self.__rango_max
        self.set_limite_alerta(limite_alerta)  # el valor inicial también pasa por la validación

    def get_limite_alerta(self) -> float:
        return self.__limite_alerta

    def set_limite_alerta(self, valor: float) -> None:
        """Asigna el límite de alerta solo si es un número dentro del rango físico del sensor."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError(f"El límite debe ser numérico, se recibió {type(valor).__name__}")
        if math.isnan(valor) or not self.__rango_min <= valor <= self.__rango_max:
            raise ValueError(
                f"Límite fuera del rango físico del sensor "
                f"({self.__rango_min} a {self.__rango_max} {self.unidad})"
            )
        self.__limite_alerta = float(valor)

    def leer(self) -> float:
        """Simula una nueva lectura con una pequeña variación aleatoria."""
        nueva = self.lectura_actual + random.uniform(-self.__variacion, self.__variacion)
        self.lectura_actual = round(min(max(nueva, self.__rango_min), self.__rango_max), 2)
        return self.lectura_actual

    def enviar_telemetria(self) -> None:
        valor = self.leer()
        alerta = " | ALERTA: supera el límite" if valor > self.__limite_alerta else ""
        print(f"[{self.id_dispositivo}] {self.magnitud}: {valor} {self.unidad} "
              f"(límite {self.__limite_alerta}){alerta}")


class NodoActuador(NodoIoT):

    def __init__(self, id_dispositivo: str, ip: str, ubicacion: str, tipo: str) -> None:
        super().__init__(id_dispositivo, ip, ubicacion)
        self.tipo = tipo
        self.__estado_activo = False
        self.__potencia_pwm = 0

    def esta_activo(self) -> bool:
        return self.__estado_activo

    def get_potencia_pwm(self) -> int:
        return self.__potencia_pwm

    def encender(self, potencia: int = 100) -> None:
        potencia = _validar_porcentaje(potencia)
        self.__estado_activo = True
        self.__potencia_pwm = potencia
        print(f"[{self.id_dispositivo}] {self.tipo} encendido al {potencia} %")

    def apagar(self) -> None:
        self.__estado_activo = False
        self.__potencia_pwm = 0
        print(f"[{self.id_dispositivo}] {self.tipo} apagado")

    def set_potencia_pwm(self, valor: int) -> None:
        """Ajusta la potencia solo si el actuador está encendido y el valor es válido."""
        valor = _validar_porcentaje(valor)
        if not self.__estado_activo:
            raise RuntimeError("Encienda el actuador antes de ajustar la potencia")
        self.__potencia_pwm = valor

    def enviar_telemetria(self) -> None:
        estado = "ENCENDIDO" if self.__estado_activo else "APAGADO"
        print(f"[{self.id_dispositivo}] {self.tipo}: {estado} | PWM: {self.__potencia_pwm} %")
