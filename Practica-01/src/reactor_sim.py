#!/usr/bin/env python3
import os
import platform
import time

def limpiar_pantalla()

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class SimuladorProcesoIndustrial:
    def __init__(self):
        # Variables de proceso y rangos de operación
        self.temperatura = 25.0       # 0.0 a 150.0 °C
        self.presion = 1.0            # 0.0 a 15.0 Bar
        self.bomba_pct = 0.0          # 0.0 a 100.0 % (Modulación Proporcional PWM)
        self.valvula = 0              # 0 (Cerrada) o 1 (Abierta) (Digital ON/OFF)
        
        # Modos: MANUAL, AUTOMATICO, PRUEBAS
        self.modo = "MANUAL"
        self.interlock_activo = False

    def verificar_interlocks(self):
        """
        [!WARNING] Interlocks de Seguridad (Prioridad de Ejecución):
        Si Temperatura > 85.0 °C o Presión > 12.0 Bar:
        Enfriamiento al 100% y Apertura Total de la Válvula de Alivio.
        """
        if self.temperatura > 85.0 or self.presion > 12.0:
            self.interlock_activo = True
            self.bomba_pct = 100.0
            self.valvula = 1
            return True
        self.interlock_activo = False
        return False

    def actualizar_dinamica(self):
        """
        Lógica del Modo Automático:
        Delta T = (+1.5 °C) - (0.05 °C * % OperaciónBomba)
        """
        if self.modo == "AUTOMATICO" and not self.interlock_activo:
            delta_t = 1.5 - (0.05 * self.bomba_pct)
            self.temperatura = max(0.0, min(150.0, self.temperatura + delta_t))
            
            # Algoritmo de estabilidad dinámica en lazo cerrado
            if self.temperatura > 65.0:
                self.bomba_pct = min(100.0, self.bomba_pct + 10.0)
            elif self.temperatura < 45.0:
                self.bomba_pct = max(0.0, self.bomba_pct - 10.0)
            
            # Válvula en régimen normal de automático permanece cerrada
            self.valvula = 0
            
            # Presión vinculada a la curva térmica
            self.presion = max(0.0, min(15.0, (self.temperatura / 150.0) * 10.0))

        elif self.interlock_activo:
            # Respuesta rápida durante el interlock
            self.temperatura = max(25.0, self.temperatura - 3.5)
            self.presion = max(1.0, self.presion - 1.2)

    def renderizar_pantalla(self, mensaje=""):
        limpiar_pantalla()
        print("=================================================================")
        print("         SIMULADOR DE HARDWARE INDUSTRIAL (SISTEMA HMI)          ")
        print("=================================================================")
        print(f" Modo de Operación : [{self.modo}]")
        print(f" Sensor Temperatura: {self.temperatura:6.2f} °C   [Rango: 0.0 - 150.0 °C]")
        print(f" Sensor Presión    : {self.presion:6.2f} Bar  [Rango: 0.0 -  15.0 Bar]")
        print(f" Bomba Enfriamiento: {self.bomba_pct:6.1f} %    [Modulación Proporcional PWM]")
        print(f" Válvula de Alivio : {'ABIERTA (1)' if self.valvula == 1 else 'CERRADA (0)'}   [Control Digital ON/OFF]")
        print("-----------------------------------------------------------------")
        
        if self.interlock_activo:
            print(" [!WARNING!] INTERLOCK DE SEGURIDAD ACTIVADO (PRIORIDAD ALTA)")
            print(" Condición crítica detectada: Temp > 85.0 °C o Presión > 12.0 Bar")
            print(" Acción automática        : Bomba al 100% | Válvula ABIERTA")
            print("-----------------------------------------------------------------")
            
        if mensaje:
            print(f" >> {mensaje}")
            print("-----------------------------------------------------------------")
            
        print(" Comandos HMI disponibles:")
        print("   - Lectura        : 'leer caudal' | 'leer manometro'")
        print("   - Modos          : 'modo manual' | 'modo auto' | 'modo pruebas'")
        print("   - Actuadores (M) : 'set bomba <0-100>' | 'set valvula <0/1>'")
        print("   - Variables (M)  : 'set temp <0-150>'  | 'set pres <0-15>'")
        print("   - Salir          : 'salir'")
        print("=================================================================")

