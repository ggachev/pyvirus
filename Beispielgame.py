# Pygame Bibliotheken importieren
import pygame.locals
import random
import time

# Initialisieren von PyGame
pygame.init()

# Fenster öffnen
screenBreite = 1200
screenHoehe = 800

screen = pygame.display.set_mode((screenBreite, screenHoehe))

# Titel für Fensterkopf
pygame.display.set_caption('PyVirus')

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Liste für Zustände für die Richtungen des Virus + Variable, der immer ein Zustand zugeordnet wird
zustandsliste = ["Oben", "Unten", "Links", "Rechts", "Nichts", "Gameover"]
# Startzustand in der Variable auf Nichts setzen
zustand = zustandsliste[4]

# Hauptvirus Dictionary
# enthaelt die Postionen X und Y vom Hauptvirus sowie die Laenge
eigenschaftenHauptvirus = {
    "PositionX": 600,
    "PositionY": 400,
    "Laenge": 0
}

# Liste mit den letzten 100 Zustaende vom Hauptvirus
# dort wird der aktuelle Zustand an der ersten Position hinzugefuegt
zustandsspeicherHauptvirus = []

# Dictionary fuer die Viren, die gespawned werden
# enthaelt die Positionen X und Y, Zaehler und das Bild
eigenschaftenKleinVirus = {
    "PositionX": 0,
    "PositionY": 0,
    "Zaehler": 1999,
    "Bild": 0
}

#Der Score wird aus einer Textdatei gelesen
scoreDatei = open("Score.txt")
score = scoreDatei.readline()
scoreDatei.close()

# Dictionary mit den letzten 100 Zustaenden fuer Virenkette
# Dictionary wird gebraucht, um Zustandslisten fuer jeden angehaengten Virus zu speichern
zustandsspeicherViruskette = {}

# Dictionary fuer Virenkette
# An jeweils der erste Stelle stehen die Elemente, die zu dem ersten Virus der Kette gehoeren, an der zweiten die vom zweiten...
virenKette = {
    "virenKettePositionX": [],
    "virenKettePositionY": [],
# aktuelle Zustand
    "virenKetteZustand": [],
    "virenKetteBild": []

}

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
virusBilderold = [virusRot, virusOrange, virusGelb, virusGruen, virusBlau, virusLila, virusPink, virusGrau]
virusBilder = []

# Virenbilder auf 50x50 verkleinern
for Bild in virusBilderold:
    Bild = pygame.transform.scale(Bild, (50, 50))
    virusBilder.append(Bild)

# Startgeschwindigkeit des Virus festlegen
# Pixelaenderung bestimmt den Wert um wie viele Pixel sich der Virus bewegen soll und das ist abhaengig von der Geschwindigkeit
# Die Geschwindigkeit soll immer ein Teiler von 100 ohne Rest sein
# zustandsanzahl berechnet wie viele Zustaende bei unterschiedlicher Geschwindigkeit betrachtet werden muessen und gibt das Ergebniss als Integer aus
geschwindigkeit = 4
pixelaenderung = geschwindigkeit/2
zustandsanzahl = int((100 / geschwindigkeit) - 1)

# Kollisionspruefung
# Zunaechst wird geprueft ob eine Kollision mit einem kleinen Virus stattfindet, wenn das der Fall ist wird berechnet an
# welcher Position der Virus angehaengt wird und in welche Richtung er sich bewegen soll
def collisionPruefung(hauptVirus, kleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, zustand, virenKetteBild, zustandsanzahl):
    if not (hauptVirus["PositionX"] >= kleinVirus["PositionX"]+50 or hauptVirus["PositionX"] <= kleinVirus["PositionX"]-50) and not (hauptVirus["PositionY"] >= kleinVirus["PositionY"]+50 or hauptVirus["PositionY"] <= kleinVirus["PositionY"]-50):
# Bei einer Kollision soll direkt eine neue Position ermittelt werden und deshalb wird der Zaehler auf 1999 gesetzt
# Der obere Block ist fuer das Anhaengen des ersten Virus an den Hauptvirus
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
# Der untere Block ist fuer das Anhaengen der weiteren Viren an den letzten Virus der Kette
        else:
            if zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][zustandsanzahl] == "Links":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX)-1] + 50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY)-1])
            elif zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][zustandsanzahl] == "Rechts":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1] - 50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1])
            elif zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][zustandsanzahl] == "Oben":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1] + 50)
            elif zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][zustandsanzahl] == "Unten":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKette["virenKettePositionY"]) - 1] - 50)
            virenKetteZustand.append(zustandsspeicherViruskette[hauptVirus["Laenge"] - 1][zustandsanzahl])
