int currpos = 200;
int k, nm, wls;

void clockwise(void);
void anticlockwise(void);
void disable(void);

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
  while (Serial.available() > 0)   //verifica a porta serial 
  {             
    wls = Serial.parseInt();   //recebe um valor via serial em nm
    nm = wls - currpos;    
    if (nm > 0 && wls >0)    
    {                        
      for(k = 0; k < nm; k++) 
        {  
           clockwise();    
        }
    currpos = wls;      
    }               
    else if (nm < 0 && wls > 0)
    {                       
      for(k = 0; k < (abs(nm) + 5); k++) 
        {  
           anticlockwise();    
        }
      for (k = 0; k < 5; k++) 
        {  
           clockwise();    
        }
    currpos = wls;
    }  
    else if (wls = 0)
    {
      disable();
    }  
   }
}    
  
void clockwise()
{ 
  int i = 0;
  while(i <= 20)
  {
    digitalWrite(8, HIGH);    // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);    // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);    // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);    // Configura o pino 11 como LOW  
    delay(4);                   // Espera 4 ms
    digitalWrite(8, LOW);     // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);    // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH);   // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);    // Configura o pino 11 como LOW  
    delay(4);                   // Espera 4 ms
    digitalWrite(8, LOW);     // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);     // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH);   // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH);   // Configura o pino 11 como LOW
    delay(4);                   // Espera 4 ms 
    digitalWrite(8, HIGH);    // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);     // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);    // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH);   // Configura o pino 11 como LOW
    delay(4);                   // Espera 4 ms
    i = i + 1;
  }
}

void anticlockwise()
{
  int j = 0;
  while(j <= 20)
  {
    digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
    digitalWrite(10,LOW);  // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH); // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    digitalWrite(8, LOW);   // Configura o pino 8 como HIGH              
    digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
    digitalWrite(11, HIGH); // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    digitalWrite(8, LOW);   // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);  // Configura o pino 9 como LOW  
    digitalWrite(10, HIGH); // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);  // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms 
    digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
    digitalWrite(9, HIGH);  // Configura o pino 9 como LOW  
    digitalWrite(10, LOW);  // Configura o pino 10 como HIGH                
    digitalWrite(11, LOW);  // Configura o pino 11 como LOW
    delay(4);               // Espera 4 ms
    j = j + 1;
  }
}

void disable()
{
  digitalWrite(8, HIGH);  // Configura o pino 8 como HIGH              
  digitalWrite(9, LOW);   // Configura o pino 9 como LOW  
  digitalWrite(10, LOW);  // Configura o pino 10 como HIGH                
  digitalWrite(11, LOW); // Configura o pino 11 como LOW
}
