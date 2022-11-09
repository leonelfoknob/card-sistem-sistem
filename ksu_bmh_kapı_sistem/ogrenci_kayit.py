import RPi.GPIO as GPIO
import MFRC522_1
import signal
import pymysql#bu kutuphane kullanılmadı ama kullanılailir
import mariadb

Host = "localhost"
User = "root"
Password = "1"
database = "ogrenci_bilgi"
Port = 3306


conn = mariadb.connect(user = User , password = Password,host = Host ,port = Port, db=database)
cur = conn.cursor()


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

ogrenci_isim = input("Ismin girin : ")
ogrenci_soyisim = input("Soyismin smin girin : ")
ogrenci_no = int(input("ogrenci numarınızı girin : "))
ogrenci_sinif = int(input("sinif girin : "))
print("Öğreci kartınız basın...")

while continue_reading:
    (status_1, TagType_1) = MIFAREReader_1.MFRC522_Request(MIFAREReader_1.PICC_REQIDL)
    if status_1 == MIFAREReader_1.MI_OK:
        (status_1, uid_1) = MIFAREReader_1.MFRC522_SelectTagSN()
        if status_1 == MIFAREReader_1.MI_OK:
            ogrenci_kart_no = str(uidToString(uid_1))
            #print ("Card numarasi : " + " " + ogrenci_kart_numarasi)
            break
        else:
            print("Authentication error")

query = f"INSERT INTO ogreci_kayit (ismin,soyismin,sinif,ogrenci_no,kart_no) VALUES ('{ogrenci_isim}','{ogrenci_soyisim}','{ogrenci_sinif}','{ogrenci_no}','{ogrenci_kart_no}')" #SAVE DATA İN DATABASE         
cur.execute(query)
print(f"{cur.rowcount} details insered")
conn.commit()
conn.close()

print("isim : " + " " + ogrenci_isim)
print("soyisim : " + " " + ogrenci_soyisim)
print("ogrenci no :" + " " + ogrenci_kimlik_no)
print("sinif :  " + " " + ogrenci_sinif)
print("ogrenci kard id : " + " " + ogrenci_kard_id )
print("Kayitiniz Tamamlandi...")
