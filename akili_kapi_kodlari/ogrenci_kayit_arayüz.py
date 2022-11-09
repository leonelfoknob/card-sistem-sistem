from tkinter import *

ws = Tk()
ws.title("Ogrenci Kayit")
ws.geometry('1080x720')
ws['bg'] = '#42c4c4'
sistem_title =  Label(ws ,text ="Bilgisayar ağları kayit sistemi", font = ("Arial", 50), bg = '#42c4c4', fg = 'white')
sistem_title.pack()
sistem_footer =  Label(ws, text ="leonelfokouong@gmail.com 2022 Copyright All Right Reserved", font = ("Arial", 10), bg = '#42c4c4', fg = 'red')
sistem_footer.pack(side=BOTTOM)

def printValue():
    o_isim = ogrenci_isim.get()
    o_soyisim = ogrenci_soyisim.get()
    o_no = ogrenci_no.get()
    o_sinif = ogrenci_sinif.get()
    '''Label(ws, text=f'{o_isim}, Registered!', pady=20, bg='#ffbf00').pack()
    Label(ws, text=f'{o_soyisim}, Registered!', pady=20, bg='#ffbf00').pack()'''
    print(o_isim)
    print(o_soyisim)
    print(o_no)
    print(o_sinif)

frame_1 =Frame(ws,bg = '#42c4c4') # bd=1, relief = SUNKEN

ogrenci_i =  Label(ws ,text ="isim :")
#ogrenci_i.grid(column = 0 , row = 0)
ogrenci_isim = Entry(frame_1)
ogrenci_isim.pack(padx=5,pady=1,fill=X)
ogrenci_i.pack(padx=5,pady=1,)

ogrenci_soyisim = Entry(frame_1)
ogrenci_soyisim.pack(padx=5,pady=1,fill=X)

ogrenci_no = Entry(frame_1)
ogrenci_no.pack(padx=5,pady=1,fill=X)

ogrenci_sinif = Entry(frame_1)
ogrenci_sinif.pack(padx=5,pady=1,fill=X)



buton_kart_oku = Button(
    frame_1,text="kart okut",font = ("Arial", 50), bg = 'white', fg = '#42c4c4',
    command=''
    )

buton_yeni_kayit = Button(
    frame_1,text="yeni kayıt",font = ("Arial", 50), bg = 'white', fg = '#42c4c4',
    command=printValue
    )
frame_1.pack(expand = YES)
buton_kart_oku.pack(padx=50,pady=10,fill=X)
buton_yeni_kayit.pack(padx=50,pady=10,fill=X)

ws.mainloop()
ismin = printValue()
print(ismin)