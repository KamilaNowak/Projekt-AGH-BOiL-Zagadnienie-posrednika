import numpy as np  # Do ułatwienia operacji na tablicach
from math import isnan


# funkcja liczy zyski jednostkowe na trasach, i zwraca macierz z wynikami
def licz_i_zapisz_zyski_jednostkowe(ceny_sprzedazy, koszty_zakupu, koszty_transportu):
    zyski_jednostkowe = np.zeros(shape=(3, 2))

    for idx, x in np.ndenumerate(zyski_jednostkowe):
        zyski_jednostkowe[idx] = ceny_sprzedazy[idx[1]] - \
                                 (koszty_zakupu[idx[0]] + koszty_transportu[idx])

    # zapis kosztów jednostkowych do pliku
    f = open("wynik.txt", "w")
    f.write("Zyski jednostkowe:\n")
    f.write("   |_O1__|_O2__|\n")
    f.write("D1 |"+str(zyski_jednostkowe[0][0]) + "|")
    f.write(str(zyski_jednostkowe[0][1]) + "|\n")
    f.write("D2 |"+str(zyski_jednostkowe[1][0]) + "|")
    f.write(str(zyski_jednostkowe[1][1]) + "|\n")
    f.write("D3 |"+str(zyski_jednostkowe[2][0]) + "|")
    f.write(str(zyski_jednostkowe[2][1]) + "|\n")
    f.close()
    return zyski_jednostkowe


