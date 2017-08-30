
#En klass som beskriver en kassaapparat.
# databas - datastrukturen
class Kassaapparat:

    #**************************** Metoder *********************************

    # Konstruktorn, initierar attributen databas
    def __init__(self, databas):
        self.databas=databas

    
    # Kontrollera om inmatningens syntax är korrekt.
    # returnerar True eller False
    def syntaxKontroll(self, indata):
        try:
            indata=indata.strip()
            indata=indata.split(' ')
            for element in indata:
                element=int(element)
                if element==0:
                    return False
                
            if len(indata) == 2:
                if int(indata[1]) <= 0:
                    return False
            
            if indata[0]=='' :
                return False
            elif 0 < len(indata) <= 2:
                return True
            else:
                return False
        except:
            return False

    # Läser av inmatade data och returnerar kod och antal
    def avlasningIndata(self, indata):
        indata=indata.strip()
        indata=indata.split(' ');
        indata_kod=indata[0];
        if len(indata)== 1:
            indata_antal=str(1);
        else:
            indata_antal=indata[1]
        return indata_kod, indata_antal
    
    # Kontrollerar om koden finns i databasen, dvs om varan finns i lager
    # returnerar True eller False
    def varuKontroll(self, kod):
        if kod in self.databas:
            return True
        else:
            return False

    # Kontrollera om det finns tillräckligt antal för varan i lager
    # returnerar True eller False
    def antalKontroll(self, kod, indata_antal, indata_lista, index):
        if indata_antal <= self.databas[kod][2]:
            return True
        elif indata_antal > self.databas[kod][2] and indata_lista != []:
            if self.kodKontroll_I_Inmatning(kod, indata_lista)==True and indata_antal <= indata_lista[index][1]:
                return True
            else:
                return False
        else:
            return False

    # Kontrollerar om det redan finns varan i inmatningen
    def kodKontroll_I_Inmatning(self, kod, indata_lista):
        lexikon={}
        for element in indata_lista:
            lexikon[element[0]]=element[1]
            
        if kod in lexikon:
            return True
        if kod not in lexikon:
            return False




# En klass som beskriver en varu-objekt.
# Attributer:
#   kod - kod för vara
#   namn - namn på vara
#   pris - pris på vara
#   antal - antal på vara

class Vara():
    # Konstruktorn, initierar attributer kod, namn, pris, antal
    def __init__(self, kod, databas):
        self.kod=kod
        self.namn=databas[kod][0]
        self.pris=databas[kod][1]
        self.antal=databas[kod][2]


    # Inmatade antal subtraheras från varuantal i lager
    def antalMinskning(self, antal):
        self.antal -= antal
    
    # Inmatade antalet adderas till varuantal i lager
    def antalOkning(self, antal):
        self.antal += antal

        
