#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
#    Copyright 2018 Daniel Perron
#
#    Base on Mario Gomez <mario.gomez@teubi.co>   MFRC522-Python
#
#    This file use part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software:
#    you can redistribute it and/or modify
#    it under the terms of
#    the GNU Lesser General Public License as published by the
#    Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the
#    GNU Lesser General Public License along with MFRC522-Python.
#    If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522_1
import MFRC522_2
import signal

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
MIFAREReader_1 = MFRC522_1.MFRC522()
MIFAREReader_2 = MFRC522_2.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status_1, TagType_1) = MIFAREReader_1.MFRC522_Request(MIFAREReader_1.PICC_REQIDL)
    (status_2, TagType_2) = MIFAREReader_2.MFRC522_Request(MIFAREReader_2.PICC_REQIDL)

    # If a card is found
    if status_1 == MIFAREReader_1.MI_OK:
        print ("Card detected")

        # Get the UID of the card
        (status_1, uid_1) = MIFAREReader_1.MFRC522_SelectTagSN()
        # If we have the UID, continue
        if status_1 == MIFAREReader_1.MI_OK:
            print("Card read UID1: %s" % uidToString(uid_1))
        else:
            print("Authentication error")
    #**************
    if status_2 == MIFAREReader_2.MI_OK:
        print ("Card detected")

        # Get the UID of the card
        (status_2, uid_2) = MIFAREReader_2.MFRC522_SelectTagSN()
        # If we have the UID, continue
        if status_2 == MIFAREReader_2.MI_OK:
            print("Card read UID2: %s" % uidToString(uid_2))
        else:
            print("Authentication error")