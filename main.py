import numpy as np  # Do ułatwienia operacji na tablicach
from math import isnan

# deklaracja tablic, aby mozna bylo potem łatwo operować na danych
koszty_transportu = np.zeros(shape=(3, 2))
ceny_sprzedazy = np.zeros([2])
koszty_zakupu = np.zeros([3])
podaz = np.zeros([3])
popyt = np.zeros([2])


def licz_zyski_jednostkowe(ceny_sprzedazy,koszty_zakupu, koszty_transportu):
    zyski_jednostkowe = np.zeros(shape=(3, 2))

    for idx, x in np.ndenumerate(zyski_jednostkowe):
        zyski_jednostkowe[idx] = ceny_sprzedazy[idx[1]] - (koszty_zakupu[idx[0]] + koszty_transportu[idx])

    return zyski_jednostkowe


def licz_optymalny_plan_przewozow(zyski_jednostkowe,popyt, podaz):
    opt_przewozy = zyski_jednostkowe

    #dodanie zera do fikcyjnych odbiorców i dostawców
    zeros_2 = np.array([[0, 0]])
    zeros_4 = np.array([[0, 0, 0, 0]])
    przewozy_wiersz = np.concatenate((opt_przewozy, zeros_2), axis=0)
    przewozy_kolumna = np.concatenate((przewozy_wiersz, zeros_4.T), axis=1)

    popyt_calosc = np.append(popyt, np.sum(podaz))
    podaz_calosc = np.append(podaz, np.sum(popyt))
    print(popyt_calosc)
    print(podaz_calosc)
    return przewozy_kolumna


def licz_alfa_beta(koszty_transportu, zyski_jednostkowe):
    alfa = [0, np.nan, np.nan]
    beta = [np.nan, np.nan, np.nan]
    temp = 0
    wiersze, kolumny = np.where(koszty_transportu != 0.0)

    while temp < 100 and np.any(np.isnan(beta)) or np.any(np.isnan(alfa)):
        for i, j in zip(wiersze, kolumny):
            if (isnan(alfa[i])) and not (isnan(beta[j])):
                alfa[i] = zyski_jednostkowe[i, j] - beta[j]
            elif not (isnan(alfa[i]) and isnan(beta[j])):
                beta[j] = zyski_jednostkowe[i, j] - alfa[i]
        temp = temp + 1

    return alfa, beta


# ceny zakupu/sprzedaży
cz_D1 = 0
cz_D2 = 0
cz_D3 = 0

cs_O1 = 0
cs_O2 = 0

# popyt/podaz
pod_D1 = 0
pod_D2 = 0
pod_D3 = 0

pop_O1 = 0
pop_O2 = 0

# koszty przwozu
kp_D1_O1 = 0
kp_D1_O2 = 0
kp_D2_O1 = 0
kp_D2_O2 = 0
kp_D3_O1 = 0
kp_D3_O2 = 0

# Czytanie danych wejściowych z pliku
f = open("input.txt", "r")
f1 = f.readlines()
y = 0
for x in f1:
    # cena zakupu
    if (y == 1):
        cz_D1 = int(x)
        koszty_zakupu[0] = int(x)
    if (y == 3):
        cz_D2 = int(x)
        koszty_zakupu[1] = int(x)
    if (y == 5):
        cz_D3 = int(x)
        koszty_zakupu[2] = int(x)
    # cena sprzedaży
    if (y == 7):
        cs_O1 = int(x)
        ceny_sprzedazy[0] = int(x)
    if (y == 9):
        cs_O2 = int(x)
        ceny_sprzedazy[1] = int(x)
    # koszt przewozu
    if (y == 11):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D1_O1 = "zablokowana"
        else:
            kp_D1_O1 = int(x)
            koszty_transportu[0][0] = int(x)
    if (y == 13):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D1_O2 = "zablokowana"
        else:
            kp_D1_O2 = int(x)
            koszty_transportu[0][1] = int(x)
    if (y == 15):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D2_O1 = "zablokowana"
        else:
            kp_D2_O1 = int(x)
            koszty_transportu[1][0] = int(x)
    if (y == 17):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D2_O2 = "zablokowana"
        else:
            kp_D2_O2 = int(x)
            koszty_transportu[1][1] = int(x)
    if (y == 19):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D3_O1 = "zablokowana"
        else:
            kp_D3_O1 = int(x)
            koszty_transportu[2][0] = int(x)
    if (y == 21):
        if "x" in x:
            print("Trasa zablokowana")
            kp_D3_O2 = "zablokowana"
        else:
            kp_D3_O2 = int(x)
            koszty_transportu[2][1] = int(x)
    if (y == 23):
        pop_O1 = int(x)
        popyt[0] = int(x)
    if (y == 25):
        pop_O2 = int(x)
        popyt[1] = int(x)
    if (y == 27):
        pod_D1 = int(x)
        podaz[0] = int(x)
    if (y == 29):
        pod_D2 = int(x)
        podaz[1] = int(x)
    if (y == 31):
        pod_D3 = int(x)
        podaz[2] = int(x)

    y += 1

f.close()

if __name__ == "__main__":
   # testy

    op = np.array([[12, 1], [6, 4], [3, -1]])
    t_popyt = np.array([20, 30])
    t_podaz = np.array([10, 28, 27])
    t1 = licz_optymalny_plan_przewozow(op, t_popyt, t_podaz)
    print(t1)
   # mt = np.array([[10., 0., 10.], [0., 28., 2.], [0., 0., 15.]])
   # mp = np.array([[12.0, 1.0, 3.0], [6.0, 4.0, -1.0], [0.0, 0.0, 0.0]])

    #print(licz_alfa_beta(mt, mp))
