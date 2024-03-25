void clockwise(void);
void anticlockwise(void);

void setup() 
{ 
  Serial.begin(9600);  
  pinMode(8, OUTPUT); // Configura os pinos d8,  
  pinMode(9, OUTPUT); // d9, 
  pinMode(10, OUTPUT);// d10 e 
  pinMode(11, OUTPUT);// d11 como saídas
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
  digitalWrite(8, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(9, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(10, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW  
  delay(4);// Espera 4 ms
  digitalWrite(8, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(9, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW  
  delay(4);// Espera 4 ms
  digitalWrite(8, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW); // Configura o pino 9 como LOW  
  digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(11, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms 
  digitalWrite(8, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW); // Configura o pino 9 como LOW  
  digitalWrite(10, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(11, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
}

void anticlockwise()
{
  digitalWrite(8, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW); // Configura o pino 9 como LOW  
  digitalWrite(10, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(11, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
  digitalWrite(8, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW); // Configura o pino 9 como LOW  
  digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(11, HIGH); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
  digitalWrite(8, LOW); // Configura o pino 8 como HIGH              
  digitalWrite(9, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms 
  digitalWrite(8, HIGH); // Configura o pino 8 como HIGH              
  digitalWrite(9, HIGH); // Configura o pino 9 como LOW  
  digitalWrite(10, LOW); // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW
  delay(4);// Espera 4 ms
}

