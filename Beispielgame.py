# Pygame Beispiel
import os, sys, pygame, pygame.locals, random
#import /Projekt/kleineViren

# Initialisieren von PyGame
pygame.init()

# Fenster öffnen
screen =pygame.display.set_mode((1200, 800))

# Titel für Fensterkopf
pygame.display.set_caption('PyVirus')

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Liste für Zustände für die Richtungen des Virus + Variable, der immer ein Zustand zugeordnet wird
zustandsliste =["Oben", "Unten", "Links", "Rechts", "Nichts", "Gameover"]

# Startzustand auf Nichts setzen
zustand = zustandsliste[4]

# Zaehler fuer Virenkettebewegung
zaehler = 0

# Hauptvirus Dictionary
eigenschaftenHauptvirus = {
    "PositionX" : 600,
    "PositionY" : 400,
    "Laenge" : 1
}

# Liste mit den letzten 50 Zustaende vom Hauptvirus








# Liste fuer die kleine Viren
eigenschaftenKleinVirus = {
    "PositionX" : 0,
    "PositionY" : 0,
    "Zaehler" : 1999,
    "Bild" : 0
}

# Listen fuer Virenkette
virenKettePositionX = []
virenKettePositionY = []
virenKetteZustand = []
virenKetteBild = []

# Virus Bilder - Idee von https://pythonprogramming.net/displaying-images-pygame/
hauptVirus = pygame.image.load('rsz_kleineviren1.png')
# Bild verkleinern https://stackoverflow.com/questions/43046376/how-to-change-an-image-size-in-pygame/43053791
hauptVirus = pygame.transform.scale(hauptVirus, (50, 50))

virusRot = pygame.image.load('rsz_kleineviren2.png')
virusOrange = pygame.image.load('rsz_kleineviren3.png')
virusGelb = pygame.image.load('rsz_kleineviren4.png')
virusGruen = pygame.image.load('rsz_kleineviren5.png')
virusBlau = pygame.image.load('rsz_kleineviren6.png')
virusLila = pygame.image.load('rsz_kleineviren7.png')
virusPink = pygame.image.load('rsz_kleineviren8.png')
virusGrau = pygame.image.load('rsz_kleineviren9.png')

# Liste mit Bilder
virusBilderold =[virusRot, virusOrange, virusGelb, virusGruen, virusBlau, virusLila, virusPink, virusGrau]
virusBilder = []

# Virenbilder resize
for Bild in virusBilderold:
    Bild = pygame.transform.scale(Bild, (50, 50))
    virusBilder.append(Bild)

# Kollisionspruefung
def collisionPruefung(hauptVirus, kleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, eigenschaftenHauptvirus, zustand, virenKetteBild):
    if not (hauptVirus["PositionX"] >= kleinVirus["PositionX"]+50 or hauptVirus["PositionX"] <= kleinVirus["PositionX"] - 50) and not (hauptVirus["PositionY"] >= kleinVirus["PositionY"]+50 or hauptVirus["PositionY"] <= kleinVirus["PositionY"] - 50):
        hauptVirus["Laenge"] += 1
        kleinVirus["Zaehler"] = 1999
        if len(virenKettePositionX) == 0:
            if zustand == "Links":
                virenKettePositionX.append(eigenschaftenHauptvirus["PositionX"]+50)
                virenKettePositionY.append(eigenschaftenHauptvirus["PositionY"])
                virenKetteZustand.append("Links")
            elif zustand == "Rechts":
                virenKettePositionX.append(eigenschaftenHauptvirus["PositionX"]-50)
                virenKettePositionY.append(eigenschaftenHauptvirus["PositionY"])
                virenKetteZustand.append("Rechts")
            elif zustand == "Oben":
                virenKettePositionX.append(eigenschaftenHauptvirus["PositionX"])
                virenKettePositionY.append(eigenschaftenHauptvirus["PositionY"]+50)
                virenKetteZustand.append("Oben")
            elif zustand == "Unten":
                virenKettePositionX.append(eigenschaftenHauptvirus["PositionX"])
                virenKettePositionY.append(eigenschaftenHauptvirus["PositionY"]-50)
                virenKetteZustand.append("Unten")
            virenKetteBild.append(kleinVirus["Bild"])

