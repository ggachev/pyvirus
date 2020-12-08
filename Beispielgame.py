# Pygame Beispiel
import os, sys, pygame, pygame.locals, random
#import /Projekt/kleineViren

# Initialisieren von PyGame
pygame.init()

# Fenster öffnen
screenBreite = 1200
screenHoehe = 800

screen =pygame.display.set_mode((screenBreite, screenHoehe))

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

# Hauptvirus Dictionary
eigenschaftenHauptvirus = {
    "PositionX" : 600,
    "PositionY" : 400,
    "Laenge" : 0
}

# Liste mit den letzten 100 Zustaende vom Hauptvirus
zustandsspeicherHauptvirus = []

# Liste fuer die kleine Viren
eigenschaftenKleinVirus = {
    "PositionX" : 0,
    "PositionY" : 0,
    "Zaehler" : 1999,
    "Bild" : 0
}

# Dictionary mit den letzten 100 Zustaenden fuer Virenkette
zustandsspeicherViruskette = {}

# Listen fuer Virenkette
virenKettePositionX = []
virenKettePositionY = []
# aktuelle Zustand
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

#Spielgeschwindigkeit
geschwindigkeit = 0.5
geschwindigkeitsmultiplikator = geschwindigkeit * 200

# Kollisionspruefung
def collisionPruefung(hauptVirus, kleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, zustand, virenKetteBild):
    if not (hauptVirus["PositionX"] >= kleinVirus["PositionX"]+50 or hauptVirus["PositionX"] <= kleinVirus["PositionX"]-50) and not (hauptVirus["PositionY"] >= kleinVirus["PositionY"]+50 or hauptVirus["PositionY"] <= kleinVirus["PositionY"]-50):

        kleinVirus["Zaehler"] = 1999
        if len(virenKettePositionX) == 0:
            if zustand == "Links":
                virenKettePositionX.append(hauptVirus["PositionX"]+50)
                virenKettePositionY.append(hauptVirus["PositionY"])
                virenKetteZustand.append("Links")
            elif zustand == "Rechts":
                virenKettePositionX.append(hauptVirus["PositionX"]-50)
                virenKettePositionY.append(hauptVirus["PositionY"])
                virenKetteZustand.append("Rechts")
            elif zustand == "Oben":
                virenKettePositionX.append(hauptVirus["PositionX"])
                virenKettePositionY.append(hauptVirus["PositionY"]+50)
                virenKetteZustand.append("Oben")
            elif zustand == "Unten":
                virenKettePositionX.append(hauptVirus["PositionX"])
                virenKettePositionY.append(hauptVirus["PositionY"]-50)
                virenKetteZustand.append("Unten")
        else:
            if virenKetteZustand[len(virenKetteZustand)-1] == "Links":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX)-1]+50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY)-1])
                #virenKetteZustand.append("Links")
            elif virenKetteZustand[len(virenKetteZustand)-1] == "Rechts":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1] - 50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1])
                #virenKetteZustand.append("Rechts")
            elif virenKetteZustand[len(virenKetteZustand)-1] == "Oben":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1] + 50)
                #virenKetteZustand.append("Oben")
            elif virenKetteZustand[len(virenKetteZustand)-1] == "Unten":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1] - 50)
                #virenKetteZustand.append("Unten")
            virenKetteZustand.append(zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][(100)/geschwindigkeitsmultiplikator])
        virenKetteBild.append(kleinVirus["Bild"])
        zustandsspeicherViruskette[hauptVirus["Laenge"]] = []
        hauptVirus["Laenge"] += 1

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

    # Aktualisieren des Zustands vom Hauptvirus
    if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
        if (zustand != zustandsliste[3]) or eigenschaftenHauptvirus["Laenge"] == 0:
            zustand = zustandsliste[2]
    if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
        if (zustand != zustandsliste[2]) or eigenschaftenHauptvirus["Laenge"] == 0:
            zustand = zustandsliste[3]
    if pygame.key.get_pressed()[pygame.locals.K_UP]:
        if (zustand != zustandsliste[1]) or eigenschaftenHauptvirus["Laenge"] == 0:
            zustand = zustandsliste[0]
    if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
        if (zustand != zustandsliste[0]) or eigenschaftenHauptvirus["Laenge"] == 0:
            zustand = zustandsliste[1]

    # Zustandsspeicher vom Hauptvirus aktualisieren
    zustandsspeicherHauptvirus.insert(0, zustand)
    if len(zustandsspeicherHauptvirus) == 101:
        zustandsspeicherHauptvirus.pop()

    # Prüfung, in welche Richtung sich der Spieler automatisch nach vorne bewegen soll.

    if zustand == zustandsliste[0]:
        if eigenschaftenHauptvirus["PositionY"] > 0:
            eigenschaftenHauptvirus["PositionY"] -= geschwindigkeit
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[1]:
        if eigenschaftenHauptvirus["PositionY"] < 750: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionY"] += geschwindigkeit
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[2]:
        if eigenschaftenHauptvirus["PositionX"] > 0:
            eigenschaftenHauptvirus["PositionX"] -= geschwindigkeit
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    elif zustand == zustandsliste[3]:
        if eigenschaftenHauptvirus["PositionX"] < 1150: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionX"] += geschwindigkeit
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])
    # Zuruecksetzen der Zustand, wenn der Rand getroffen wurde
    elif zustand == zustandsliste[5]:
        eigenschaftenHauptvirus["PositionX"] = 600
        eigenschaftenHauptvirus["PositionY"] = 400
        eigenschaftenHauptvirus["Laenge"] = 0
        virenKettePositionX = []
        virenKettePositionY = []
        virenKetteZustand = []
        virenKetteBild = []
        zustandsspeicherViruskette = {}
        zustandsspeicherHauptvirus = []

    # Spiellogik hier integrieren

    eigenschaftenKleinVirus = kleineViren(eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"], eigenschaftenKleinVirus, zustand, virusBilder)

    collisionPruefung(eigenschaftenHauptvirus, eigenschaftenKleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, zustand, virenKetteBild)

    # Zustandsspeicher von kleine Viren aktualisieren
    if len(virenKetteZustand) >= 1:
        for virusnummer in zustandsspeicherViruskette:
            print(virusnummer)
            zustandsspeicherViruskette[virusnummer].insert(0, virenKetteZustand[virusnummer])
            print(virusnummer)
            if len(zustandsspeicherViruskette[virusnummer]) == 101:
                zustandsspeicherViruskette[virusnummer].pop()

    # Aktualisieren des Zustands von der Viruskette
    listenIndex = 0
    for virusnummer in virenKetteZustand:
        if listenIndex == 0:
            virenKetteZustand[listenIndex] = zustandsspeicherHauptvirus[49]
        else:
            virenKetteZustand[listenIndex] = zustandsspeicherViruskette[listenIndex - 1][49]
        listenIndex += 1

    #Bewegung der Viruskette
    virenIndex = 0
    for anzahlVirus in virenKettePositionX:
        if virenIndex == 0:
            if zustandsspeicherHauptvirus[49] == "Oben":
                virenKettePositionY[virenIndex] -= geschwindigkeit
            elif zustandsspeicherHauptvirus[49] == "Unten":
                virenKettePositionY[virenIndex] += geschwindigkeit
            elif zustandsspeicherHauptvirus[49] == "Links":
                virenKettePositionX[virenIndex] -= geschwindigkeit
            elif zustandsspeicherHauptvirus[49] == "Rechts":
                virenKettePositionX[virenIndex] += geschwindigkeit
        else:
            if virenKetteZustand[virenIndex] == "Oben":
                virenKettePositionY[virenIndex] -= geschwindigkeit
            elif virenKetteZustand[virenIndex] == "Unten":
                virenKettePositionY[virenIndex] += geschwindigkeit
            elif virenKetteZustand[virenIndex] == "Links":
                virenKettePositionX[virenIndex] -= geschwindigkeit
            elif virenKetteZustand[virenIndex] == "Rechts":
                virenKettePositionX[virenIndex] += geschwindigkeit
        virenIndex += 1

    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            # Spiel wird beendet!
            spielaktiv=False

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
    clock.tick(100)

pygame.quit()
