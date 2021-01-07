# Pygame Bibliotheken importieren
import random
import time
import pygame.locals
# Um pygame menu zu installieren: python -m pip install pygame-menu
import pygame_menu

# Initialisieren von PyGame und Schrift
pygame.init()

# Schriftart festlegen
# https://www.wfonts.com/font/comic-sans-ms
schriftart = pygame.font.Font("comici.ttf", 30)

# Fenster öffnen
screenBreite = 1212
screenHoehe = 812

screen = pygame.display.set_mode((screenBreite, screenHoehe))

# Titel für Fensterkopf
pygame.display.set_caption('PyVirus')

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

#Quelle:https://pythonprogramming.net/displaying-text-pygame-screen/
#Text nach Game
def textObjekt(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def textDisplay(text):
    font = pygame.font.Font('comici.ttf', 90)
    TextSurf, TextRect = textObjekt(text, font)
    TextRect.center = ((screenBreite/2), (screenHoehe/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)



# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Liste für Zustände für die Richtungen des Virus + Variable, der immer ein Zustand zugeordnet wird
zustandsliste = ["Oben", "Unten", "Links", "Rechts", "Nichts", "Gameover"]
# Startzustand in der Variable auf Nichts setzen
zustand = zustandsliste[4]

# Hauptvirus Dictionary
# enthaelt die Postionen X und Y vom Hauptvirus sowie die Laenge
eigenschaftenHauptvirus = {
    "PositionX": 606,
    "PositionY": 406,
    "Laenge": 0,
    "NaechsterZustand": "Nichts"
}

# Dictionary fuer die Viren, die gespawned werden
# enthaelt die Positionen X und Y, Zaehler und das Bild
eigenschaftenKleinVirus = {
    "PositionX": 0,
    "PositionY": 0,
    "Zaehler": 1999,
    "Bild": 0
}

# Der Score wird aus einer Textdatei gelesen
scoreDatei = open("Score.txt")
highscore = scoreDatei.readline()
scoreDatei.close()

# Dictionary fuer Virenkette
# An jeweils der erste Stelle stehen die Elemente, die zu dem ersten Virus der Kette gehoeren, an der zweiten die vom zweiten...
virenKette = {
    "virenKettePositionX": [],
    "virenKettePositionY": [],
    # aktuelle Zustand
    "virenKetteZustand": [],
    "virenKetteBild": [],
    "virenKetteBildRichtung": [],
    "NaechsterZustand" : []
}

# Virus Bilder - Idee von https://pythonprogramming.net/displaying-images-pygame/
hauptVirus = pygame.image.load('rsz_kleineviren1.png')
# Bild verkleinern https://stackoverflow.com/questions/43046376/how-to-change-an-image-size-in-pygame/43053791
hauptVirus = pygame.transform.scale(hauptVirus, (50, 50))
hauptVirusRichtung = 0

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

# Bilder Zusatzobjkte (Maske/ Spritze) 27.12.20
# https://icon-icons.com/de/symbol/virus-covid19-corona-Maske-Gesicht/141777
Maske = pygame.image.load('Maske.png')
Maske = pygame.transform.scale(Maske, (50, 50))

# Variable fuer Maske
maskeAktiv = False

# Variable fuer Impfung
spritzeAktiv = False

# Variable fuer Schwierigkeitsgrad
schwierigkeitsgradAktiv = False

# https://icons8.de/icon/52583/spritze
Spritze = pygame.image.load('Spritze.png')
Spritze = pygame.transform.scale(Spritze, (50, 50))

# Dictionary fuer die Maske, die gespawned wird
# enthaelt die Positionen X und Y, Zaehler und das Bild
eigenschaftenMaske = {
    "PositionX": 0,
    "PositionY": 0,
    "MaskeZaehler": 4999,
    "Bild": Maske,
    "maskeAktivZaehler": 0
}
# Dictionary fuer die Spritze , die gespawned wird
# enthaelt die Positionen X und Y, Zaehler und das Bild
eigenschaftenSpritze = {
    "PositionX": 0,
    "PositionY": 0,
    "SpritzeZaehler": 3999,
    "Bild": Spritze
}

# Startgeschwindigkeit des Virus festlegen
# Pixelaenderung bestimmt den Wert um wie viele Pixel sich der Virus bewegen soll und das ist abhaengig von der Geschwindigkeit
# Die Geschwindigkeit soll immer ein Teiler von 100 ohne Rest sein
# zustandsanzahl berechnet wie viele Zustaende bei unterschiedlicher Geschwindigkeit betrachtet werden muessen und gibt das Ergebniss als Integer aus
geschwindigkeit = 4
pixelaenderung = geschwindigkeit / 2

# Variable um den Randuebergehen zu aktivieren bzw. deaktivieren
randaktiv = True

# Menue Logik, es wurde ein Library pygame_menu benutzt
# https://pygame-menu.readthedocs.io/en/latest/index.html
def name_aendern(wert):
    print(wert)

def setze_schwierigkeitsgrad(wert, schwierigkeitsgrad):
    global schwierigkeitsgradAktiv
    if schwierigkeitsgrad == 1:
        schwierigkeitsgradAktiv = False
    if schwierigkeitsgrad == 2:
        schwierigkeitsgradAktiv = True
    return schwierigkeitsgradAktiv

def setze_rand(wert, x):
    global randaktiv
    if x == 1:
        randaktiv = True
    if x == 2:
        randaktiv = False
    return randaktiv

def spiel_starten():
    menu.disable()

# Es wird ein Menue erstellt mit Groesse 300x600
menu = pygame_menu.Menu(400, 600, 'Willkommen', theme=pygame_menu.themes.THEME_DARK)

menu.add_text_input('Name: ', default='Max Weiss', onchange=name_aendern)
menu.add_selector('Schwierigkeitsgrad: ', [('Leicht', 1), ('Schwer', 2)], onchange=setze_schwierigkeitsgrad)
menu.add_selector('Randuebergang: ', [('Aktiv', 1), ('Inaktiv', 2)], onchange=setze_rand)
menu.add_button('Spielen', spiel_starten)
menu.add_button('Spiel beenden', pygame_menu.events.EXIT)
# Das Menue wird hier zum Ersten mal gestartet
menu.mainloop(screen)

# Kollisionspruefung
# Zunaechst wird geprueft ob eine Kollision mit einem kleinen Virus stattfindet, wenn das der Fall ist wird berechnet an
# welcher Position der Virus angehaengt wird und in welche Richtung er sich bewegen soll
def collisionPruefung(hauptVirus, kleinVirus, virenKettePositionX, virenKettePositionY, virenKetteZustand, zustand, virenKetteBild, virenKetteNaechsterZustand):
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
            virenKetteNaechsterZustand.append(zustand)

# Der untere Block ist fuer das Anhaengen der weiteren Viren an den letzten Virus der Kette
        else:
            if virenKette["virenKetteZustand"][len(virenKette["virenKetteZustand"])-1] == "Links":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX)-1] + 50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY)-1])
            elif virenKette["virenKetteZustand"][len(virenKette["virenKetteZustand"])-1] == "Rechts":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1] - 50)
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1])
            elif virenKette["virenKetteZustand"][len(virenKette["virenKetteZustand"])-1] == "Oben":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKettePositionY) - 1] + 50)
            elif virenKette["virenKetteZustand"][len(virenKette["virenKetteZustand"])-1] == "Unten":
                virenKettePositionX.append(virenKettePositionX[len(virenKettePositionX) - 1])
                virenKettePositionY.append(virenKettePositionY[len(virenKette["virenKettePositionY"]) - 1] - 50)
            virenKetteZustand.append(virenKetteZustand[len(virenKetteZustand) - 1])
            virenKetteNaechsterZustand.append(virenKetteZustand[len(virenKetteZustand) - 2])
