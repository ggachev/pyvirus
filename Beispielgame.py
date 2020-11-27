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

# Startlaenge
laengeObjekt1 = 1

# Spielzustand vorbereiten [x, y]
positionObjekt1 = [600, 400]

# Liste fuer die kleine Viren
kleinVirus = {
    "PositionX" : 0,
    "PositionY" : 0,
    "Zaehler" : 199,
    "R" : 140,
    "G" : 140,
    "B" : 140
}

# Virus Bilder
HauptVirus = pygame.image.load('Hauptvirus.png')
virusGruen = pygame.image.load('Virus_Gruen_edited_50x50.png')

# Funktion um kleine Viren zu erstellen
def kleineViren(x, y, laenge, dictionary, zustand):
    z = dictionary["Zaehler"]
    if zustand != "Nichts" and zustand != "Gameover":
        z += 1
        if z == 200:
            randomr = random.randrange(140, 255)
            randomg = random.randrange(140, 255)
            randomb = random.randrange(140, 255)

            dictionary["R"] = randomr
            dictionary["G"] = randomg
            dictionary["B"] = randomb

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
        if positionObjekt1[1] != 0:
            positionObjekt1[1] -=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    if zustand == zustandsliste[1]:
        if positionObjekt1[1] != 750: # 50 abziehen, wegen Objektlaenge
            positionObjekt1[1] +=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    if zustand == zustandsliste[2]:
        if positionObjekt1[0] != 0:
            positionObjekt1[0] -=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])

    if zustand == zustandsliste[3]:
        if positionObjekt1[0] != 1150: # 50 abziehen, wegen Objektlaenge
            positionObjekt1[0] +=0.5
        else:
            zustand = zustandsliste[5]
            print(zustandsliste[5])
    # Zuruecksetzen der Zustand, wenn der Rand getroffen wurde
    if zustand == zustandsliste[5]:
        positionObjekt1[0] = 600
        positionObjekt1[1] = 400

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

    kleinVirus = kleineViren(positionObjekt1[0], positionObjekt1[1], laengeObjekt1, kleinVirus, zustand)

# Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
# RGB Schwarz -> 0, 0, 0
# RGB Pink -> 255, 20, 147
# RGB Dark Grey -> 64, 64, 64
# RGB White -> 255, 255, 255
    screen.fill((0, 0, 0))  # Black
    #pygame.draw.rect(screen, (255, 20, 147), (positionObjekt1[0],positionObjekt1[1],50,50))
    if zustand != "Nichts" and zustand != "Gameover":
        pygame.draw.rect(screen, (kleinVirus["R"], kleinVirus["G"], kleinVirus["B"]), (kleinVirus["PositionX"], kleinVirus["PositionY"], 50, 50))
    #screen.blit(virusGruen, (200, 200))
    screen.blit(HauptVirus, (positionObjekt1[0],positionObjekt1[1]))

# Fenster aktualisieren
    pygame.display.flip()

# Refresh-Zeiten festlegen
    clock.tick(100)

pygame.quit()
