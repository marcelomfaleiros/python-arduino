void clockwise(void);
void anticlockwise(void);

void setup() 
{ 
  Serial.begin(9600);  
  pinMode(4, OUTPUT); // Configura os pinos d4,  
  pinMode(5, OUTPUT); // d5, 
  pinMode(6, OUTPUT);// d6 e 
  pinMode(7, OUTPUT);// d7 como saídas
}

void loop() 
{   
  int inipos, currpos = 0;
  int i = 0;  
  while (Serial.available() > 0)    
  {
    int wls = Serial.parseInt();    
    while(i < wls)
    {
      if(wls > inipos)
      {
        anticlockwise();        
        Serial.println(i);
        i = i+1;
      }
      else
      {
        clockwise();        
        Serial.println(i);
        i = i+1; 
      }
    }                    
  }      
}

void clockwise()
{
  digitalWrite(4, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(5, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(6, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(7, LOW); // Configura o pino 11 como LOW  
  delay(4);// Espera 4 ms
  digitalWrite(4, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(5, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(6, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(7, LOW); // Configura o pino 11 como LOW  
  delay(4);// Espera 4 ms
  digitalWrite(4, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(5, LOW); // Configura o pino 9 como LOW  
  digitalWrite(6, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(7, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms 
  digitalWrite(4, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(5, LOW); // Configura o pino 9 como LOW  
  digitalWrite(6, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(7, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
}

void anticlockwise()
{
  digitalWrite(4, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(5, LOW); // Configura o pino 9 como LOW  
  digitalWrite(6, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(7, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
  digitalWrite(4, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(5, LOW); // Configura o pino 9 como LOW  
  digitalWrite(6, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(7, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
  digitalWrite(4, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(5, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(6, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(7, LOW); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms 
  digitalWrite(4, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(5, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(6, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(7, LOW); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
}
