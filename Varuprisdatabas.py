#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Spec av P-uppgift
# Namn: Ah Zau Marang
# Personnummer:900725-9238
# P-uppgift nr: 145
# Titel: Varuprisdatabas


# **************************** Grafiskt Användargränsnitt ************************

# Vid körning ska programmet se ut som nedan:
#   *Kassaapparat*
#   Mata in kod och antal med mellanslag för varan, t.ex (xxx xx) eller (120 2), och \"<Enter>\"
#   Mata in ett \"#\"-tecken för att skriva ut kvitto!
#   Tryck på \"F1\" för att ångra inmatade inköp eller \"Delete\" för att avbryta hela inmatningen!
#   Mata in kod och antal med en '-' tecken för att minska inmattade inköp, t.ex(-xxx xx)!
#   Inmatning data:
#   100
#   280 2
#   135
#   100
#   #

#   Kvitto:
#   Varunamn    Antal       A-pris      Summa
#   -----------------------------------------
#   CHIPS       2           14.90       14.90
#   VOLVO       2       107000.00   214000.00
#   STÖVLAR     1          159.00      159.90
#   -----------------------------------------
#   Total       5                   214189.70



# ************************** Minne / Datastruktur ************************

#   Varje varan representeras av en lista med var sitt namn (String), antal (int) och pris (int)
#   Alla varorna lagras i en dictionary med varsitt kod som nykel



# ***************************** Algoritm *********************************

# * Börjar med att skapa en lista för en vara och läggs den i en lista.
# * Programmet läser in information om varan från filen.
# * Detta upprepas tills hela filen är inläst.
# * En dictonary skapas och alla listorna läggs in i den med varsitt kod som nykel.
# * Ber användaren mata in kod och antal för varje vara.
# * Kontrollera om inmatningens syntax är korrekt.
# * Kolla om koden finns i databasen samt att det finns tillräckligt antal för varan i lager.
# * Om dessa är ok ska varuantalet subtrahera från antalet i lager, annars felmeddela.
# * Detta upprepas för varje inmatning.
# * Beräkna priset för varan
# * Visar kvitto
# * Detta upprepas tills hela inmatningen är klar.
# * Skriver ut kvitto när inmatningen är klar eller när expediten matar in "#".
# * Sparar datastrukturen i varufil.
# * Stänger av apparat.

# ************************** Programskelett ******************************
# 
#importerar moduler
import tkinter as tk
import Apparat_class
import os


# Läser data från fil, skapar listor var för sig för alla varor och lagrar dem i en "Dictionary"
# returnerar "Dictionary"
def lasFil(filnamn):
    databas={}
    namn=str()
    kod=int()
    fil=open(filnamn, 'r')
    for rad in fil:
        strang = rad.strip()
        if strang.isdigit():
            kod=int(strang)
        elif ' ' in strang:
            lista=strang.split(' ')
            pris=float(lista[0])
            antal=int(lista[1])
            databas[kod]=[namn, pris, antal]
        else:
            namn=strang
    return databas

# uppdaterar varufil
def sparFil(filnamn, databas):
    fil = open(filnamn, 'w')
    for kod in databas:
        fil.write(str(kod) + '\n')
        varu_lista = databas[kod]
        fil.write(varu_lista[0] + '\n')
        fil.write(str(varu_lista[1])+ ' ' + str(varu_lista[2]) + '\n')
    fil.close()
    

# En klass som beskriver ett grafiskt användargränssnitt till kassaapparat
# Attributer:
#   databas - datastrukturen som uppdateras kontinuerligt under körning
#   modifierad_databas - datastrukturen som uppdateras enbast efter utskrift av kvitto
#   filnamn - namnet på varufil
#   indata_lista - en list som sparar alla inmatningar
#   root - huvud fönster
#   ram - ramen som innehåller alla användargränssnitt

