import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import pymysql

Host = "localhost"
User = "root"
Password = "Fokouong01"
database = "ogrenci_bilgi"

conn = pymysql.connect(host = Host , user = User , password = Password, db=database)
cur = conn.cursor()

red_led = 23
blue_led = 24
relay = 22
buzzer = 12


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(blue_led,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

def kart_okumus_sesi():
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)

def hatasiz_kart_sesi():
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)

def hatali_kart_sesi():
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.1)

continue_reading = True


# function to read uid an conver it to a string

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:
    GPIO.output(red_led,GPIO.HIGH)
    GPIO.output(blue_led,GPIO.LOW)
    GPIO.output(relay,GPIO.HIGH)
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        if status == MIFAREReader.MI_OK:
            ogrnci_kart_numarasi = uidToString(uid)
            #print("Card read UID: %s" % uidToString(uid))-->montre luid de la carte
            #print(uidToString(uid))-->montre l'uid de la carte
            #query = f"SELECT * FROM ogrenci_kayitlari WHERE (kart_no = 'uidToString(uid)')"
            #uid = uidToString(uid)
            query1 = f"SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
            result = cur.execute(query1,(ogrnci_kart_numarasi,))
            #cur.execute(query, (uidToString(uid),))
            #result = cur.fetchone()
            #print(uidToString(uid))
            print(result)
            print(type(result))
            #print(type(uid))
            if result == 1:

                query2 = f"INSERT INTO ogrenci_girisleri (isim,soyisim,sinif,ogrenci_no) SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
                cur.execute(query2,(ogrnci_kart_numarasi,))
                print(f"{cur.rowcount} details insered")
                conn.commit()
                hatasiz_kart_sesi()
                print("gir...")
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.LOW)
                GPIO.output(relay,GPIO.LOW)
                cur.execute(query1,(ogrnci_kart_numarasi,))
                giren_ogrenci_bilgi = cur.fetchone()
                print(giren_ogrenci_bilgi)
                print(type(giren_ogrenci_bilgi))
                time.sleep(3)
            else:
                hatali_kart_sesi()
                GPIO.output(red_led,GPIO.HIGH)
                GPIO.output(blue_led,GPIO.LOW)
                GPIO.output(relay,GPIO.HIGH)

        else:
            print("Authentication error")