# Das Bild von dem erstellten klein Virus wird zur Liste mit den Bildern hinzugefuegt
        virenKetteBild.append(kleinVirus["Bild"])
# neue Liste in Dictionary der Viruskette zum Speichern der Zustaende vom neuen Virus erstellt
        zustandsspeicherViruskette[hauptVirus["Laenge"]] = []
        hauptVirus["Laenge"] += 1

# Funktion fuer kleine Viren
# es wird eine zufaellige Postion(X, Y) und ein zufaelliges Bild ermittelt
# Die Position von dem kleinen Virus wird alle 2000 Durchlaeufe neu berechnet
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
# Es wird gepruft, ob der Zustand nicht Gameover ist und eine Pfeiltaste gedrueckt wird
    if zustand != zustandsliste[5]:
        if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                zustand = zustandsliste[2]
            elif virenKette["virenKetteZustand"][0] != "Rechts":
                zustand = zustandsliste[2]
        elif pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                zustand = zustandsliste[3]
            elif virenKette["virenKetteZustand"][0] != "Links":
                zustand = zustandsliste[3]
        elif pygame.key.get_pressed()[pygame.locals.K_UP]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                zustand = zustandsliste[0]
            elif virenKette["virenKetteZustand"][0] != "Unten":
                zustand = zustandsliste[0]
        elif pygame.key.get_pressed()[pygame.locals.K_DOWN]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                zustand = zustandsliste[1]
            elif virenKette["virenKetteZustand"][0] != "Oben":
                zustand = zustandsliste[1]

# Zustandsspeicher vom Hauptvirus aktualisieren
# An der erste Stelle von zustandsspeicherHauptvirus wird der aktuelle Zustand gespeichert
# Wenn die Zustaende ueber 100 sind, wird der letzte geloescht
    zustandsspeicherHauptvirus.insert(0, zustand)
    if len(zustandsspeicherHauptvirus) == 101:
        zustandsspeicherHauptvirus.pop()
# Wenn der erste Kleinvirus angehaengt wird, soll er zunaechst zustandsanzahl-mal die aktuelle Richtung von Hauptvirus uebernehmen
    if eigenschaftenHauptvirus["Laenge"] == 0:
        listenIndex = 0
        for zustandsposition in zustandsspeicherHauptvirus:
            zustandsspeicherHauptvirus[listenIndex] = zustand
            listenIndex += 1

# Prüfung, in welche Richtung sich der Spieler automatisch nach vorne bewegen soll.
# Wenn die Richtung ausserhalb des Spielfelds ist, dann wird der Zustand auf Gameover gesetzt
    if zustand == zustandsliste[0]:
        if eigenschaftenHauptvirus["PositionY"] > 0:
            eigenschaftenHauptvirus["PositionY"] -= pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)

    elif zustand == zustandsliste[1]:
        if eigenschaftenHauptvirus["PositionY"] < screenHoehe - 50: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionY"] += pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)

    elif zustand == zustandsliste[2]:
        if eigenschaftenHauptvirus["PositionX"] > 0:
            eigenschaftenHauptvirus["PositionX"] -= pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)

    elif zustand == zustandsliste[3]:
        if eigenschaftenHauptvirus["PositionX"] < screenBreite - 50: # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionX"] += pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)

# Zuruecksetzen aller Zustaende, wenn der Rand getroffen wurde
    elif zustand == zustandsliste[5]:
        zustand = zustandsliste[4]
        eigenschaftenHauptvirus["PositionX"] = 600
        eigenschaftenHauptvirus["PositionY"] = 400
        eigenschaftenHauptvirus["Laenge"] = 0
        virenKette["virenKettePositionX"] = []
        virenKette["virenKettePositionY"] = []
        virenKette["virenKetteZustand"] = []
        virenKette["virenKetteBild"] = []
        zustandsspeicherViruskette = {}
        zustandsspeicherHauptvirus = []
# Idee von: https://docs.python.org/3/library/time.html?highlight=time%20sleep#time.sleep
        time.sleep(1)

# Kollisionspruefung mit der Virenkette
# Die Durchlaeufe sind von der Laenge des Virus abhaengig
    listenIndex = 0
    for position in virenKette["virenKettePositionX"]:
        if listenIndex >= 1 and zustand != zustandsliste[5]:
            if not (eigenschaftenHauptvirus["PositionX"] >= virenKette["virenKettePositionX"][listenIndex] + 50 or eigenschaftenHauptvirus["PositionX"] <= virenKette["virenKettePositionX"][listenIndex] - 50) and not (eigenschaftenHauptvirus["PositionY"] >= virenKette["virenKettePositionY"][listenIndex] + 50 or eigenschaftenHauptvirus["PositionY"] <= virenKette["virenKettePositionY"][listenIndex] - 50):
                zustand = zustandsliste[5]
                print(zustand)
        listenIndex += 1



