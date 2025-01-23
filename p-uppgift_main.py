import random as rand
import time
import os
os.system("cls")

class Spelare:
    def __init__(self, spelare: str, karta: list, position: list = [0, 0], status: bool = True, pilar: int = 5,):    #initierar spealre klassen
        self.status = status
        self.spelare = spelare
        self.karta = karta
        self.position = position
        self.pilar = pilar

    def flytta_objekt(self, väderstreck: str):                                      #flyttar spelar objektet 
        x, y = self.position

        if väderstreck == "N":
            nytt_x, nytt_y = x - 1, y
        elif väderstreck == "S":
            nytt_x, nytt_y = x + 1, y
        elif väderstreck == "V":
            nytt_x, nytt_y = x, y - 1
        elif väderstreck == "Ö":
            nytt_x, nytt_y = x, y + 1
        else:
            print("Du kan endast förflytta dig med kommandon N/S/V/Ö. 🤣")
            return

        if 0 <= nytt_x < 8 and 0 <= nytt_y < 7:                                    # Kollar så att spelaren försöker röra sig inom kartans gränser            
            self.position = [nytt_x, nytt_y]
            print(f"Du har flyttat till {self.position}.")
        else:
            print("Du försöker gå in i en vägg... spelet är inte så stressfullt. ☜(ﾟヮﾟ☜)")

        self.kolla_fladdermus()
        self.kolla_bottomlöst_hål()

    def kolla_fladdermus(self):                                                     #Kollar om det finns fladdermus runt spelaren eller om spelaren går in i fladdermus.
        x, y = self.position
        karta = self.karta

        if x > 0 and karta[x-1][y] == "F": 
            print(f"Du hör Fladdermöss.")
        if x < len(karta) - 1  and karta[x+1][y] == "F": 
            print(f"Du hör Fladdermöss.")
        if y > 0 and karta[x][y-1] == "F": 
            print(f"Du hör Fladdermöss.")
        if x < len(karta[0])-1 and karta[x][y+1] == "F": 
            print(f"Du hör Fladdermöss.")

        if karta[x][y] == "F":
            print("Du har gått i ni en fladdermus och har blivit buren till en ny position🤑")
            self.fladdermus_flytta()

    def fladdermus_flytta(self):                                                    #Flyttar spelaren till en ny random locaiton ifall spelaren går in i en fladdermuis 
        while True:
            ny_x = rand.randint(0, 7)
            ny_y = rand.randint(0, 6)
            if self.karta[ny_x][ny_y] not in ["F", "H", "W"]:
                self.position = [ny_x, ny_y]
                print(f"Du blev flyttad till {self.position}.")
                break

    def skjuta_pil(self):                                                           #metoden anvädns fölr att kontrollera styurning och antal pilar
        if self.pilar <= 0: #Kollar om det finns pilar kvar 
            print("Du har inga pilar kvar loser 😭🙏")                                  
            return

        print(f"Du har {self.pilar} pilar, när du skjuter kan du styra pilen 3 drag m.h.a N/S/V/Ö")
        pil_position = [self.position[0], self.position[1]]

        for i in range(3):                                                          #Ser til lså att seplaren kan styra pilen i 3 drag
            väderstreck: str = input(f"Du kan styra pilen, {3-i} drag kvar. Vilken riktning N/S/V/Ö?: ").upper()
            if väderstreck == "N":
                nytt_x, nytt_y = pil_position[0] - 1, pil_position[1]
            elif väderstreck == "S":
                nytt_x, nytt_y = pil_position[0] + 1, pil_position[1]
            elif väderstreck == "V":
                nytt_x, nytt_y = pil_position[0], pil_position[1] - 1
            elif väderstreck == "Ö":
                nytt_x, nytt_y = pil_position[0], pil_position[1] + 1
            else:
                print("Endast N/S/V/Ö är giltiga kommandon, låt mig inte säga det igen 😡.")
                break

            if 0 <= nytt_x < 8 and 0 <= nytt_y < 7:
                pil_position = [nytt_x, nytt_y]
                print(f"Pilen är flyttad till {pil_position}. 😈")

                if self.karta[nytt_x][nytt_y] == "W":                               #Avslutar spelet om spelaren träffar Wumpus 
                    print("Pilen träffade Wumpus! Du vinner!")
                    self.status = False
                    break
            else:
                print("Du körde in pilen i en vägg och den gick sönder...")
                break

        self.pilar -= 1
        print(f"Du har nu bara {self.pilar} pilar kvar😢.")
        
        
        if self.pilar == 0:
            print("Du har slut på pilar gubben/gumman")
        else:
            print("Pilen missade. Du har alltså inte vunnit lmao")

    def kolla_bottomlöst_hål(self):                                                 #Exakt ssamma som fladdermus metoden. men dödar spelren ifall den går in i ett hål
        x, y = self.position
        karta = self.karta

        if x > 0 and karta[x-1][y] == "H": 
            print(f"Du känner susningarna av ett djupt hål😨")
        
        if x < len(karta) - 1  and karta[x+1][y] == "H": 
            print(f"Du känner susningarna av ett djupt hål😨")
            
        if y > 0 and karta[x][y-1] == "H": 
            print(f"Du känner susningarna av ett djupt hål😨")
            
        if x < len(karta[0])-1 and karta[x][y+1] == "H": 
            print(f"Du känner susningarna av ett djupt hål😨")

        if karta[x][y] == "H":
            print("Du har gått ner i ett hål och är numera stendöd 💀")
            self.status = False