# Das Bild von dem erstellten klein Virus wird zur Liste mit den Bildern hinzugefuegt
        virenKetteBild.append(kleinVirus["Bild"])
        hauptVirus["Laenge"] += 1

# Zunaechst wird geprueft ob eine Kollision mit der Maske/ Spritze stattfindet
def collisionPruefungMaske(hauptVirus, eigenschaftenMaske, maskeAktiv):
    if not (hauptVirus["PositionX"] >= eigenschaftenMaske["PositionX"] + 50 or hauptVirus["PositionX"] <= eigenschaftenMaske["PositionX"] - 50) and not (hauptVirus["PositionY"] >= eigenschaftenMaske["PositionY"] + 50 or hauptVirus["PositionY"] <= eigenschaftenMaske["PositionY"] - 50):
        eigenschaftenMaske["MaskeZaehler"] = 0
        maskeAktiv = True
        eigenschaftenMaske["PositionX"] = -1
    return maskeAktiv

def collisionPruefungSpritze(hauptVirus, eigenschaftenSpritze, spritzeAktiv, maskeAktiv, virenKette, zustand, schwierigkeitsgradAktiv):
    if not (hauptVirus["PositionX"] >= eigenschaftenSpritze["PositionX"] + 50 or hauptVirus["PositionX"] <= eigenschaftenSpritze["PositionX"] - 50) and not (hauptVirus["PositionY"] >= eigenschaftenSpritze["PositionY"] + 50 or hauptVirus["PositionY"] <= eigenschaftenSpritze["PositionY"] - 50):
        eigenschaftenSpritze["SpritzeZaehler"] = 3999
        if not maskeAktiv:
            if schwierigkeitsgradAktiv:
                gameOver(zustand, eigenschaftenHauptvirus, virenKette, geschwindigkeit, highscore, maskeAktiv)
            else:
                hauptVirus["Laenge"] = int(hauptVirus["Laenge"]/2)
                while hauptVirus["Laenge"] != len(virenKette["virenKetteZustand"]):
                    virenKette["virenKetteZustand"].pop()
                    virenKette["virenKettePositionX"].pop()
                    virenKette["virenKettePositionY"].pop()
                    virenKette["virenKetteBild"].pop()
                    virenKette["NaechsterZustand"].pop()

    return spritzeAktiv

