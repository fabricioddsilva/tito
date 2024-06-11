#include <ArduinoJson.h>
#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>
#include <Adafruit_NeoPixel.h>
#include <Ultrasonic.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define LED_PIN 27
#define LED_COUNT 8
#define NWIFIS 8

// Estrutura para armazenar as credenciais da rede WiFi
struct WiFiCredentials {
  const char* ssid;
  const char* password;
};

char *redeAtual;


struct WiFiCredentials wifiNetworks[]={
  {"Cimento", "comercimento5544"},
  {"NETMAIS_TULIBIA_979133843", "adm32668634"},
  {"iPhone de Arnott","arbbbe11"},
  {"SENAC-Mesh","09080706"},
  {"Vivo-Internet-E532", "6EFC366C"},
  {"iPhone de Arnott","arbbbe11"},
  {"SENAC-MESH","09080706"},
  {"DVD","12345678"}

};

int numNetworks = NWIFIS;

// Número de redes WiFi para tentar conectar

bool sistema = false;

Adafruit_NeoPixel leds(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
Ultrasonic ultrasonic(13,12);

float distancia = 0;

MFRC522DriverPinSimple ss_pin(21); // Configurable, see typical pin layout above.

MFRC522DriverSPI driver{ss_pin}; // Create SPI driver.
MFRC522 mfrc522{driver};  // Create MFRC522 instance.

void setup() {
  Serial.begin(9600);
  mfrc522.PCD_Init();
   for(int i = 0; i < numNetworks; ++i) {
      conectaWifi(i); // tenta conectar em uma das redes disponiveis
      if (WiFi.status() == WL_CONNECTED){
        led_bar(255,0,255,100);
        delay(1500);
        sistema = true;
        break;
      }

      if (WiFi.status() != WL_CONNECTED )
        delay(100);
  }
  leds.begin();
	
}

void loop() {
do {
  
  distancia = ultrasonic.read();
    if (distancia <= 70) {
      led_bar(0,0,255,0);
      	// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( !mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards.
	if ( !mfrc522.PICC_ReadCardSerial()) {
		return;
	}

  
    
	//Serial.print("UID da Tag: ");
  String conteudo = "";
  byte letra;
  for (byte i = 0; i < mfrc522.uid.size; i++){
   // Serial.println(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
   //   Serial.println(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
    led_bar(255,255,0,0);
  }
  Serial.println();

  Serial.print("Mensagem: ");
  conteudo.toUpperCase();

  autenticar(conteudo.substring(1));
  // String url = "drakonor.pythonanywhere.com/auth";
  // doc["uuid"] = conteudo.substring(1);
  // String output;
  // serializeJson(doc, output);
  // Serial.println(output);
  // autenticar(url, output);

  delay(1000);
  
    }
    else{
      led_bar(0,0,0,0);
    }

  } while (sistema == true);

 
}

void led_bar(int red, int green, int blue, int delay_time) {
  for (int i = 0; i < LED_COUNT; i++) {
    leds.setPixelColor(i, leds.Color(red, green, blue));
    leds.show();
    delay(delay_time);
  }
   // Atualiza a barra de LED
}


void conectaWifi(int index)
{
// Loop através de cada rede WiF
    Serial.print("Conectando-se a ");
    Serial.println(wifiNetworks[index].ssid);

    // Tentativa de conexão com a rede WiFi
    WiFi.begin(wifiNetworks[index].ssid, wifiNetworks[index].password);

    int attempt = 0;
    // Aguarda a conexão WiFi ser estabelecida
    while (WiFi.status() != WL_CONNECTED && attempt < 5) {
      delay(500);
      Serial.print(".");
      attempt++;
    }

    // Verifica se a conexão WiFi foi bem-sucedida
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println();
      Serial.println("Conexão bem-sucedida!");
      Serial.print("Endereço IP: ");
      Serial.println(WiFi.localIP());
      // Sai do loop se a conexão for bem-sucedida
    } else {
      Serial.println();
      Serial.println("Falha ao conectar-se!");
    }
  
}

void autenticar(String uuid) {
  if (WiFi.status() == WL_CONNECTED) { // Verifica se está conectado ao WiFi
    HTTPClient http;
    String url = "https://drakonor.pythonanywhere.com/auth";

    http.begin(url); // Inicia a conexão HTTP
    http.addHeader("Content-Type", "application/json"); // Adiciona cabeçalho de conteúdo JSON

    StaticJsonDocument<200> doc;
    doc["uuid"] = uuid;

    String cartao;
    serializeJson(doc, cartao);

    int httpResponseCode = http.POST(cartao); // Envia a requisição POST com o payload

    if (httpResponseCode > 0) {
      String response = http.getString(); // Obtém a resposta da requisição
      Serial.println(httpResponseCode); // Código de resposta HTTP
      Serial.println(response);// Resposta da API
      if (response == "Autenticado com Sucesso"){
          Serial.println("Seja Bem Vindo!! Fabrício");
          led_bar(0,255,0,0);
          delay(1500); 
      }
      else if (response == "Cartão não encontrado"){
          Serial.println("Tag não identificada...");
          led_bar(255,0,0,0);
          delay(1500);
      }
     
    } else {
       Serial.print("Erro na requisição: ");
       Serial.println(httpResponseCode);
    }

    http.end(); // Finaliza a conexão HTTP
  } else {
    Serial.println("WiFi Desconectado");
  }
}

