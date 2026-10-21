class NodoIoT:
    """Clase padre de todos los dispositivos de la red IoT."""

    def __init__(self, id_dispositivo: str, ip: str, ubicacion: str) -> None:
        self.id_dispositivo = id_dispositivo
        self.ip = ip
        self.ubicacion = ubicacion
        self.conectado = False

    def conectar(self) -> bool:
        """Simula la conexión del nood a la red."""
        self.conectado = True
        print(f"[{self.id_dispositivo}] Conectado a {self.ip} - {self.ubicacion}")
        return self.conectado

    def enviar_telemetria(self) -> None:
        """Compotraamiento base; cada subclase lo sobrescribe con su propia información."""
        estado = "conectado" if self.conectado else "desconectado"
        print(f"[{self.id_dispositivo}] Nodo genérico ({estado}) - {self.ip}")