# funckja liczy optymalny plan przewozów tzn. dodaje fikcyjnego dostawcę i fikcyjnego odbiorcę wypełniając w tych miejscach macierz zerami.
# rozpoczynamy rozpisywanie przewozów od tras, na których osiągany zysk jest największy.
# Pamiętamy przy tym o regule, ze na poczatku  rozpisujemy trasy między dostawcami i odbiorcami rzeczywistymi, potem fikcyjnymi.
# Funckja zwraca: macierz, z wartoścami na trasach, a tam gdzie nie ma wartości są nany
def licz_optymalny_plan_przewozow(zyski_jednostkowe, popyt, podaz):
    # tabela przewozów z fikcyjnym dostawcą i odbiorcą
    plan_przewozow = np.zeros(shape=(4, 3))
    optymalne_przewozy = zyski_jednostkowe
    przewozy_wiersze = np.concatenate(
        (optymalne_przewozy, np.array([[0.0, 0.0]])), axis=0)
    zyski = np.concatenate(
        (przewozy_wiersze, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)

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
        podaz_z_fikcyjnymi[int(index_max[0])] = max(
            0, podaz_z_fikcyjnymi[int(index_max[0])] - wartosc_zaleznosci)

        if (popyt_z_fikcyjnymi[int(index_max[1])] == 0):
            zyski[:, index_max[1]] = np.nan

        if (podaz_z_fikcyjnymi[int(index_max[0])] == 0):
            zyski[index_max[0], :] = np.nan

    return plan_przewozow


# Funckja obllicza alfy i bety na podstawy macierzy kosztów transportu i zysków jednostkowych. Zwraca obiekt zawierający dwie tablice = aldy oraz bety


def licz_alfa_beta(koszty_transportu, zyski_jednostkowe):
    zj = np.concatenate((zyski_jednostkowe, np.array([[0.0, 0.0]])), axis=0)
    zyski_jednostkowe = np.concatenate((zj, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)

    wiersze, kolumny = np.where(koszty_transportu != 0.0)
    temp = 0

    alfa = [0, np.nan, np.nan, np.nan]
    beta = [np.nan, np.nan, np.nan]

    while temp < 20 and np.any(np.isnan(beta)) or np.any(np.isnan(alfa)):
        for i, j in zip(wiersze, kolumny):
            if (isnan(alfa[i])) and not (isnan(beta[j])):
                alfa[i] = zyski_jednostkowe[i, j] - beta[j]
            elif not (isnan(alfa[i]) and isnan(beta[j])):
                beta[j] = zyski_jednostkowe[i, j] - alfa[i]
        temp = temp + 1
    return alfa, beta


def licz_delty(zyski_jednostkowe, plan_przewozow, alfa, beta):
    zj = np.concatenate((zyski_jednostkowe, np.array([[0.0, 0.0]])), axis=0)
    zyski_jednostkowe = np.concatenate((zj, (np.array([[0.0, 0.0, 0.0, 0.0]])).T), axis=1)

    delty = np.zeros(shape=(4, 3))  # tabela wskaźników optymalności

    for idx, x in np.ndenumerate(plan_przewozow):
        if (plan_przewozow[idx] == 0.0):
            delty[idx] = zyski_jednostkowe[idx] - alfa[idx[0]] - beta[idx[1]]
    return delty




# Zapisywanie zysku pośrednika do pliku , póki co nie uwzględnia blokowania tras
# kontrola=0 -> zyski poczatkowe
# kontrola=1 -> zyski koncowe
def zapisz_zysk_calkowity_do_pliku(zyski_jednostkowe, plan_przewozow, kontrola):
    zyski = 0
    for i in range(3):
        for j in range(2):
            zyski += zyski_jednostkowe[i][j] * plan_przewozow[i][j]

    f = open("wynik.txt", "a")
    if (kontrola == 0):
        f.write("\nZysk poczatkowy:\n")
    else:
        f.write("\nZysk koncowy:\n")
    f.write(str(zyski) + "\n")
    f.close()

# funckja maksymalizuje zyski soiagane przez posrednika.
# Tzn wybiera dodatni element w tablicy i dodaje/odejmuje wartość minimum z z tych tras/
def licz_maksymalizacje_zyskow(tab_transportowa, delty):

    wiersze, kolumny = np.where(delty > 0.)
    delty[delty == 0.0] = np.nan

    for i, j in (zip(wiersze, kolumny)):
        lista_wiersze_zer = list((np.where(np.isnan(delty[i, :])))[0])
        lista_kolumny_zer = list((np.where(np.isnan(delty[:, j])))[0])

        for X in lista_wiersze_zer:
            for Y in lista_kolumny_zer:
                if (isnan(delty[Y, X])):

                    min_z_tras = min([tab_transportowa[Y, X]],
                                      tab_transportowa[i, X],
                                      tab_transportowa[Y, j])

                    tab_transportowa[i, j] = tab_transportowa[i, j] + min_z_tras
                    tab_transportowa[Y, X] = tab_transportowa[Y, X] + min_z_tras

                    tab_transportowa[i, X] = tab_transportowa[i, X] - min_z_tras
                    tab_transportowa[Y, j] = tab_transportowa[Y, j] - min_z_tras

    return tab_transportowa

def licz_i_zapisz_koszt_calkowity(tablica_transportowa,koszty_zakupu,koszty_transportu):
    koszt_calkowity=0
    for i in range(3):
        for j in range(2):
            koszt_calkowity+=tablica_transportowa[i][j]*(koszty_zakupu[i]+koszty_transportu[i][j])

    f = open("wynik.txt", "a")
    f.write("\nKoszt calkowity:\n")
    f.write(str(koszt_calkowity))
    f.close()
    return koszt_calkowity   

def zapisz_optymalna_tablice_transportowa(tab_transportowa):
    f = open("wynik.txt", "a")
    f.write("\n\nOptymalna tablica transportowa:\n")
    f.write("  |_O1_|_O2_|_FO_|\n")    
    for i in range(4):
        if i!=3:
            f.write("D"+str(i+1)+"| ")
        else:
            f.write("FD"+"| ")    
        for j in range(3):
            if tab_transportowa[i][j]>=100:
                f.write(str(int(tab_transportowa[i][j]))+"| ")
            elif tab_transportowa[i][j]>=10:
                f.write(str(int(tab_transportowa[i][j]))+" | ")
            else:
                f.write(str(int(tab_transportowa[i][j]))+"  | ")    
        f.write("\n")    
    f.close()        

