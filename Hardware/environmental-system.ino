const int pinoTrig = 2;
const int pinoEcho = 3;

// Sensor Infravermelho (Refletância)
const int pinoIR = A0;

// Buzzer
const int pinoBuzzer = 4;

// LED RGB
const int pinoVermelho = 5;
const int pinoVerde = 6;
const int pinoAzul = 7;

// ====== VARIÁVEIS GLOBAIS ======
long duracao;
int distancia;
int valorIR;

// ====== CONFIGURAÇÃO INICIAL ======
void setup() {
  // Inicializa a comunicação serial (para enviar dados ao computador)
  Serial.begin(9600);
  
  // Configura os pinos
  pinMode(pinoTrig, OUTPUT);
  pinMode(pinoEcho, INPUT);
  pinMode(pinoBuzzer, OUTPUT);
  pinMode(pinoVermelho, OUTPUT);
  pinMode(pinoVerde, OUTPUT);
  pinMode(pinoAzul, OUTPUT);
  
  // Inicialmente, desliga o buzzer e define a cor do LED
  digitalWrite(pinoBuzzer, LOW);
  setColor(0, 0, 255); // Azul (Estado Normal)

  // Cabeçalho do CSV na Serial (importante para a análise!)
  Serial.println("Tempo(ms),Distancia(cm),Luminosidade(IR),Estado"); 
}

// ====== LOOP PRINCIPAL ======
void loop() {
  // 1. LÊ OS SENSORES
  distancia = lerSensorUltrassonico();
  valorIR = analogRead(pinoIR);
  
  // 2. TOMA AÇÃO COM BASE NOS DADOS (Atuadores)
  // Define a cor do LED e ativa buzzer com base nas leituras
  if (distancia > 0 && distancia < 10) {
    // Objeto MUITO perto -> Alerta Vermelho + Buzzer
    setColor(255, 0, 0); // Vermelho
    tone(pinoBuzzer, 1000, 100); // Toca um tom de 1kHz por 100ms
  } else if (distancia >= 10 && distancia < 30) {
    // Objeto em distância "ideal" -> Verde
    setColor(0, 255, 0); // Verde
    noTone(pinoBuzzer);
  } else {
    // Nada detectado ou muito longe -> Azul
    setColor(0, 0, 255); // Azul
    noTone(pinoBuzzer);
  }

  // 3. ENVIA OS DADOS PARA O COMPUTADOR (Ciência de Dados!)
  Serial.print(millis());  // Timestamp em milissegundos
  Serial.print(",");
  Serial.print(distancia);
  Serial.print(",");
  Serial.print(valorIR);
  Serial.print(",");
  
  // Adiciona um rótulo de estado para facilitar a análise
  if (distancia < 10) {
    Serial.println("ALERTA_PROXIMO");
  } else if (distancia < 30) {
    Serial.println("OBJETO_DETECTADO");
  } else {
    Serial.println("NORMAL");
  }

  // Pequena pausa para não sobrecarregar a serial
  delay(500);
}

// ====== FUNÇÃO PARA LER O SENSOR ULTRASSÔNICO ======
int lerSensorUltrassonico() {
  digitalWrite(pinoTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinoTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinoTrig, LOW);
  
  duracao = pulseIn(pinoEcho, HIGH);
  // Calcula a distância em centímetros (velocidade do som / 2)
  distancia = duracao * 0.034 / 2;
  
  // Retorna a distância. Retorna 999 se fora do alcance (erro).
  if (distancia > 300 || distancia <= 0) {
    return 999;
  }
  return distancia;
}

// ====== FUNÇÃO PARA CONTROLAR A COR DO LED RGB ======
void setColor(int vermelho, int verde, int azul) {
  // Lembre-se: Cátodo Comum -> valor HIGH desliga o LED, LOW liga.
  // Por isso, usamos '255 - valor' para inverter.
  analogWrite(pinoVermelho, 255 - vermelho);
  analogWrite(pinoVerde, 255 - verde);
  analogWrite(pinoAzul, 255 - azul);
}
