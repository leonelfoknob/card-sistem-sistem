import RPi.GPIO as GPIO
import time

buzzer = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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


hatali_kart_sesi()

