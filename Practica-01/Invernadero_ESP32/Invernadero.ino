// ==========================================
// CONFIGURACIÓN DE PINES
// ==========================================
const int PIN_LDR       = 34; // Entrada analógica ADC1 (LDR + Resistencia de 6.8 kΩ)
const int PIN_LED       = 19; // Salida PWM al Gate del MOSFET IRLZ44N (LED 1W)

// Pines para el Puente H (Motor)
const int PIN_MOTOR_PWM = 18; // Señal PWM al driver del motor (IN1 o ENA)
const int PIN_MOTOR_DIR = 5;  // Dirección del motor (IN2)

// Pines para el Encoder
const int PIN_ENC_A     = 32; // Canal A del Encoder (Cable Amarillo)
const int PIN_ENC_B     = 33; // Canal B del Encoder (Cable Verde)

// ==========================================
// PARÁMETROS PWM ESP32
// ==========================================
const int FREC_PWM   = 5000; // Frecuencia PWM de 5 kHz
const int RESOLUCION = 8;    // Resolución de 8 bits (Valores de 0 a 255)

// ==========================================
// VARIABLES DEL ENCODER
// ==========================================
volatile long contadorPulsos = 0;

// Subrutina de Interrupción para lectura de cuadratura del encoder
void IRAM_ATTR encoderISR() {
  if (digitalRead(PIN_ENC_B) == HIGH) {
    contadorPulsos++;
  } else {
    contadorPulsos--;
  }
}

void setup() {
  Serial.begin(115200);

  // 1. Configuración de dirección del motor
  pinMode(PIN_MOTOR_DIR, OUTPUT);
  digitalWrite(PIN_MOTOR_DIR, LOW); // Sentido de giro fijo

  // 2. Configuración PWM con la nueva API del ESP32 (Core v3.x+)
  // Sintaxis: ledcAttach(pin, frecuencia, resolucion)
  ledcAttach(PIN_MOTOR_PWM, FREC_PWM, RESOLUCION);
  ledcAttach(PIN_LED, FREC_PWM, RESOLUCION);

  // 3. Configuración del Encoder con resistencias Pull-Up internas
  pinMode(PIN_ENC_A, INPUT_PULLUP);
  pinMode(PIN_ENC_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), encoderISR, RISING);

  // 4. Configuración de entrada LDR
  pinMode(PIN_LDR, INPUT);

  Serial.println("--- Sistema ESP32 Inicializado Correctamente ---");
}

void loop() {
  // Lectura del valor analógico del divisor de voltaje LDR + 6.8 kΩ (0 a 4095)
  int valorLDR = analogRead(PIN_LDR);

  // Límites calibrados para la resistencia de 6.8 kΩ (Ajustar según tu entorno de luz)
  int minLDR = 300;   // Oscuridad / Sombra
  int maxLDR = 3700;  // Luz directa

  // Restringir lectura dentro de los límites de seguridad
  int ldrAjustada = constrain(valorLDR, minLDR, maxLDR);

  // Mapear de la resolución ADC (12-bit) al control PWM (8-bit: 0 a 255)
  int valorPWM = map(ldrAjustada, minLDR, maxLDR, 0, 255);

  // Aplicar señal PWM proporcional al Motor y al LED de 1W con la nueva función
  // Sintaxis: ledcWrite(pin, valor_pwm)
  ledcWrite(PIN_MOTOR_PWM, valorPWM);
  ledcWrite(PIN_LED, valorPWM);

  // Monitoreo Serie para Diagnóstico
  Serial.print("LDR Directo: ");
  Serial.print(valorLDR);
  Serial.print(" | Salida PWM: ");
  Serial.print(valorPWM);
  Serial.print(" | Pulsos Encoder: ");
  Serial.println(contadorPulsos);

  delay(50); // Muestreo cada 50 ms
}
