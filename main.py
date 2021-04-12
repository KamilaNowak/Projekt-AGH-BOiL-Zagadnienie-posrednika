import numpy as np  # Do ułatwienia operacji na tablicach
from math import isnan

# deklaracja tablic, aby mozna bylo potem łatwo operować na danych
koszty_transportu = np.zeros(shape=(3, 2))
ceny_sprzedazy = np.zeros([2])
koszty_zakupu = np.zeros([3])
podaz = np.zeros([3])
popyt = np.zeros([2])


def licz_zyski_jednostkowe(ceny_sprzedazy, koszty_zakupu, koszty_transportu):
    zyski_jednostkowe = np.zeros(shape=(3, 2))

    for idx, x in np.ndenumerate(zyski_jednostkowe):
        zyski_jednostkowe[idx] = ceny_sprzedazy[idx[1]] - (koszty_zakupu[idx[0]] + koszty_transportu[idx])
    return zyski_jednostkowe


def licz_optymalny_plan_przewozow(zyski_jednostkowe, popyt, podaz):
    plan_przewozow = np.zeros(shape=(4, 3))
    optymalne_przewozy = zyski_jednostkowe
    przewozy_wiersze = np.concatenate((optymalne_przewozy, np.array([[0.0, 0.0]])), axis=0)
    zyski = np.concatenate((przewozy_wiersze, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)

    popyt_z_fikcyjnymi = np.append(popyt, np.sum(podaz))
    podaz_z_fikcyjnymi = np.append(podaz, np.sum(popyt))

    while not np.isnan(zyski).all():
        if not np.isnan(zyski[:3, :2]).all():
            maximum = np.nanmax(zyski[:3, :2])
        else:
            maximum = np.nanmax(zyski)

        wiersz_max, kolumna_max = np.nonzero(zyski == maximum)
        index_max = list(map(int, [wiersz_max[0], kolumna_max[0]]))
        zyski[index_max[0], index_max[1]] = np.nan

        plan_przewozow[int(index_max[0]), int(index_max[1])] = min(popyt_z_fikcyjnymi[int(index_max[1])],
                                                                   podaz_z_fikcyjnymi[int(index_max[0])])

        popyt_kopia = list(popyt_z_fikcyjnymi)
        wartosc_zaleznosci = popyt_kopia[int(index_max[1])]

        popyt_z_fikcyjnymi[int(index_max[1])] = max(0, popyt_z_fikcyjnymi[int(index_max[1])] - podaz_z_fikcyjnymi[
            int(index_max[0])])
        podaz_z_fikcyjnymi[int(index_max[0])] = max(0, podaz_z_fikcyjnymi[int(index_max[0])] - wartosc_zaleznosci)

        if (popyt_z_fikcyjnymi[int(index_max[1])] == 0):
            zyski[:, index_max[1]] = np.nan

        if (podaz_z_fikcyjnymi[int(index_max[0])] == 0):
            zyski[index_max[0], :] = np.nan

    return plan_przewozow


def licz_alfa_beta(koszty_transportu, zyski_jednostkowe):
    wiersze, kolumny = np.where(koszty_transportu != 0.0)
    temp = 0

    alfa = [0, np.nan, np.nan]
    beta = [np.nan, np.nan, np.nan]

    while temp < 100 and np.any(np.isnan(beta)) or np.any(np.isnan(alfa)):
        for i, j in zip(wiersze, kolumny):
            if (isnan(alfa[i])) and not (isnan(beta[j])):
                alfa[i] = zyski_jednostkowe[i, j] - beta[j]
            elif not (isnan(alfa[i]) and isnan(beta[j])):
                beta[j] = zyski_jednostkowe[i, j] - alfa[i]
        temp = temp + 1

    return alfa, beta

def licz_delty(zyski_jednostkowe, plan_przewozow,alfa, beta):
    delty = np.zeros(shape=(4, 3))

    for idx, x in np.ndenumerate(plan_przewozow):
        if plan_przewozow[idx] == 0.0:
           delty[idx] = zyski_jednostkowe[idx] - alfa[idx[0]] - beta[idx[1]]
    return delty
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
    popyt = np.array([10, 28, 27])
    podaz = np.array([20, 30])
    koszty_transportu = np.array([[8, 14], [12, 9], [17, 19]])
    ceny_sprzedazy = np.array([10, 12])
    koszty_zakupu = np.array([20, 25, 30])

    # OK WYNIK
    print(licz_zyski_jednostkowe(ceny_sprzedazy, koszty_zakupu, koszty_transportu))
    zyski_temp = np.array([[12, 1], [6, 4], [3, -1]])
    test_popyt = np.array([20, 30])
    test_podaz = np.array([10, 28, 27])

    # OK WYNIK
    print(licz_optymalny_plan_przewozow(zyski_temp, test_popyt, test_podaz))

    mt = np.array([[10., 0., 10.], [0., 28., 2.], [0., 0., 15.]])
    mp = np.array([[12.0, 1.0, 3.0], [6.0, 4.0, -1.0], [0.0, 0.0, 0.0]])

    # OK WYNIK
    alfa, beta = licz_alfa_beta(mt, mp)
    print(alfa)

    optymalne_przewozy = zyski_temp
    przewozy_wiersze = np.concatenate((optymalne_przewozy, np.array([[0.0, 0.0]])), axis=0)
    zyski = np.concatenate((przewozy_wiersze, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)
    test_alfa = np.array([3, -1, 0, 0])
    test_beta = np.array([9, 5, 0])

    # OK WYNIK
    print(licz_delty(zyski, licz_optymalny_plan_przewozow(zyski_temp, test_popyt, test_podaz), test_alfa, test_beta))
