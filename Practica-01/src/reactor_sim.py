import machine
import time


#1. CONFIGURACIÓN DE PINES (GPIO / ADC)

# Entradas Analógicas 
adc_temp = machine.ADC(26)      # Canal ADC 
adc_press = machine.ADC(27)     # Canal ADC

# Salidas de Actuadores
pwm_bomba = machine.PWM(machine.Pin(15))  # Bomba de enfriamiento (Modulación 0 - 100%)
pwm_bomba.freq(1000)
