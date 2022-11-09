import RPi.GPIO as GPIO
import MFRC522
import signal
import time


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

def create_file(file_name):
    f= open(file_name,"w+")
    f.close

def write_file(file_name):
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    while continue_reading:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            #print ("Card detected")
            print ("Saving Your Card...")
            (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
            if status == MIFAREReader.MI_OK:
                uid = uidToString(uid)
                #print(uid)
                #f= open(file_name,"a+")
                #f.write(uid+"\n")
                read_file_write(file_name,uid)
                time.sleep(1)
    f.close()

def read_file_write(file_name,uid):
    f= open(file_name,"r")
    f1 = f.readlines()
    for x in f1:
        if uid != x:
            f= open(file_name,"a+")
            f.write(uid+"\n")
            print(uid)


file_name = "uid_card_number.txt"    
#create_file(file_name)
write_file(file_name)
#read_file(file_name)
