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


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(blue_led,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

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
            uid_no = ''.join(str(e) for e in uid)
            ogrenci_kart_no = int(uid_no)
#             @uid_n := ogrenci_kart_no
            print(uid)
            #luid = ' '.join(map(str, uidToString(uid)))
            #UID = uidToString(uid)
            #print("Card read UID: %s" % uidToString(uid))-->montre luid de la carte
            #print(uidToString(uid))-->montre l'uid de la carte
            #query = f"SELECT * FROM ogrenci_kayitlari WHERE (kart_no = 'uidToString(uid)')"
            #uid = uidToString(uid)
            '''print(uid)
            print(type(uid))
            UID = chr(uid)
            print(UID)'''
            #print(type(UID))
            #print(type(luid))
            query = f"SELECT uid_num FROM uid WHERE uid_num = %s"
            #result = cur.execute(query)
            cur.execute(query, (ogrenci_kart_no,))
            result = cur.fetchone()
            #print(uidToString(uid))
            print(result)
            #print(type(uid))
            '''if uidToString(uid) == uid1 or uidToString(uid) == uid2:
                print("gir...")
                GPIO.output(blue_led,GPIO.HIGH)
                GPIO.output(red_led,GPIO.LOW)
                GPIO.output(relay,GPIO.LOW)
                time.sleep(3)
            #else:
                #GPIO.output(red_led,GPIO.HIGH)
                #GPIO.output(blue_led,GPIO.LOW)
                #GPIO.output(relay,GPIO.HIGH)
                
        else:
            print("Authentication error")'''

