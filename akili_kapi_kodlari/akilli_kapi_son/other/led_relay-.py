#Relay GPIO 22-->12numarallı pin control maniyetik kilit
#red_led GPIO 23-->16numaralı pin door_close
#blue_led GPIG 24-->18numaralı pin door_open
# contrairement a l'arduino le high du relay fonctionne en 3.3v et non en 5v si vous connecter au 5 volt sa ne va pas fonctionner

import RPi.GPIO as GPIO
import time

red_led = 23
blue_led = 24
relay = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(blue_led,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)


#for i in range():
while True:
    print("Red led on | Blue led off")
    GPIO.output(red_led,GPIO.HIGH)
    GPIO.output(blue_led,GPIO.LOW)
    GPIO.output(relay,GPIO.HIGH)
    time.sleep(1)
    print("Blue led on | Red led off")
    GPIO.output(blue_led,GPIO.HIGH)
    GPIO.output(red_led,GPIO.LOW)
    GPIO.output(relay,GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
# my id card number = DBB1ECF9