def main():
    sim = SimuladorProcesoIndustrial()
    mensaje = "Sistema inicializado. Listo para recibir instrucciones."
    
    while True:
        sim.verificar_interlocks()
        sim.actualizar_dinamica()
        sim.renderizar_pantalla(mensaje)
        
        try:
            cmd = input("HMI Consola >> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nSimulación finalizada.")
            break

        mensaje = ""
        partes = cmd.split()
        
        # 1. Comandos obligatorios de lectura
        if cmd == "leer caudal":
            caudal_calculado = (sim.bomba_pct / 100.0) * 50.0
            mensaje = f"[CAUDALÍMETRO]: {caudal_calculado:.2f} L/min (Bomba operando al {sim.bomba_pct:.1f}%)"
            
        elif cmd == "leer manometro":
            mensaje = f"[MANÓMETRO]: {sim.presion:.2f} Bar"

        # 2. Selección de Modos de Operación
        elif cmd == "modo manual":
            sim.modo = "MANUAL"
            mensaje = "Modo cambiado a MANUAL. Interacción directa por consola habilitada."
            
        elif cmd == "modo auto":
            sim.modo = "AUTOMATICO"
            mensaje = "Modo cambiado a AUTOMÁTICO. Algoritmo de estabilidad dinámica activo."
            
        elif cmd == "modo pruebas":
            sim.modo = "PRUEBAS"
            # Inyección de fallos para validación de límites operativos
            sim.temperatura = 92.0
            sim.presion = 13.5
            sim.verificar_interlocks()
            mensaje = "MODO DE PRUEBAS: Fallo inyectado (Temp = 92.0 °C, Presión = 13.5 Bar)."

        # 3. Control de Actuadores en Modo Manual
        elif len(partes) == 3 and partes[0] == "set" and partes[1] == "bomba":
            if sim.interlock_activo:
                mensaje = "COMANDO RECHAZADO: Interlock de seguridad activo."
            elif sim.modo != "MANUAL":
                mensaje = "COMANDO RECHAZADO: Solo permitido en Modo Manual."
            else:
                try:
                    val = float(partes[2])
                    if 0.0 <= val <= 100.0:
                        sim.bomba_pct = val
                        mensaje = f"Bomba de enfriamiento ajustada a {sim.bomba_pct:.1f}%"
                    else:
                        mensaje = "Error: El porcentaje de la bomba debe estar entre 0 y 100 %."
                except ValueError:
                    mensaje = "Error de sintaxis. Uso: set bomba <0-100>"

        elif len(partes) == 3 and partes[0] == "set" and partes[1] == "valvula":
            if sim.interlock_activo:
                mensaje = "COMANDO RECHAZADO: Interlock de seguridad activo."
            elif sim.modo != "MANUAL":
                mensaje = "COMANDO RECHAZADO: Solo permitido en Modo Manual."
            else:
                if partes[2] in ("0", "1"):
                    sim.valvula = int(partes[2])
                    mensaje = f"Válvula de alivio configurada en estado {sim.valvula}"
                else:
                    mensaje = "Error: Estado de válvula inválido. Use 0 (Cerrada) o 1 (Abierta)."

        # 4. Ajuste manual de variables simuladas
        elif len(partes) == 3 and partes[0] == "set" and partes[1] == "temp":
            try:
                sim.temperatura = float(partes[2])
                mensaje = f"Temperatura modificada a {sim.temperatura:.1f} °C"
            except ValueError:
                mensaje = "Error de sintaxis. Uso: set temp <0-150>"

        elif len(partes) == 3 and partes[0] == "set" and partes[1] == "pres":
            try:
                sim.presion = float(partes[2])
                mensaje = f"Presión modificada a {sim.presion:.1f} Bar"
            except ValueError:
                mensaje = "Error de sintaxis. Uso: set pres <0-15>"

        elif cmd == "salir":
            print("\nSimulación cerrada.")
            break
        else:
            mensaje = f"Comando '{cmd}' no reconocido. Revise la lista de comandos disponibles."

if __name__ == "__main__":
    main()