# Funktion fuer kleine Viren
# es wird eine zufaellige Postion(X, Y) und ein zufaelliges Bild ermittelt
# Die Position von dem kleinen Virus wird alle 2000 Durchlaeufe neu berechnet
# Die Parameter x und y liefern die aktuelle Position von dem Hauptvirus
def kleineViren(x, y, eigenschaftenKleinVirus, virusBilder, virenKette):
    z = eigenschaftenKleinVirus["Zaehler"]
    z += 1

    if z == 2000:
        # Es wird geprueft, ob das Bild gleich wie das vorherige ist und wenn das der Fall ist, wird neues Bild zufaellig erstellt
        virenbildgleich = True

        while virenbildgleich:
            randomvirus = random.randrange(0, 7)
            randomvirus = virusBilder[randomvirus]
            if eigenschaftenKleinVirus["Bild"] != randomvirus:
                virenbildgleich = False
        eigenschaftenKleinVirus["Bild"] = randomvirus

        # Kollisionspruefung und Erstellungs die neue Koordinaten fuer kleinVirus
        position = False

        while not position:
            position = True
            randomx = random.randrange(3, 1159)
            randomy = random.randrange(3, 759)

            if not ((randomx >= x + 200 or randomx <= x - 200) and (randomy >= y + 200 or randomy <= y - 200)):
                position = False
            listenIndex = 0
            for Position in virenKette["virenKettePositionX"]:
                if ((randomx <= virenKette["virenKettePositionX"][listenIndex] + 50 and randomx >=
                     virenKette["virenKettePositionX"][listenIndex] - 50) and (
                        randomy <= virenKette["virenKettePositionY"][listenIndex] + 50 and randomy >=
                        virenKette["virenKettePositionY"][listenIndex] - 50)):
                    position = False
                listenIndex += 1
        eigenschaftenKleinVirus["PositionX"] = randomx
        eigenschaftenKleinVirus["PositionY"] = randomy

        z = 0

    eigenschaftenKleinVirus["Zaehler"] = z
    return eigenschaftenKleinVirus

