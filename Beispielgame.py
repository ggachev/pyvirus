# Pygame Beispiel
import os, sys, pygame, pygame.locals

# Initialisieren von PyGame
pygame.init()

# Fenster öffnen
screen =pygame.display.set_mode((1280, 800))

# Titel für Fensterkopf
pygame.display.set_caption('PyVirus')

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Liste für Zustände für die Richtungen des Virus + Variable, der immer ein Zustand zugeordnet wird
richtung =["Oben", "Unten", "Links", "Rechts", "Nichts"]
zustand = richtung[4]

# Spielzustand vorbereiten
x = 640
y = 400

# Schleife Hauptprogramm
while spielaktiv:
    # Prüfung, in welche Richtung sich der Spieler automatisch nach vorne bewegen soll.

    if zustand == richtung[0]:
        if y != 0:
            y -=0.5
        else:
            zustand = richtung[4]

    if zustand == richtung[1]:
        if y != 750: # 50 abziehen, wegen Objektlaenge
            y +=0.5
        else:
            zustand = richtung[4]

    if zustand == richtung[2]:
        if x != 0:
            x -=0.5
        else:
            zustand = richtung[4]

    if zustand == richtung[3]:
        if x != 1230: # 50 abziehen, wegen Objektlaenge
            x +=0.5
        else:
            zustand = richtung[4]
    #  if (x == 1280) or (x == 0 ) or (y == 800 ) or (y == 0):
    #   zustand = richtung[4]

# Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            # Spiel wird beendet!
            spielaktiv=False

# Aktualisieren des Zustands
    if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
        zustand = richtung[2]
    if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
        zustand = richtung[3]
    if pygame.key.get_pressed()[pygame.locals.K_UP]:
        zustand  = richtung[0]
    if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
        zustand = richtung[1]

# Spiellogik hier integrieren


# Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
# RGB Schwarz -> 0, 0, 0
# RGB Pink -> 255, 20, 147
# RGB Dark Grey -> 64, 64, 64
    screen.fill((0, 0, 0))  # Dark Gray
    pygame.draw.rect(screen, (255, 20, 147), (x,y,50,50))

# Fenster aktualisieren
    pygame.display.flip()

# Refresh-Zeiten festlegen
    clock.tick(100)

pygame.quit()
