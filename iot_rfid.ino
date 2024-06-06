#include <WiFi.h>
#include <MFRC522.h>
#include <SPI.h>
const char* ssid1 = "Drica";
const char* password1 = "dricaeguti";
const char* ssid2 = "DVD";
const char* password2 = "12345678";
#define SS_PIN 21
#define RST_PIN 22
#define pinVerde     12
#define pinVermelho  32

#define SIZE_BUFFER     18
#define MAX_SIZE_BLOCK  16
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;
MFRC522 mfrc522(SS_PIN, RST_PIN); 

void setup() {
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus

   mfrc522.PCD_Init(); 
  // Mensagens iniciais no serial monitor
  Serial.println("Aproxime o seu cartao do leitor...");
  Serial.println();

  Serial.begin(9600);
  connectToWiFi();
}

void loop() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Seleciona um dos cartoes
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }

  //chama o menu e recupera a opção desejada
  int opcao = menu();
  
  if(opcao == 0) 
    leituraDados();
  else if(opcao == 1) 
    gravarDados();
  else {
    Serial.println(F("Opção Incorreta!"));
    return;
  }
  // instrui o PICC quando no estado ACTIVE a ir para um estado de "parada"
  mfrc522.PICC_HaltA(); 
  // "stop" a encriptação do PCD, deve ser chamado após a comunicação com autenticação, caso contrário novas comunicações não poderão ser iniciadas
  mfrc522.PCD_StopCrypto1();  
}

//faz a leitura dos dados do cartão/tag
void leituraDados()
{
  //imprime os detalhes tecnicos do cartão/tag
  mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid)); 

  //Prepara a chave - todas as chaves estão configuradas para FFFFFFFFFFFFh (Padrão de fábrica).
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;

  //buffer para colocar os dados ligos
  byte buffer[SIZE_BUFFER] = {0};

  //bloco que faremos a operação
  byte bloco = 1;
  byte tamanho = SIZE_BUFFER;


  //faz a autenticação do bloco que vamos operar
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, bloco, &key, &(mfrc522.uid)); //line 834 of MFRC522.cpp file
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    digitalWrite(pinVermelho, HIGH);
    delay(1000);
    digitalWrite(pinVermelho, LOW);
    return;
  }

  //faz a leitura dos dados do bloco
  status = mfrc522.MIFARE_Read(bloco, buffer, &tamanho);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    digitalWrite(pinVermelho, HIGH);
    delay(1000);
    digitalWrite(pinVermelho, LOW);
    return;
  }
  else{
      digitalWrite(pinVerde, HIGH);
      delay(1000);
      digitalWrite(pinVerde, LOW);
  }




void connectToWiFi() {
  int attempts = 0;
  
  while (attempts < 10) {
    Serial.println("Conectando a uma rede...");
    if (connectToNetwork(ssid1, password1) || connectToNetwork(ssid2, password2)) {
      Serial.println("Conectado!");
      break;
    } else {
      attempts++;
      Serial.println("A conexão falhou. Reconectando...");
      delay(1000);
    }
  }

  if (attempts >= 10) {
    Serial.println("Não foi possível se conectar ao Wifi. Por favor, cheque sua rede e senha.");
  }
}

bool connectToNetwork(const char* ssid, const char* password) {
  WiFi.begin(ssid, password);
  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED && attempts < 5) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    return true;
  } else {
    return false;
  }
}