# Funktion für die Maske (Analog zu der Funktion kleineViren)
# es wird eine zufaellige Postion(X, Y) mit dem Bild der Maske
# Die Position der Maske wird alle 5000 Durchlaeufe neu berechnet
def zusatzObjektMaske(eigenschaftenMaske, x, y):
    z = eigenschaftenMaske["MaskeZaehler"]
    z += 1
    if z == 5000:

        position = False

        while not position:
            position = True

            randomx = random.randrange(3, 1159)
            randomy = random.randrange(3, 759)
            eigenschaftenMaske["Bild"] = Maske
            if not ((randomx >= x + 200 or randomx <= x - 200) and (randomy >= y + 200 or randomy <= y - 200)):
                position = False
            listenIndex = 0
            for Position in virenKette["virenKettePositionX"]:
                if ((randomx <= virenKette["virenKettePositionX"][listenIndex] + 50 and randomx >=
                     virenKette["virenKettePositionX"][listenIndex] - 50) and (
                        randomy <= virenKette["virenKettePositionY"][listenIndex] + 50 and randomy >=
                        virenKette["virenKettePositionY"][listenIndex] - 50)):
                    position = False
                listenIndex += 1
        eigenschaftenMaske["PositionX"] = randomx
        eigenschaftenMaske["PositionY"] = randomy
        z = 0
    eigenschaftenMaske["MaskeZaehler"] = z
    return eigenschaftenMaske

# Funktion für die Spritze (Analog zu der Funktion kleineViren)
# es wird eine zufaellige Postion(X, Y) mit dem Bild der Spritze
# Die Position der Spritze wird alle 4000 Durchlaeufe neu berechnet
def zusatzObjektSpritze(eigenschaftenSpritze, x, y):
    z = eigenschaftenSpritze["SpritzeZaehler"]
    z += 1
    if z == 4000:
        position = False

        while not position:
            position = True

            randomx = random.randrange(3, 1159)
            randomy = random.randrange(3, 759)
            if not ((randomx >= x + 200 or randomx <= x - 200) and (randomy >= y + 200 or randomy <= y - 200)):
                position = False
            listenIndex = 0
            for Position in virenKette["virenKettePositionX"]:
                if ((randomx <= virenKette["virenKettePositionX"][listenIndex] + 50 and randomx >=
                     virenKette["virenKettePositionX"][listenIndex] - 50) and (
                        randomy <= virenKette["virenKettePositionY"][listenIndex] + 50 and randomy >=
                        virenKette["virenKettePositionY"][listenIndex] - 50)):
                    position = False
                listenIndex += 1
        eigenschaftenSpritze["PositionX"] = randomx
        eigenschaftenSpritze["PositionY"] = randomy
        z = 0
    eigenschaftenSpritze["SpritzeZaehler"] = z
    return eigenschaftenSpritze

def gameOver(zustand, eigenschaftenHauptvirus, virenKette, geschwindigkeit, highscore, maskeAktiv):
    zustand = zustandsliste[4]
    # Quelle: https://www.youtube.com/watch?v=XJSnaeOcnVs
    # Score Update
    if int(eigenschaftenHauptvirus["Laenge"]) > int(highscore):
        highscore = eigenschaftenHauptvirus["Laenge"]
        textDisplay('New Highscore:' + 'Name ' + str(highscore))
        scoreDatei = open("Score.txt", "w")
        highscore = scoreDatei.write(str(highscore))
        scoreDatei.close()

        scoreDatei = open("Score.txt", "r")
        highscore = scoreDatei.readline()
        scoreDatei.close()

    else:
        textDisplay('GAME OVER')

    eigenschaftenHauptvirus["PositionX"] = 606
    eigenschaftenHauptvirus["PositionY"] = 406
    eigenschaftenHauptvirus["Laenge"] = 0
    virenKette["virenKettePositionX"] = []
    virenKette["virenKettePositionY"] = []
    virenKette["virenKetteZustand"] = []
    virenKette["virenKetteBild"] = []
    virenKette["NaechsterZustand"] = []
    eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[4]
    maskeAktiv = False
    eigenschaftenMaske["MaskeZaehler"] = 4999
    eigenschaftenSpritze["SpritzeZaehler"] = 3999
    geschwindigkeit = 1


# Schleife Hauptprogramm
while spielaktiv:

    # Aktualisieren des Zustands vom Hauptvirus
    # Es wird gepruft, ob der Zustand nicht Gameover ist und eine Pfeiltaste gedrueckt wird
    if zustand != zustandsliste[5]:
        if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[2]
            elif zustand != "Rechts":
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[2]
        elif pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[3]
            elif zustand != "Links":
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[3]
        elif pygame.key.get_pressed()[pygame.locals.K_UP]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[0]
            elif zustand != "Unten":
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[0]
        elif pygame.key.get_pressed()[pygame.locals.K_DOWN]:
            if eigenschaftenHauptvirus["Laenge"] == 0:
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[1]
            elif zustand != "Oben":
                eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[1]

