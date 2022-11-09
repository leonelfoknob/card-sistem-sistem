import csv

isim=input("isimim gir :")
soyisim=input("soyisim gir")
ogrencino=input("ogrenci no gir :")
sinif=input("sinif gir :")

with open('kayit_dosya.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in (('Isim', 'Soyismin','Ogrenci no','Sınıf'),(isim,soyisim,ogrencino,sinif)):
            writer.writerow(row)