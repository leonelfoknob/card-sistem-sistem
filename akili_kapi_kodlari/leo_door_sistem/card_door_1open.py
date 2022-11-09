import RPi.GPIO as GPIO
import MFRC522
import signal
import time

red_led = 23
blue_led = 24
relay = 22

uid1 = "DBB1ECF9"
uid2 = "EBD89082"

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
            #print("Card read UID: %s" % uidToString(uid))-->montre luid de la carte
            #print(uidToString(uid))-->montre l'uid de la carte
            if uidToString(uid) == uid1 or uidToString(uid) == uid2:
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
            print("Authentication error")