# Alle 50 Pixel

    if eigenschaftenHauptvirus["PositionX"] % 50 == 6 and eigenschaftenHauptvirus["PositionY"] % 50 == 6:
        zustand = eigenschaftenHauptvirus["NaechsterZustand"]

# Geschwindigkeitsanpassung
        if eigenschaftenHauptvirus["Laenge"] >= 100:
            geschwindigkeit = 10
        elif eigenschaftenHauptvirus["Laenge"] >= 50:
            geschwindigkeit = 5
        elif eigenschaftenHauptvirus["Laenge"] >= 0:
            geschwindigkeit = 4
        elif eigenschaftenHauptvirus["Laenge"] >= 5:
            geschwindigkeit = 2.5
        elif eigenschaftenHauptvirus["Laenge"] >= 1:
            geschwindigkeit = 2
        elif eigenschaftenHauptvirus["Laenge"] >= 0:
            geschwindigkeit = 1
        pixelaenderung = geschwindigkeit / 2

# Aktualisieren des aktuellen Zustands und nächsten Zustands von der Viruskette alle 50 Pixel nach der Aenderung des Hauptvirus, aber vor der Bewegung
        listenIndex = 0
        for virusnummer in virenKette["virenKetteZustand"]:
            virenKette["virenKetteZustand"][listenIndex] = virenKette["NaechsterZustand"][listenIndex]
            listenIndex += 1
        listenIndex = 0
        for virusnummer in virenKette["NaechsterZustand"]:
            if listenIndex == 0:
                virenKette["NaechsterZustand"][listenIndex] = zustand
            else:
                virenKette["NaechsterZustand"][listenIndex] = virenKette["virenKetteZustand"][listenIndex - 1]
            listenIndex += 1

