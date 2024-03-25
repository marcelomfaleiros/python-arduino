// Programa : Sensor de temperatura DHT22 e Teste escrita cartao SD
// Autor : Arduino e Cia
/* The circuit:
 * analog sensors on analog ins 0, 1, and 2
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 51
 ** MISO - pin 50
 ** CLK - pin 52
 ** CS - pin 53
*/ 
#include <DHT.h>
#include <LiquidCrystal.h>
#include <SPI.h>
#include <SD.h>
#include <DS1307.h>

#define DHTPIN 7                    // Pino conectado ao pino de dados do sensor
#define DHTTYPE DHT22               // Sensor DHT 22  (AM2302)

//Modulo RTC DS1307 ligado as portas A4 e A5 do Arduino 
DS1307 rtc(A4, A5);

File dataFile;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);        // Pinos do display

DHT dht(DHTPIN, DHTTYPE);                     // Definicoes do sensor : pino, tipo

byte grau[8] ={ B00001100,                    // Array simbolo grau
                B00010010, 
                B00010010, 
                B00001100, 
                B00000000, 
                B00000000, 
                B00000000, 
                B00000000,}; 

String dataString ="";  
String stringh ="";
String stringt ="";
String d ="";
String hora ="";
String dows ="";

void setup() 
{  
  lcd.begin(20, 4);                       // Inicializa o display
  lcd.clear();  
  lcd.createChar(0, grau);                    // Cria o caracter customizado com o simbolo do grau
  lcd.setCursor(0,0);                       // Informacoes iniciais no display
  lcd.print("Temp. : ");
  lcd.setCursor(13,0); 
  lcd.write(byte(0));                        //Mostra o simbolo do grau
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Umid. : ");
  lcd.setCursor(14,1);
  lcd.print("%");
  lcd.setCursor(0,2);
  lcd.print("Data : ");
  lcd.setCursor(0,3);
  lcd.print("Hora : ");

  rtc.halt(false);                        // aciona o relogio

  rtc.setDOW(MONDAY);                     //Define o dia da semana
  rtc.setTime(15, 05, 0);                 //Define o horario
  rtc.setDate(8, 10, 2018);               //Define o dia, mes e ano
   
  //Definicoes do pino SQW/Out
  rtc.setSQWRate(SQW_RATE_1);
  rtc.enableSQW(true);
    
  Serial.begin(9600); 
  Serial.println("Aguardando dados...");  
  pinMode(53, OUTPUT);  
  
  dht.begin();                                // Inicializa o sensor DHT
  if (!SD.begin(53)) 
  {
      Serial.println("Falha ao acessar o cartao !");    
      return;
  }
  Serial.println("Cartao iniciado corretamente !");  
}

void loop() 
{ 
  d = rtc.getDateStr(FORMAT_SHORT);
  hora = rtc.getTimeStr();    
  dows = rtc.getDOWStr(FORMAT_SHORT);  
  float h = dht.readHumidity();           // Leitura da umidade  
  float t = dht.readTemperature();        // Leitura da temperatura (Celsius)    
  stringh = String(h);
  stringt = String(t);
  dataString = (stringt+","+stringh+","+d+","+hora);
  if (isnan(h) || isnan(t))               // Verifica se o sensor esta respondendo
  {
    Serial.println("Falha ao ler dados do sensor DHT !!!");
    return;
  }  

  dataFile = SD.open("arquivo.txt", FILE_WRITE);  
  if (dataFile)                                     // Grava os dados no arquivo
  {
    dataFile.println(dataString);     
    dataFile.close();
  }  
  else 
  {    
    Serial.println("Erro ao abrir arquivo.txt !");  // Mensagem de erro caso ocorra algum problema na abertura do arquivo
  } 
  Serial.print("Hora : ");
  Serial.print(hora);
  Serial.print(" ");
  Serial.print("Data : ");
  Serial.print(d);
  Serial.print(" ");
  Serial.print(dows);
  Serial.print(" ");
  Serial.print("T = ");
  Serial.print(t);                                  // Mostra a temperatura no serial monitor e no display
  Serial.print(" ");
  Serial.print("H = ");
  Serial.println(h);
  
  lcd.setCursor(8,0);
  lcd.print(t);                       
  lcd.setCursor(8,1);
  lcd.print(h);                                     // Mostra a umidade no serial monitor e no display
  lcd.setCursor(8,2);
  lcd.print(d); 
  lcd.setCursor(8,3);
  lcd.print(hora); 
  delay(60000);                                     // Aguarda 2 segundos entre as medicoes  
}