# Spiellogik ist hier integriert
    eigenschaftenKleinVirus = kleineViren(eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"], eigenschaftenKleinVirus, zustand, virusBilder)

    collisionPruefung(eigenschaftenHauptvirus, eigenschaftenKleinVirus, virenKette["virenKettePositionX"], virenKette["virenKettePositionY"], virenKette["virenKetteZustand"], zustand, virenKette["virenKetteBild"], zustandsanzahl)

# Zustandsspeicher von Virenkette aktualisieren
# Wird nur gemacht, wenn mindestens 1 Virus angehaengt ist
# Logik ist analog zu Hauptvirus
    if len(virenKette["virenKetteZustand"]) >= 1:
        for virusnummer in zustandsspeicherViruskette:
            zustandsspeicherViruskette[virusnummer].insert(0, virenKette["virenKetteZustand"][virusnummer])
            if len(zustandsspeicherViruskette[virusnummer]) == (101):
                zustandsspeicherViruskette[virusnummer].pop()
        listenIndex = 0
        for zustandsposition in zustandsspeicherViruskette[eigenschaftenHauptvirus["Laenge"] - 1]:
            zustandsspeicherViruskette[eigenschaftenHauptvirus["Laenge"] - 1][listenIndex] = virenKette["virenKetteZustand"][len(virenKette["virenKetteZustand"]) - 1]
            listenIndex += 1

# Aktualisieren des aktuellen Zustands von der Viruskette
# Logik ist analog zu Hauptvirus
    listenIndex = 0
    for virusnummer in virenKette["virenKetteZustand"]:
        if listenIndex == 0:
            virenKette["virenKetteZustand"][listenIndex] = zustandsspeicherHauptvirus[zustandsanzahl]
        else:
            virenKette["virenKetteZustand"][listenIndex] = zustandsspeicherViruskette[listenIndex - 1][zustandsanzahl]
        listenIndex += 1

# Bewegung der Viruskette
# Logik ist analog zu Hauptvirus
# Verzoegerung mit Hilfe des Zustandsspeichers
    virenIndex = 0
    for anzahlVirus in virenKette["virenKettePositionX"]:
        if virenIndex == 0:
            if zustandsspeicherHauptvirus[zustandsanzahl] == "Oben":
                virenKette["virenKettePositionY"][virenIndex] -= pixelaenderung
            elif zustandsspeicherHauptvirus[zustandsanzahl] == "Unten":
                virenKette["virenKettePositionY"][virenIndex] += pixelaenderung
            elif zustandsspeicherHauptvirus[zustandsanzahl] == "Links":
                virenKette["virenKettePositionX"][virenIndex] -= pixelaenderung
            elif zustandsspeicherHauptvirus[zustandsanzahl] == "Rechts":
                virenKette["virenKettePositionX"][virenIndex] += pixelaenderung
        else:
            if virenKette["virenKetteZustand"][virenIndex] == "Oben":
                virenKette["virenKettePositionY"][virenIndex] -= pixelaenderung
            elif virenKette["virenKetteZustand"][virenIndex] == "Unten":
                virenKette["virenKettePositionY"][virenIndex] += pixelaenderung
            elif virenKette["virenKetteZustand"][virenIndex] == "Links":
                virenKette["virenKettePositionX"][virenIndex] -= pixelaenderung
            elif virenKette["virenKetteZustand"][virenIndex] == "Rechts":
                virenKette["virenKettePositionX"][virenIndex] += pixelaenderung
        virenIndex += 1

# Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
# Spiel wird beendet!
            spielaktiv=False

# Speilfeld loeschen
    screen.fill((0, 0, 0))  # Black R,G,B
# Kleinvirus zeichnen
    if zustand != "Nichts" and zustand != "Gameover":
        screen.blit(eigenschaftenKleinVirus["Bild"], (eigenschaftenKleinVirus["PositionX"], eigenschaftenKleinVirus["PositionY"]))
# Hauptvirus zeichnen
    screen.blit(hauptVirus, (eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"]))
# Virenkette zeichnen
    virenIndex = 0
    for anzahlVirus in virenKette["virenKettePositionX"]:
        screen.blit(virenKette["virenKetteBild"][virenIndex], (virenKette["virenKettePositionX"][virenIndex], virenKette["virenKettePositionY"][virenIndex]))
        virenIndex += 1

# Fenster aktualisieren
    pygame.display.flip()

# Refresh-Zeiten festlegen
    clock.tick(100)

pygame.quit()
