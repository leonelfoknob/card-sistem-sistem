import RPi.GPIO as GPIO
import MFRC522_1
import MFRC522_2
import signal
import time
import pymysql

Host = "localhost"
User = "bmh_ksu"
Password = "@ksu_bmh"
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


def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring

def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)

MIFAREReader_1 = MFRC522_1.MFRC522()
MIFAREReader_2 = MFRC522_2.MFRC522()

print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

while continue_reading:
    GPIO.output(red_led,GPIO.HIGH)
    GPIO.output(blue_led,GPIO.LOW)
    GPIO.output(relay,GPIO.HIGH)

    (status_1, TagType_1) = MIFAREReader_1.MFRC522_Request(MIFAREReader_1.PICC_REQIDL)
    (status_2, TagType_2) = MIFAREReader_2.MFRC522_Request(MIFAREReader_2.PICC_REQIDL)

    if status_1 == MIFAREReader_1.MI_OK or status_2 == MIFAREReader_2.MI_OK:

        (status_1, uid_1) = MIFAREReader_1.MFRC522_SelectTagSN()
        (status_2, uid_2) = MIFAREReader_2.MFRC522_SelectTagSN()
        
        if status_1 == MIFAREReader_1.MI_OK:
            ogrnci_kart_numarasi_giris = uidToString(uid_1)
            query_1 = f"SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
            result_1 = cur.execute(query_1,(ogrnci_kart_numarasi_giris,))
            print(result_1)
            print("Card read UID_1: %s" % uidToString(uid_1))
            if result_1 == 1:
                
                query_giris = f"INSERT INTO ogrenci_girisleri (isim,soyisim,sinif,ogrenci_no) SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
                cur.execute(query_giris,(ogrnci_kart_numarasi_giris,))
                print(f"{cur.rowcount} details insered")
                conn.commit()
                hatasiz_kart_sesi()
                print("gir...")
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.LOW)
                GPIO.output(relay,GPIO.LOW)
                cur.execute(query_1,(ogrnci_kart_numarasi_giris,))
                giren_ogrenci_bilgi = cur.fetchone()
                print(giren_ogrenci_bilgi)
                print(type(giren_ogrenci_bilgi))
                time.sleep(3)
            else:
                hatali_kart_sesi()
                GPIO.output(red_led,GPIO.HIGH)
                GPIO.output(blue_led,GPIO.LOW)
                GPIO.output(relay,GPIO.HIGH)
            

        elif status_2 == MIFAREReader_2.MI_OK:
            ogrnci_kart_numarasi_cikis = uidToString(uid_2)
            query_2 = f"SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
            result_2 = cur.execute(query_2,(ogrnci_kart_numarasi_cikis,))
            print(result_2)
            print("Card read UID_2: %s" % uidToString(uid_2))
            if result_2 == 1:
                query_cikis = f"INSERT INTO ogrenci_cikislari (isim,soyisim,sinif,ogrenci_no) SELECT isim,soyisim,sinif,ogrenci_no FROM ogrenci_kayitlari WHERE (kart_no = %s)"
                cur.execute(query_cikis,(ogrnci_kart_numarasi_cikis,))
                print(f"{cur.rowcount} details insered")
                conn.commit()
                hatasiz_kart_sesi()
                print("gir...")
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.LOW)
                GPIO.output(relay,GPIO.LOW)
                cur.execute(query_2,(ogrnci_kart_numarasi_cikis,))
                cikan_ogrenci_bilgi = cur.fetchone()
                print(cikan_ogrenci_bilgi)
                print(type(cikan_ogrenci_bilgi))
                time.sleep(3)
            else:
                hatali_kart_sesi()
                GPIO.output(red_led,GPIO.HIGH)
                GPIO.output(blue_led,GPIO.LOW)
                GPIO.output(relay,GPIO.HIGH)                
            
        else:
            print("Authentication error")