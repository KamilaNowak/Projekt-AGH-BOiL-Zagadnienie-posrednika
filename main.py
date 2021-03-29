import numpy as np #Do ułatwienia operacji na tablicach

#deklaracja tablic, aby mozna bylo potem łatwo operować na danych
koszty_transportu=np.zeros(shape=(3,2))
ceny_sprzedazy=np.zeros([2])
koszty_zakupu=np.zeros([3])
podaz=np.zeros([3])
popyt=np.zeros([2])


#ceny zakupu/sprzedaży
cz_D1=0
cz_D2=0
cz_D3=0

cs_O1=0
cs_O2=0

#popyt/podaz
pod_D1=0
pod_D2=0
pod_D3=0

pop_O1=0
pop_O2=0

#koszty przwozu
kp_D1_O1=0
kp_D1_O2=0
kp_D2_O1=0
kp_D2_O2=0
kp_D3_O1=0
kp_D3_O2=0

#Czytanie danych wejściowych z pliku
f=open("input.txt","r")
f1=f.readlines()
y=0
for x in f1:
	#cena zakupu
	if(y==1):
		cz_D1=int(x)
		koszty_zakupu[0]=int(x)
	if(y==3):
		cz_D2=int(x)
		koszty_zakupu[1] = int(x)
	if(y==5):
		cz_D3=int(x)
		koszty_zakupu[2] = int(x)
	#cena sprzedaży
	if(y==7):
		cs_O1=int(x)
		ceny_sprzedazy[0]=int(x)
	if(y==9):
		cs_O2=int(x)
		ceny_sprzedazy[1] = int(x)
	#koszt przewozu	
	if(y==11):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D1_O1="zablokowana"
		else:	
			kp_D1_O1=int(x)
			koszty_transportu[0][0]=int(x)
	if(y==13):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D1_O2="zablokowana"
		else:	
			kp_D1_O2=int(x)
			koszty_transportu[0][1] = int(x)
	if(y==15):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D2_O1="zablokowana"
		else:	
			kp_D2_O1=int(x)
			koszty_transportu[1][0] = int(x)
	if(y==17):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D2_O2="zablokowana"
		else:	
			kp_D2_O2=int(x)
			koszty_transportu[1][1] = int(x)
	if(y==19):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D3_O1="zablokowana"
		else:	
			kp_D3_O1=int(x)
			koszty_transportu[2][0] = int(x)
	if(y==21):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D3_O2="zablokowana"
		else:	
			kp_D3_O2=int(x)
			koszty_transportu[2][1] = int(x)
	if(y==23):
		pop_O1=int(x)
		popyt[0]=int(x)
	if(y==25):
		pop_O2=int(x)
		popyt[1]=int(x)
	if(y==27):
		pod_D1=int(x)
		podaz[0]=int(x)
	if(y==29):
		pod_D2=int(x)
		podaz[1]=int(x)
	if(y==31):
		pod_D3=int(x)
		podaz[2]=int(x)
	    		
	y+=1
# ilosc dostawcow: 3
# ilosc odbiorcow: 2
#     |O1|O2|
# |D1| x  x
# |D2| x  x
# |D3| x  x
#  Z = CS -(KZ + KT)

zyski_jednostkowe=np.zeros(shape=(3,2))

for idx, x in np.ndenumerate(zyski_jednostkowe):
  zyski_jednostkowe[idx]=ceny_sprzedazy[idx[1]]-(koszty_zakupu[idx[0]]+koszty_transportu[idx])

f.close()