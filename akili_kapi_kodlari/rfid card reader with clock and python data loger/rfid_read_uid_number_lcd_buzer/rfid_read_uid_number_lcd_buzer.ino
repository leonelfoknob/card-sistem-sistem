#include <SPI.h> // SPI
#include <MFRC522.h> // RFID
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

#define SS_PIN 10
#define RST_PIN 9

//led and buzer pin
int green_led = 3;
int blue_led = 4;
int buzer = 2;
    
// Déclaration 
MFRC522 rfid(SS_PIN, RST_PIN); 

// Tableau contentent l'ID
byte nuidPICC[4];
int UID_int[4];
String UID_char[4];

void setup() 
{ 
  pinMode(buzer,OUTPUT);
  pinMode(green_led,OUTPUT);
  pinMode(blue_led,OUTPUT);
  lcd.init();
  lcd.backlight();
  lcd.begin (16, 2);
  // Init RS232
  //Serial.begin(9600);

  // Init SPI bus
  SPI.begin(); 

  // Init MFRC522 
  rfid.PCD_Init(); 
}
 
void loop() 
{
  digitalWrite(blue_led,1);
  digitalWrite(green_led,0);
  lcd.setCursor(1, 0);
  lcd.print("kart basin ...");
  // Initialisé la boucle si aucun badge n'est présent 
  if ( !rfid.PICC_IsNewCardPresent())
    return;

  // Vérifier la présence d'un nouveau badge 
  if ( !rfid.PICC_ReadCardSerial())
    return;

  // Enregistrer l'ID du badge (4 octets) 
  for (byte i = 0; i < 4; i++) 
  {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }
  //convert uid number byte to int after convert it to string
    for (int i = 0; i < 4; i++) 
  {
    UID_int[i] = nuidPICC[i];
    UID_char[i] = String(UID_int[i]);
  }
  // concatenation of all string of uid
  String UID_string = UID_char[0]+UID_char[1]+UID_char[2]+UID_char[3];
//print uid character
  digitalWrite(buzer,1);
  digitalWrite(blue_led,0);
  digitalWrite(green_led,1);
  delay(100);
  digitalWrite(buzer,0);
  lcd.setCursor(1, 0);
  lcd.print("kart kimligi :          ");
  lcd.setCursor(3, 1);
  lcd.print(UID_string);
  delay(2000);
  //Serial.println();
  // Re-Init RFID
  rfid.PICC_HaltA(); // Halt PICC
  rfid.PCD_StopCrypto1(); // Stop encryption on PCD
  lcd.clear();
}
