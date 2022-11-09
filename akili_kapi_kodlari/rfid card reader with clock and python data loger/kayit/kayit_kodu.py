import os
import csv
import serial
import time

ser = serial.Serial('COM7',115200, timeout=0.1) # communication avec l'arduino

def read_sensor_data():
    data = ser.readline()
    return data.decode('utf-8')

#get studend's data
ogrenci_isim = input("Ismin girin : ")
ogrenci_soyismin = input("Soyismin smin girin : ")
ogrenci_kimlik_no = input("ogrenci numarınızı girin : ")
ogrenci_sinif = input("sinif girin : ")
print("Öğreci kartınız basın...")

while True:#enrgistrement du numero du badge
    value = read_sensor_data()
    if value:#verifi si la ligne n'est pas vide si c'est vide sa ne fait rien au cas contraire sa enregistre et sa break
    	ogrenci_kard_id = value
    	break

#save student's data in liste
baslik = ['Ismin' , 'Soyismin' , 'Ogrenci_no' , 'Sinif' , 'Kart_Numarasi' ]
data = [ogrenci_isim,ogrenci_soyismin,ogrenci_kimlik_no,ogrenci_sinif,ogrenci_kard_id]

if os.path.isfile('ogrenci_bilgileri.csv'):#verifie si le fichier existe ou pas
	with open('ogrenci_bilgileri.csv','a', encoding='UTF8' , newline='') as f:#creer le fichier si sa n'existe pas
		writer = csv.writer(f)
		writer.writerow(data)

else:
	with open('ogrenci_bilgileri.csv','w', encoding='UTF8' , newline='') as f:
		writer = csv.writer(f)
		writer.writerow(data)

#pint studen't data
print("ogrenci_kard_id" + " : " +ogrenci_kard_id)
print("Kayıtınız tamamlamıştır...")
#print(baslik)
#print(data)

'''
la library os est utiliser pour verifier si le fichier du system : ici si le fichier existe ou pas
'''