class Wumpus:
    def __init__(self, karta):                                                      #initierar Wumpus klassen
        self.karta = karta
        self.position = self.placera_wumpus()

    def placera_wumpus(self):                                                       #Placerar Wumpus på en tom ruta.
        while True:
            x = rand.randint(0, 7)
            y = rand.randint(0, 6)
            if self.karta[x][y] == ".":
                self.karta[x][y] = "W"
                return [x, y]

    def flytta(self):                                                               #Flyttar Wumpus till en ny ruta randomly.
        x, y = self.position
        self.karta[x][y] = "."

        while True:
            wumpus_riktning = rand.choice([(-1, 0), (0, -1), (1, 0), (0, 1)])
            steg_x, steg_y = wumpus_riktning
            nytt_x = x + steg_x
            nytt_y = y + steg_y
            
            if 0 <= nytt_x < 8 and 0 <= nytt_y < 7:
                if self.karta[nytt_x][nytt_y] == "H":                               #Wumpus kan inte gå ner i  ett hål
                    continue 
                if self.karta[nytt_x][nytt_y] == "F":                               #Wumpus äter fladdermusen om han går in i den
                    print(f"Wumpus åt precis en fladdermus på positionen: {nytt_x}, {nytt_y}")
                self.karta[nytt_x][nytt_y] = "W"
                self.position = [nytt_x, nytt_y]
                break

def generera_karta():                                                               #Genererar kartan med 8 rader och 7 kolumner i storlek 
    karta: list = []
    for i in range(8):
        rad = ["."] * 7  
        karta.append(rad)
    
    antal_positioner: int = len(karta) * len(karta[0])
    fladdermöss_antal: int = antal_positioner * 30 // 100                                #genererar fladdermus på c.a 30% av kartan
    for i in range(fladdermöss_antal):
        while True:
            x = rand.randint(0, 7)
            y = rand.randint(0, 6)
            if (x, y) != (0, 0) and karta[x][y] == ".":
                karta[x][y] = "F"   
                break

    bottomlöst_hål_antal: int = antal_positioner * 20 // 100                             #genererar hål på c.a 20% av kartan
    for i in range(bottomlöst_hål_antal):
        while True:
            x = rand.randint(0, 7)
            y = rand.randint(0, 6)
            if (x, y) != (0, 0) and karta[x][y] == ".":
                karta[x][y] = "H"  
                break



    
    return karta


def skriv_ut_karta_på_fil(karta):                                                   #skriver ut kartan på en fil. 
    with open("wumpus_källare.csv", "w", encoding="utf-8") as utfil:
        for rad in karta:
            utfil.write(";".join(map(str, rad)) + "\n")


def vad_heter_användaren():                                                         #frågar användarens namn, används inte riktigt
    namn = input("Vad heter du? ")
    return namn


def rör_spelare(karta):                                                             #Funktionen skjöterr spelarens rörelse över kartan. 
    
    namn = vad_heter_användaren()
    användare = Spelare(namn, karta)
    wumpus = Wumpus(karta)

    while användare.status:                                                         #När spelarens status är true alltså spelaren är vid liv loopas detta. 
        print(f"Din position: {användare.position}")
        förflytta_eller_skjuta = input("\nVill du förflytta dig eller skjuta (F/S)? ").upper()
        
        if förflytta_eller_skjuta == "F":
            förflytta = input("Vart vill du förflytta dig Norr/Söder/Väster/Öster (N/S/V/Ö)? ").upper()
            användare.flytta_objekt(förflytta)
            
        elif förflytta_eller_skjuta == "S":                                         #Initierar skjutapil metoden i spelar klassen ifall spelaren vill skjuta "S"
            användare.skjuta_pil()                  
        else: 
            print("Du kan inte skriva sådär🤬 antingen förflytta (F) eller skjuta (S).")
        if användare.status:
            wumpus.flytta()

def introducera_användare_till_spel():                                              #Skriver introduceringen till spelet vilken den hämtar från en fil. 
    with open("wumpus_introduktion.txt", "r", encoding="utf-8") as infil:
        for rad in infil:
            rad = rad.strip()
            print(rad)
            
            
def main():                                                                         #main loop som initierar själva spelet.                           
    introducera_användare_till_spel()
    karta = generera_karta()
    skriv_ut_karta_på_fil(karta)
    rör_spelare(karta)

if __name__ == "__main__":
    main()