class Applikation:
    def __init__(self, databas, original_databas, filnamn):
        self.databas=databas;
        self.modifierad_databas=original_databas;
        self.filnamn=filnamn
        self.indata_lista=[]
        
        # fönster
        self.root=tk.Tk()
        self.root.title("Varuprisdatabas")
        self.root.geometry("680x450")
        self.root.resizable(width=False, height=False)
        
        # ram
        self.ram=tk.Frame(bd=2)

        # initiera användargränssnitt
        self.skapa_Widgets(self.ram)
        self.ram.grid() #skapar rutnät på ramen

        #startar slinga
        self.root.mainloop()

    

    # Skapar widgets(etikett, knapp, inmatningsruta och display) med hjälp av klasser från modul(tkinter) och placerar dem i ramen
    def skapa_Widgets(self, ram):
        self.etikett1=tk.Label(ram, text="*Kassaapparat*", fg="blue", font=('Arial', 16, 'bold'))
        self.etikett1.grid(row=1, column=0, sticky=tk.W)

        self.etikett2=tk.Label(ram, text="Mata in kod och antal med mellanslag för varan, t.ex (xxx xx) eller (120 2), och \"<Enter>\"! \n" \
                            "Mata in ett \"#\"-tecken för att skriva ut kvitto! \n" \
                            "Tryck på \"F1\" för att ångra inmatade inköp eller \"Delete\" för att avbryta hela inmatningen! \n" \
                            "Mata in kod och antal med en '-' tecken för att minska inmattade inköp, t.ex(-xxx xx)!\n" , justify=tk.LEFT, fg="black")
        self.etikett2.grid(columnspan=700, row=2, column=0, sticky=tk.W)

        self.etikett3=tk.Label(ram, text="Ange kod och antal!", fg="black", font=('Arial', 10, 'bold'))
        self.etikett3.grid(row=3, column=0, sticky=tk.W)

        self.etikett4=tk.Label(ram, text='', fg="red")
        self.etikett4.grid(row=4, column=1, sticky=tk.W)

        self.entry=tk.Entry(ram)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "xxx xx")
        self.entry.bind('<Return>', self.uppdateraIndata)
        self.entry.bind('<F1>', self.angra_inmatning)
        self.entry.bind('<Delete>', self.avbryta_inmatning)
        self.entry.grid(row=4, column=0, sticky=tk.W)

        self.display_indata = tk.Text(ram)
        self.display_indata.config(font=('arial', 11, 'normal'), fg='green', width=20, height=15, state='disable')     
        self.display_indata.grid( row=5, column=0, sticky=tk.W) 


        self.display_kvitto = tk.Text(ram)
        self.display_kvitto.config(font=('arial', 11, 'normal'), fg='green', width=60, height=15, state='disable')      
        self.display_kvitto.grid(padx=10, row=5, column=1, sticky=tk.W) 

        self.knapp=tk.Button(ram, text='Avsluta >>', command=self.stangAvApplikation).grid(row=6, sticky=tk.W)


    # meddellar felaktiga inmatningar
    def utskriftFelmeddelande(self, meddelande):
        self.etikett4.destroy()
        self.etikett4=tk.Label(self.ram, text=meddelande, fg="red")
        self.etikett4.grid(row=4, column=1, sticky=tk.W)

    # skriver ut inmatade data
    def visaIndata(self):
        self.display_indata.config(state='normal')
        self.display_indata.delete(0.0, tk.END)
        for element in self.indata_lista:
            if element[1] == 1:
                self.display_indata.insert(tk.END, str(element[0])+'\n')
            else:
                self.display_indata.insert(tk.END, str(element[0])+' '+str(element[1])+'\n')
        self.display_indata.config(state='disable')

    # tar bort felutskrift och rensar inmatningsruta
    def rensaFelmedOchEntre(self):
        self.entry.delete(0, tk.END)
        self.etikett4.destroy()

    # uppdaterar inmatade data eller skriver ut kvitto
    def uppdateraIndata(self, ram):
        apparat=Apparat_class.Kassaapparat(self.databas);
        indata=self.entry.get()
        indata_kod, indata_antal=apparat.avlasningIndata(indata);
        if indata_kod == '#' and self.indata_lista != []:
            self.Kvitto(self.ram)
        else:
            if apparat.syntaxKontroll(indata)==True:
                kod, indata_kod, indata_antal=self.strang_till_heltal(indata_kod, indata_antal)
                index=self.finnaIndex(kod);
                if apparat.varuKontroll(kod)==True:
                    if apparat.antalKontroll(kod, indata_antal, self.indata_lista, index)==True:
                        if apparat.kodKontroll_I_Inmatning(kod, self.indata_lista) == True:
                            if indata_kod < 0:
                                if indata_antal < self.indata_lista[index][1]:
                                    self.indata_lista[index][1] -= indata_antal
                                    self.uppdatera_Databas(kod, indata_antal, 'okning')
                                    self.visaIndata()
                                    self.rensaFelmedOchEntre()
                                elif indata_antal == self.indata_lista[index][1]:
                                    self.indata_lista.remove([kod, indata_antal])
                                    self.uppdatera_Databas(kod, indata_antal, 'okning')
                                    self.visaIndata()
                                    self.rensaFelmedOchEntre()
                                else:
                                    meddelande='Fel inmatning!'
                                    self.utskriftFelmeddelande(meddelande)
                                    self.visaIndata()
                            else:
                                if indata_antal <= self.databas[kod][2]:
                                    self.indata_lista[index][1] += indata_antal
                                    self.uppdatera_Databas(kod, indata_antal, 'minskning')
                                    self.visaIndata()
                                    self.rensaFelmedOchEntre()
                                else:
                                    meddelande='Finns ej tillräckligt antal för varan med koden '+ str(kod)+'!'
                                    self.utskriftFelmeddelande(meddelande)
                                    self.visaIndata()
                        elif apparat.kodKontroll_I_Inmatning(kod, self.indata_lista) == False:
                            if indata_kod > 0:
                                self.indata_lista.append([kod, indata_antal])
                                self.uppdatera_Databas(kod, indata_antal, 'minskning')
                                self.visaIndata()
                                self.rensaFelmedOchEntre()
                            else:
                                meddelande='Fel inmatning!'
                                self.utskriftFelmeddelande(meddelande)
                                self.visaIndata()
                    else:
                        meddelande='Fel inmatning eller finns ej tillräckligt antal för varan med koden '+ str(kod)+'!'
                        self.utskriftFelmeddelande(meddelande)
                else:
                    meddelande='Finns ingen vara med koden '+ str(kod)+'!'
                    self.utskriftFelmeddelande(meddelande)
            else:
                meddelande='Fel inmatning!'
                self.utskriftFelmeddelande(meddelande)


    # finna element i attributen(indata_lista) for rätt kod och returnera dess index
    def finnaIndex(self, kod):
        i=0
        index=0
        for lista in self.indata_lista:
            if lista[0]==kod:
                index=i
            i +=1
        return index
    
    # Uppdaterar datastrukturen(self.databas)
    def uppdatera_Databas(self, kod, indata_antal, nyckel):
        self.vara=Apparat_class.Vara(kod, self.databas)
        if nyckel=='okning':
            self.vara.antalOkning(indata_antal)
        elif nyckel == 'minskning':
            self.vara.antalMinskning(indata_antal)
        self.databas[kod][2]=self.vara.antal

    # ångra inmatade inköp
    def angra_inmatning(self, ram):
        if self.indata_lista != []:
            sista_element=len(self.indata_lista)-1
            kod=self.indata_lista[sista_element][0]
            antal=self.indata_lista[sista_element][1]
            self.uppdatera_Databas(kod, antal, 'okning')
            del self.indata_lista[sista_element]
            self.visaIndata()
            self.rensaFelmedOchEntre()
        else:
            meddelande='Finns ej inmatade data!'
            self.utskriftFelmeddelande(meddelande)

    # Tar bort hela inmatning
    def avbryta_inmatning(self, ram):
        if self.indata_lista != []:
            for element in self.indata_lista:
                kod=element[0]
                antal=element[1]
                self.uppdatera_Databas(kod, antal, 'okning')
            del self.indata_lista[:]
            self.visaIndata()
            self.rensaFelmedOchEntre()
        else:
            meddelande='Finns ej inmatade data!'
            self.utskriftFelmeddelande(meddelande)

    # Konverterar sträng till heltal
    def strang_till_heltal(self, indata_kod, indata_antal):
        kod=str(indata_kod).strip('-')
        kod=int(kod)
        indata_kod=int(indata_kod)
        indata_antal=int(indata_antal)
        return kod, indata_kod, indata_antal
    
    # Skapar kvitto
    def Kvitto(self,ram):
        self.display_indata.config(state='normal')
        self.display_kvitto.config(state='normal')
        self.display_indata.delete(0.0, tk.END)
        self.display_kvitto.delete(0.0, tk.END)
        
        self.display_kvitto.insert(1.0, 'Varunamn\t\tAntal\t\tA-pris\t\tSumma\n')
        self.display_kvitto.insert(2.0, '------------------------------------------------------------------------------------------\n')
        i=3.0
        total_antal=0
        total_summa=0
        for element in self.indata_lista:
            kod=element[0]
            namn=self.databas[kod][0]
            antal=element[1]
            pris=self.databas[kod][1]
            summa=antal*pris
            self.display_kvitto.insert(i, namn+ '\t\t' + str(antal) + '\t\t' + '%.2f' %pris + '\t\t' + '%.2f' %summa +'\n')
            total_antal += antal
            total_summa += summa
            i += 1

        self.display_kvitto.insert(i+1, '------------------------------------------------------------------------------------------\n')
        self.display_kvitto.insert(i+2, '------------------------------------------------------------------------------------------\n')
        self.display_kvitto.insert(i+3, 'Total' + '\t\t' + str(total_antal) + '\t\t\t\t' + '%.2f' %total_summa +'\n')
        
        self.display_kvitto.config(state='disable')
        self.display_indata.config(state='disable')
        del self.indata_lista[:]
        self.rensaFelmedOchEntre()
        self.modifierad_databas=self.databas

    
    
    # Avslutar programkörning
    def stangAvApplikation(self):
        print('Applikationen har stängt!')
        sparFil(self.filnamn, self.modifierad_databas)
        os._exit(99)


#-------huvudprogram-------

if __name__=='__main__':
    filnamn='Databas.txt'
    
    # läser in data från varufil
    databas=lasFil(filnamn)
    original_databas=lasFil(filnamn)
    
    # Anropa attributen(modifierad_databas) från klassen(Applikation)
    modifierad_databas=Applikation(databas, original_databas, filnamn).modifierad_databas
    
    #Sparar datastrukturen i varufil
    sparFil(filnamn, modifierad_databas)
    print('Applikationen har stängt!')
    
