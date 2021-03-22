import numpy as np #Do ułatwienia operacji na tablicach

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
	if(y==3):
		cz_D2=int(x)
	if(y==5):
		cz_D3=int(x)
	#cena sprzedaży
	if(y==7):
		cs_O1=int(x)
	if(y==9):
		cs_O2=int(x)
	#koszt przewozu	
	if(y==11):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D1_O1="zablokowana"
		else:	
			kp_D1_O1=int(x)
	if(y==13):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D1_O2="zablokowana"
		else:	
			kp_D1_O2=int(x)
	if(y==15):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D2_O1="zablokowana"
		else:	
			kp_D2_O1=int(x)
	if(y==17):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D2_O2="zablokowana"
		else:	
			kp_D2_O2=int(x)		
	if(y==19):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D3_O1="zablokowana"
		else:	
			kp_D3_O1=int(x)		
	if(y==21):
		if "x" in x:
			print("Trasa zablokowana")
			kp_D3_O2="zablokowana"
		else:	
			kp_D3_O2=int(x)	
	if(y==23):
		pop_O1=int(x)
	if(y==25):
		pop_O2=int(x)
	if(y==27):
		pod_D1=int(x)
	if(y==29):
		pod_D2=int(x)
	if(y==31):
		pod_D3=int(x)

	    		
	y+=1
f.close()