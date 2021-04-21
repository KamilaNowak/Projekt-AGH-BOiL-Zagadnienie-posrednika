import numpy as np  # Do ułatwienia operacji na tablicach
from math import isnan
import funkcje

# deklaracja tablic, aby mozna bylo potem łatwo operować na danych
koszty_transportu = np.zeros(shape=(3, 2))
ceny_sprzedazy = np.zeros([2])
koszty_zakupu = np.zeros([3])
podaz = np.zeros([3])
popyt = np.zeros([2])

# Czytanie danych wejściowych z pliku
f = open("input.txt", "r")
f1 = f.readlines()
y = 0
for x in f1:
    # cena zakupu
    if (y == 1):
        koszty_zakupu[0] = int(x)
    if (y == 3):
        koszty_zakupu[1] = int(x)
    if (y == 5):
        koszty_zakupu[2] = int(x)
    # cena sprzedaży
    if (y == 7):
        ceny_sprzedazy[0] = int(x)
    if (y == 9):
        ceny_sprzedazy[1] = int(x)
    # koszt przewozu
    if (y == 11):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[0][0] ="zablokowana"
        else:
            kp_D1_O1 = int(x)
            koszty_transportu[0][0] = int(x)
    if (y == 13):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[0][1] ="zablokowana"
        else:
            kp_D1_O2 = int(x)
            koszty_transportu[0][1] = int(x)
    if (y == 15):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[1][0] ="zablokowana"
        else:
            kp_D2_O1 = int(x)
            koszty_transportu[1][0] = int(x)
    if (y == 17):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[1][1] ="zablokowana"
        else:
            kp_D2_O2 = int(x)
            koszty_transportu[1][1] = int(x)
    if (y == 19):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[2][0] ="zablokowana"
        else:
            kp_D3_O1 = int(x)
            koszty_transportu[2][0] = int(x)
    if (y == 21):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[2][1] ="zablokowana"
        else:
            kp_D3_O2 = int(x)
            koszty_transportu[2][1] = int(x)
    if (y == 23):        
        popyt[0] = int(x)
    if (y == 25):        
        popyt[1] = int(x)
    if (y == 27):        
        podaz[0] = int(x)
    if (y == 29):        
        podaz[1] = int(x)
    if (y == 31):
        podaz[2] = int(x)
    y += 1
f.close()

if __name__ == "__main__":
    #wyznaczenie zysków jednostkowych (zyski_temp)
    zyski_jednostkowe=funkcje.licz_zyski_jednostkowe(ceny_sprzedazy,koszty_zakupu,koszty_transportu)
    print("Zyski jednostkowe:")
    print(zyski_jednostkowe)
    print("\n")
    #wyznaczenie tablicy transportowej (plan_przewozow)
    tablica_transportowa=funkcje.licz_optymalny_plan_przewozow(zyski_jednostkowe,popyt,podaz)    
    print("Tablica transportowa:")
    print(tablica_transportowa)
    print("\n")

    funkcje.zapisz_zyski_do_pliku(zyski_jednostkowe,tablica_transportowa,0) 

    #Wyznaczenie alfy i bety
    alfa,beta=funkcje.licz_alfa_beta(koszty_transportu,zyski_jednostkowe)
    print("Alfa:")
    print(alfa)
    print("\n")
    print("Beta:")
    print(beta)
    print("\n")

    #Co robią te dwie linijki?
    przewozy_wiersze = np.concatenate((tablica_transportowa, np.array([[0.0, 0.0]])), axis=0)
    zyski = np.concatenate((przewozy_wiersze, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)

    delty=funkcje.licz_delty(zyski,tablica_transportowa,alfa,beta)

    print(delty)


   
