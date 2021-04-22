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
            koszty_transportu[0][0] = "zablokowana"
        else:
            kp_D1_O1 = int(x)
            koszty_transportu[0][0] = int(x)
    if (y == 13):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[0][1] = "zablokowana"
        else:
            kp_D1_O2 = int(x)
            koszty_transportu[0][1] = int(x)
    if (y == 15):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[1][0] = "zablokowana"
        else:
            kp_D2_O1 = int(x)
            koszty_transportu[1][0] = int(x)
    if (y == 17):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[1][1] = "zablokowana"
        else:
            kp_D2_O2 = int(x)
            koszty_transportu[1][1] = int(x)
    if (y == 19):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[2][0] = "zablokowana"
        else:
            kp_D3_O1 = int(x)
            koszty_transportu[2][0] = int(x)
    if (y == 21):
        if "x" in x:
            print("Trasa zablokowana")
            koszty_transportu[2][1] = "zablokowana"
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
    # wyznaczenie zysków jednostkowych (zyski_temp)
    zyski_jednostkowe = funkcje.licz_i_zapisz_zyski_jednostkowe(ceny_sprzedazy, koszty_zakupu, koszty_transportu)
    print("\nZyski jednostkowe:")
    print(zyski_jednostkowe)
    # wyznaczenie tablicy transportowej (plan_przewozow)
    tablica_transportowa = funkcje.licz_optymalny_plan_przewozow(zyski_jednostkowe, popyt, podaz)
    print("\nTablica transportowa:")
    print(tablica_transportowa)

    funkcje.zapisz_zysk_calkowity_do_pliku(zyski_jednostkowe, tablica_transportowa, 0)

    # Wyznaczenie alfy i bety
    alfa, beta = funkcje.licz_alfa_beta(tablica_transportowa, zyski_jednostkowe)
    print("\nAlfa:")
    print(alfa)
    print("\nBeta:")
    print(beta)

    print("\nDelty:")
    delty = funkcje.licz_delty(zyski_jednostkowe, tablica_transportowa, alfa, beta)
    print(delty)

    print("\nMaksymalizacja zyskow:")
    tablica_transportowa=funkcje.licz_maksymalizacje_zyskow(tablica_transportowa, delty)
    print(tablica_transportowa)

    print("\nKoszty zakupu:")
    print(koszty_zakupu)
    print("\nKoszty transportu:")
    print(koszty_transportu)

    print("\nKoszt calkowity:")
    print(funkcje.licz_i_zapisz_koszt_calkowity(tablica_transportowa,koszty_zakupu,koszty_transportu))

    funkcje.zapisz_optymalna_tablice_transportowa(tablica_transportowa)

    print("\nTEST PRZYKLADU:")
    delty_test = np.array([[0., -7, 0., -3.], [-2., 0., 0., 1.], [-9., -5., 0., 0.]])
    tab_trans = np.array([[10., 0., 10., 0.], [0., 28., 2., 0.], [0., 0., 15., 50.]])
    print(funkcje.licz_maksymalizacje_zyskow(tab_trans, delty_test))


