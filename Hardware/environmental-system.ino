const int pinoAgua = 2;

// Tilt Switch (Sensor de Inclinação)
const int pinoTilt = 3;

// Buzzer
const int pinoBuzzer = 8;

// LED RGB
const int pinoVermelho = 5;
const int pinoVerde = 6;
const int pinoAzul = 7;

// Sensor Ultrassônico (Opcional)
const int pinoTrig = 9;
const int pinoEcho = 10;

// ====== VARIÁVEIS GLOBAIS ======
bool estadoAgua = false;
bool estadoTilt = false;
bool ultimoEstadoAgua = false;
bool ultimoEstadoTilt = false;

unsigned long ultimoEventoAgua = 0;
unsigned long ultimoEventoTilt = 0;
const unsigned long tempoDebounce = 200; // ms para evitar bouncing

int nivelAgua = 0; // Para uso com ultrassônico

// ====== CONFIGURAÇÃO INICIAL ======
void setup() {
  // Inicializa comunicação serial
  Serial.begin(9600);
  
  // Configura os pinos
  pinMode(pinoAgua, INPUT);
  pinMode(pinoTilt, INPUT_PULLUP); // Usa pull-up interno para o tilt
  pinMode(pinoBuzzer, OUTPUT);
  pinMode(pinoVermelho, OUTPUT);
  pinMode(pinoVerde, OUTPUT);
  pinMode(pinoAzul, OUTPUT);
  
  pinMode(pinoTrig, OUTPUT);
  pinMode(pinoEcho, INPUT);
  
  // Estado inicial
  digitalWrite(pinoBuzzer, LOW);
  setColor(0, 255, 0); // Verde = Sistema OK
  
  // Cabeçalho do CSV
  Serial.println("Timestamp,Evento,Detalhes");
  Serial.println("SISTEMA_INICIADO,-,-");
}

// ====== LOOP PRINCIPAL ======
void loop() {
  unsigned long tempoAtual = millis();
  
  // 1. LÊ OS SENSORES PRINCIPAIS (Com debounce)
  estadoAgua = digitalRead(pinoAgua);
  estadoTilt = digitalRead(pinoTilt);
  
  // 2. VERIFICA EVENTO DE VAZAMENTO
  if (estadoAgua != ultimoEstadoAgua) {
    if (tempoAtual - ultimoEventoAgua > tempoDebounce) {
      if (estadoAgua == HIGH) {
        // Água detectada!
        registrarEvento("VAZAMENTO_DETECTADO", "CRITICO");
        setColor(255, 0, 0); // Vermelho
        tone(pinoBuzzer, 800, 2000); // Alarme longo
      } else {
        // Água saiu
        registrarEvento("VAZAMENTO_NORMALIZADO", "INFO");
        setColor(0, 0, 255); // Azul (Atenção)
      }
      ultimoEventoAgua = tempoAtual;
    }
    ultimoEstadoAgua = estadoAgua;
  }
  
  // 3. VERIFICA EVENTO DE MOVIMENTO
  if (estadoTilt != ultimoEstadoTilt) {
    if (tempoAtual - ultimoEventoTilt > tempoDebounce) {
      if (estadoTilt == LOW) { // Lembrando: pull-up, LOW = ativado
        registrarEvento("MOVIMENTO_DETECTADO", "ATENCAO");
        setColor(255, 165, 0); // Laranja
        tone(pinoBuzzer, 500, 500); // Alarme curto
      } else {
        registrarEvento("MOVIMENTO_NORMALIZADO", "INFO");
        setColor(0, 255, 0); // Verde (Voltou ao normal)
      }
      ultimoEventoTilt = tempoAtual;
    }
    ultimoEstadoTilt = estadoTilt;
  }
  
  // 4. MONITORAMENTO CONTÍNUO COM ULTRASSÔNICO (Opcional)
  if (tempoAtual % 5000 == 0) { // A cada 5 segundos
    int distancia = lerSensorUltrassonico();
    if (distancia < 100 && distancia > 0) { // Se houver recipiente
      nivelAgua = 100 - distancia; // Exemplo: converter para "nível %"
      Serial.print(millis());
      Serial.print(",NIVEL_AGUA,");
      Serial.println(nivelAgua);
    }
  }
  
  // 5. RESETA ALARME SONORO APÓS ALGUM TEMPO
  if (tempoAtual % 10000 == 0) { // A cada 10 segundos
    noTone(pinoBuzzer);
    // Volta para cor normal se não há eventos críticos
    if (!estadoAgua && estadoTilt) {
      setColor(0, 255, 0); // Verde
    }
  }
  
  delay(100); // Pequena pausa para estabilidade
}

// ====== FUNÇÃO PARA REGISTRAR EVENTOS ======
void registrarEvento(String tipo, String severidade) {
  Serial.print(millis());
  Serial.print(",");
  Serial.print(tipo);
  Serial.print(",");
  Serial.println(severidade);
}

// ====== FUNÇÃO DO SENSOR ULTRASSÔNICO ======
int lerSensorUltrassonico() {
  digitalWrite(pinoTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinoTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinoTrig, LOW);
  
  long duracao = pulseIn(pinoEcho, HIGH);
  return duracao * 0.034 / 2;
}

// ====== FUNÇÃO PARA CONTROLAR LED RGB ======
void setColor(int vermelho, int verde, int azul) {
  analogWrite(pinoVermelho, 255 - vermelho);
  analogWrite(pinoVerde, 255 - verde);
  analogWrite(pinoAzul, 255 - azul);
}