# Funktion um kleine Viren zu erstellen
def kleineViren(x, y, dictionary, zustand, viren):
    z = dictionary["Zaehler"]
    if zustand != "Nichts" and zustand != "Gameover":
        z += 1
        if z == 2000:

            randomvirus = random.randrange(0, 7)
            randomvirus = viren[randomvirus]
            dictionary["Bild"] = randomvirus

            randomx = random.randrange(0, 1150)
            randomy = random.randrange(0, 750)

            while not (randomx >= x+100 or randomx <= x-100):
                randomx = random.randrange(0, 1150)
            dictionary["PositionX"] = randomx

            while not (randomy >= y+100 or randomy <= y-100):
                randomy = random.randrange(0, 750)
            dictionary["PositionY"] = randomy
            z = 0

        dictionary["Zaehler"] = z
    return dictionary

# Schleife Hauptprogramm
while spielaktiv:
    # Prüfung, in welche Richtung sich der Spieler automatisch nach vorne bewegen soll.

    if zustand == zustandsliste[0]:
        if eigenschaftenHauptvirus["PositionY"] != 0:
            eigenschaftenHauptvirus["PositionY"] -=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[1]:
        if eigenschaftenHauptvirus["PositionY"] != 750: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionY"] +=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[2]:
        if eigenschaftenHauptvirus["PositionX"] != 0:
            eigenschaftenHauptvirus["PositionX"] -=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[3]:
        if eigenschaftenHauptvirus["PositionX"] != 1150: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionX"] +=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])
    # Zuruecksetzen der Zustand, wenn der Rand getroffen wurde
    elif zustand == zustandsliste[5]:
        eigenschaftenHauptvirus["PositionX"] = 600
        eigenschaftenHauptvirus["PositionY"] = 400
        virenKettePositionX = []
        virenKettePositionY = []
        virenKetteZustand = []
        virenKetteBild = []

    virenIndex = 0
    for anzahlVirus in virenKettePositionX:
        if virenIndex == 0:
            if zaehler == 50:
                virenKetteZustand[virenIndex] = zustand
                zaehler = 0
            else:
                zaehler += 1

        if virenKetteZustand[virenIndex] == "Oben":
            virenKettePositionY[virenIndex] -= 0.5
        elif virenKetteZustand[virenIndex] == "Unten":
            virenKettePositionY[virenIndex] += 0.5
        elif virenKetteZustand[virenIndex] == "Links":
            virenKettePositionX[virenIndex] -= 0.5
        elif virenKetteZustand[virenIndex] == "Rechts":
            virenKettePositionX[virenIndex] += 0.5

        virenIndex += 1
    print(virenKetteZustand)
    print(virenKettePositionX)

# Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            # Spiel wird beendet!
            spielaktiv=False

# Aktualisieren des Zustands
    if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
        zustand = zustandsliste[2]
    if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
        zustand = zustandsliste[3]
    if pygame.key.get_pressed()[pygame.locals.K_UP]:
        zustand  = zustandsliste[0]
    if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
        zustand = zustandsliste[1]

# Spiellogik hier integrieren

    eigenschaftenKleinVirus = kleineViren(eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"], eigenschaftenKleinVirus, zustand, virusBilder)

    collisionPruefung(eigenschaftenHauptvirus, eigenschaftenKleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, eigenschaftenHauptvirus, zustand, virenKetteBild)

# Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
    screen.fill((0, 0, 0))  # Black R,G,B
    if zustand != "Nichts" and zustand != "Gameover":
        screen.blit(eigenschaftenKleinVirus["Bild"], (eigenschaftenKleinVirus["PositionX"], eigenschaftenKleinVirus["PositionY"]))
#Hauptvirus zeichnen
    screen.blit(hauptVirus, (eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"]))
# Virenkette zeichnen
    virenIndex = 0
    for anzahlVirus in virenKettePositionX:
        screen.blit(virenKetteBild[virenIndex], (virenKettePositionX[virenIndex], virenKettePositionY[virenIndex]))
        virenIndex += 1

# Fenster aktualisieren
    pygame.display.flip()

# Refresh-Zeiten festlegen
    clock.tick(110)

pygame.quit()