# Prüfung, in welche Richtung sich der Spieler automatisch nach vorne bewegen soll.
# Wenn die Richtung ausserhalb des Spielfelds ist, dann wird der Zustand auf Gameover gesetzt
# Wenn die Raender aktiv sind werden die Raender auch beruecksichtigt
# Nach Oben
    if zustand == zustandsliste[0]:
        if randaktiv:
            if eigenschaftenHauptvirus["PositionY"] > 5 or (
                    eigenschaftenHauptvirus["PositionX"] > 755 and eigenschaftenHauptvirus[
                "PositionX"] < 807):  # > 5 wegen dem Rand
                eigenschaftenHauptvirus["PositionY"] -= pixelaenderung
                if eigenschaftenHauptvirus["PositionY"] < -43:
                    eigenschaftenHauptvirus["PositionX"] = 256
                    eigenschaftenHauptvirus["PositionY"] = screenHoehe-6
            else:
                zustand = zustandsliste[5]
                print(zustand)
        elif eigenschaftenHauptvirus["PositionY"] > 5:
            eigenschaftenHauptvirus["PositionY"] -= pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)
    # Nach Unten
    elif zustand == zustandsliste[1]:
        if randaktiv:
            if eigenschaftenHauptvirus["PositionY"] < screenHoehe-6 - 55 or (
                    eigenschaftenHauptvirus["PositionX"] > 255 and eigenschaftenHauptvirus[
                "PositionX"] < 356):  # 55 abziehen, wegen Objektlaenge+Rand
                eigenschaftenHauptvirus["PositionY"] += pixelaenderung
                if eigenschaftenHauptvirus["PositionY"] > screenHoehe-5:
                    eigenschaftenHauptvirus["PositionX"] = 756
                    eigenschaftenHauptvirus["PositionY"] = -43
            else:
                zustand = zustandsliste[5]
                print(zustand)
        elif eigenschaftenHauptvirus["PositionY"] < screenHoehe - 55:
            eigenschaftenHauptvirus["PositionY"] += pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)
    # Nach Links
    elif zustand == zustandsliste[2]:
        if randaktiv:
            if eigenschaftenHauptvirus["PositionX"] > 5 or (
                    eigenschaftenHauptvirus["PositionY"] > 155 and eigenschaftenHauptvirus[
                "PositionY"] < 256):  # > 5 wegen dem Rand
                eigenschaftenHauptvirus["PositionX"] -= pixelaenderung
                if eigenschaftenHauptvirus["PositionX"] < -43:
                    eigenschaftenHauptvirus["PositionX"] = screenBreite-6
                    eigenschaftenHauptvirus["PositionY"] = 606
            else:
                zustand = zustandsliste[5]
                print(zustand)
        elif eigenschaftenHauptvirus["PositionX"] > 5:
            eigenschaftenHauptvirus["PositionX"] -= pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)
    # Nach Rechts
    elif zustand == zustandsliste[3]:
        if randaktiv:
            if eigenschaftenHauptvirus["PositionX"] < screenBreite-6 - 55 or (
                    eigenschaftenHauptvirus["PositionY"] > 605 and eigenschaftenHauptvirus[
                "PositionY"] < 706):  # 55 abziehen, wegen Objektlaenge+Rand
                eigenschaftenHauptvirus["PositionX"] += pixelaenderung
                if eigenschaftenHauptvirus["PositionX"] > screenBreite-5:
                    eigenschaftenHauptvirus["PositionX"] = -43
                    eigenschaftenHauptvirus["PositionY"] = 156
            else:
                zustand = zustandsliste[5]
                print(zustand)
        elif eigenschaftenHauptvirus["PositionX"] < screenBreite - 55:  # 50 abziehen, wegen Objektlaenge
            eigenschaftenHauptvirus["PositionX"] += pixelaenderung
        else:
            zustand = zustandsliste[5]
            print(zustand)

    # Zuruecksetzen aller Zustaende, wenn der Rand getroffen wurde
    elif zustand == zustandsliste[5]:
        zustand = zustandsliste[4]
    # Quelle: https://www.youtube.com/watch?v=XJSnaeOcnVs
    # Score Update
        if int(eigenschaftenHauptvirus["Laenge"]) > int(highscore):
            highscore = eigenschaftenHauptvirus["Laenge"]
            textDisplay('New Highscore:' + 'Name ' + str(highscore))
            scoreDatei = open("Score.txt", "w")
            highscore = scoreDatei.write(str(highscore))
            scoreDatei.close()

            scoreDatei = open("Score.txt", "r")
            highscore = scoreDatei.readline()
            scoreDatei.close()

        else:
            textDisplay('GAME OVER')

        eigenschaftenHauptvirus["PositionX"] = 606
        eigenschaftenHauptvirus["PositionY"] = 406
        eigenschaftenHauptvirus["Laenge"] = 0
        virenKette["virenKettePositionX"] = []
        virenKette["virenKettePositionY"] = []
        virenKette["virenKetteZustand"] = []
        virenKette["virenKetteBild"] = []
        virenKette["NaechsterZustand"] = []
        eigenschaftenHauptvirus["NaechsterZustand"] = zustandsliste[4]
        maskeAktiv = False
        eigenschaftenMaske["MaskeZaehler"]=4999
        eigenschaftenSpritze["SpritzeZaehler"]=3999
        geschwindigkeit = 1

    # Idee von: https://docs.python.org/3/library/time.html?highlight=time%20sleep#time.sleep
        time.sleep(1)

    # Virenkettepositionen aktualisieren, nachdem der Rand getroffen wurde
    if randaktiv:
        listenIndex = 0
        for position in virenKette["virenKettePositionX"]:
            # Nach oben
            if virenKette["virenKettePositionY"][listenIndex] < -44:
                virenKette["virenKettePositionX"][listenIndex] = 256
                virenKette["virenKettePositionY"][listenIndex] = screenHoehe-6
            # Nach unten
            if virenKette["virenKettePositionY"][listenIndex] > screenHoehe-6:
                virenKette["virenKettePositionX"][listenIndex] = 756
                virenKette["virenKettePositionY"][listenIndex] = -44
            # Nach Links
            if virenKette["virenKettePositionX"][listenIndex] < -44:
                virenKette["virenKettePositionX"][listenIndex] = screenBreite-6
                virenKette["virenKettePositionY"][listenIndex] = 606
            # Nach Rechts
            if virenKette["virenKettePositionX"][listenIndex] > screenBreite-6:
                virenKette["virenKettePositionX"][listenIndex] = -44
                virenKette["virenKettePositionY"][listenIndex] = 156
            listenIndex += 1

    # Kollisionspruefung mit der Virenkette
    # Die Durchlaeufe sind von der Laenge des Virus abhaengig
    listenIndex = 0
    for position in virenKette["virenKettePositionX"]:
        if listenIndex >= 1 and zustand != zustandsliste[5]:
            if not (eigenschaftenHauptvirus["PositionX"] >= virenKette["virenKettePositionX"][listenIndex] + 50 or
                    eigenschaftenHauptvirus["PositionX"] <= virenKette["virenKettePositionX"][
                        listenIndex] - 50) and not (
                    eigenschaftenHauptvirus["PositionY"] >= virenKette["virenKettePositionY"][listenIndex] + 50 or
                    eigenschaftenHauptvirus["PositionY"] <= virenKette["virenKettePositionY"][listenIndex] - 50):
                zustand = zustandsliste[5]
                print(zustand)
        listenIndex += 1

    # Spiellogik ist hier integriert
    if zustand != "Nichts" and zustand != "Gameover":
        eigenschaftenKleinVirus = kleineViren(eigenschaftenHauptvirus["PositionX"],
                                              eigenschaftenHauptvirus["PositionY"], eigenschaftenKleinVirus,
                                              virusBilder, virenKette)

        collisionPruefung(eigenschaftenHauptvirus, eigenschaftenKleinVirus, virenKette["virenKettePositionX"],
                          virenKette["virenKettePositionY"], virenKette["virenKetteZustand"], zustand,
                          virenKette["virenKetteBild"], virenKette["NaechsterZustand"])
        eigenschaftenMaske = zusatzObjektMaske(eigenschaftenMaske, eigenschaftenHauptvirus["PositionX"],
                                              eigenschaftenHauptvirus["PositionY"],)
        eigenschaftenSpritze = zusatzObjektSpritze(eigenschaftenSpritze, eigenschaftenHauptvirus["PositionX"],
                                              eigenschaftenHauptvirus["PositionY"],)
        maskeAktiv = collisionPruefungMaske(eigenschaftenHauptvirus, eigenschaftenMaske, maskeAktiv)
        spritzeAktiv = collisionPruefungSpritze(eigenschaftenHauptvirus, eigenschaftenSpritze, spritzeAktiv, maskeAktiv, virenKette, zustand, schwierigkeitsgradAktiv)

    # Bewegung der Viruskette
    # Logik ist analog zu Hauptvirus
    # Verzoegerung mit Hilfe des Zustandsspeichers
    virenIndex = 0
    for zustandKette in virenKette["virenKetteZustand"]:
        if zustandKette == "Oben":
            virenKette["virenKettePositionY"][virenIndex] -= pixelaenderung
        elif zustandKette == "Unten":
            virenKette["virenKettePositionY"][virenIndex] += pixelaenderung
        elif zustandKette == "Links":
            virenKette["virenKettePositionX"][virenIndex] -= pixelaenderung
        elif zustandKette == "Rechts":
            virenKette["virenKettePositionX"][virenIndex] += pixelaenderung
        virenIndex += 1





    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            # Spiel wird beendet!
            spielaktiv = False
        # Das Menue wird aktiviert und gezeichnet, wenn Escape gedrueckt wird
        if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
            menu.enable()
    while menu.is_enabled():
        menu.update(pygame.event.get())
        if menu.is_enabled():
            menu.draw(screen)
        pygame.display.update()
    # Speilfeld loeschen
    screen.fill((0, 0, 0))  # Black R,G,B
    # Kleinvirus, Maske und Spritze zeichnen
    if zustand != "Nichts" and zustand != "Gameover":
        screen.blit(eigenschaftenKleinVirus["Bild"], (eigenschaftenKleinVirus["PositionX"], eigenschaftenKleinVirus["PositionY"]))

    # Hauptvirus zeichnen
    # Umdrehen Idee von: https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate
    if zustand == "Oben":
        hauptVirusRichtung = pygame.transform.rotate(hauptVirus, 180)
    elif zustand == "Links":
        hauptVirusRichtung = pygame.transform.rotate(hauptVirus, 270)
    elif zustand == "Rechts":
        hauptVirusRichtung = pygame.transform.rotate(hauptVirus, 90)
    else:
        hauptVirusRichtung = hauptVirus
    screen.blit(hauptVirusRichtung, (eigenschaftenHauptvirus["PositionX"], eigenschaftenHauptvirus["PositionY"]))

    # Virenkette zeichnen
    virenIndex = 0
    for anzahlVirus in virenKette["virenKettePositionX"]:
        if virenKette["virenKetteZustand"][virenIndex] == "Oben":
            virenKette["virenKetteBildRichtung"].append(
                pygame.transform.rotate(virenKette["virenKetteBild"][virenIndex], 180))
        elif virenKette["virenKetteZustand"][virenIndex] == "Links":
            virenKette["virenKetteBildRichtung"].append(
                pygame.transform.rotate(virenKette["virenKetteBild"][virenIndex], 270))
        elif virenKette["virenKetteZustand"][virenIndex] == "Rechts":
            virenKette["virenKetteBildRichtung"].append(
                pygame.transform.rotate(virenKette["virenKetteBild"][virenIndex], 90))
        else:
            virenKette["virenKetteBildRichtung"].append(virenKette["virenKetteBild"][virenIndex])
        screen.blit(virenKette["virenKetteBildRichtung"][virenIndex],
                    (virenKette["virenKettePositionX"][virenIndex], virenKette["virenKettePositionY"][virenIndex]))
        virenIndex += 1
    virenKette["virenKetteBildRichtung"] = []

    if not eigenschaftenMaske["PositionX"] == -1 and zustand != "Nichts" and zustand != "Gameover":
        screen.blit(eigenschaftenMaske["Bild"], (eigenschaftenMaske["PositionX"], eigenschaftenMaske["PositionY"]))

    if not spritzeAktiv and zustand != "Nichts" and zustand != "Gameover":
        screen.blit(eigenschaftenSpritze["Bild"], (eigenschaftenSpritze["PositionX"], eigenschaftenSpritze["PositionY"]))

    # Textfeld zeichnen
    textfeldLaenge = schriftart.render('Laenge: ' + str(eigenschaftenHauptvirus["Laenge"]), False, (255, 255, 255))
    textfeldHighscore = schriftart.render('Highscore: ' + highscore, False, (255, 255, 255))
    screen.blit(textfeldLaenge, (10, 0))
    screen.blit(textfeldHighscore, (980, 0))

    if maskeAktiv:
        textfeldMaske = schriftart.render("Schutzdauer: " + str((500-eigenschaftenMaske["maskeAktivZaehler"])/100), False, (255, 255, 255))
        screen.blit(textfeldMaske, (400,0))
        eigenschaftenMaske["maskeAktivZaehler"] += 1
        if eigenschaftenMaske["maskeAktivZaehler"] == 500:
            eigenschaftenMaske["maskeAktivZaehler"] = 0
            maskeAktiv = False


    # Randlinien zeichenen
    if randaktiv:
        # Rand oben
        pygame.draw.line(screen, (255, 255, 255), (3, 3), (756, 3), width=3)
        pygame.draw.line(screen, (255, 255, 255), (856, 3), (screenBreite - 3, 3), width=3)
        # Rand links
        pygame.draw.line(screen, (255, 255, 255), (3, 3), (3, 156), width=3)
        pygame.draw.line(screen, (255, 255, 255), (3, 256), (3, screenHoehe - 3), width=3)
        # Rand rechts
        pygame.draw.line(screen, (255, 255, 255), (screenBreite - 3, 3), (screenBreite - 3, 606), width=3)
        pygame.draw.line(screen, (255, 255, 255), (screenBreite - 3, 706), (screenBreite - 3, screenHoehe - 3), width=3)
        # Rand unten
        pygame.draw.line(screen, (255, 255, 255), (3, screenHoehe - 3), (256, screenHoehe - 3), width=3)
        pygame.draw.line(screen, (255, 255, 255), (356, screenHoehe - 3), (screenBreite - 3, screenHoehe - 3), width=3)
    else:
        pygame.draw.line(screen, (255, 255, 255), (3, 3), (screenBreite - 3, 3), width=3)
        pygame.draw.line(screen, (255, 255, 255), (3, 3), (3, screenHoehe - 3), width=3)
        pygame.draw.line(screen, (255, 255, 255), (screenBreite - 3, 3), (screenBreite - 3, screenHoehe - 3), width=3)
        pygame.draw.line(screen, (255, 255, 255), (3, screenHoehe - 3), (screenBreite - 3, screenHoehe - 3), width=3)

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(100)

pygame.quit()
