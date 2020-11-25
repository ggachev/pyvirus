# Pygame Beispiel
import os, sys, pygame, pygame.locals

# Initialisieren von PyGame
pygame.init()

# Fenster öffnen
screen =pygame.display.set_mode((640, 480))

# Titel für Fensterkopf
pygame.display.set_caption('PyVirus')

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Spielzustand vorbereiten
x = 320
y = 50

# Schleife Hauptprogramm
while spielaktiv:

# Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            # Spiel wird beendet!
            spielaktiv=False

# Aktualisieren des Zustands
    if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
        x -= 1
    if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
        x += 1
    if pygame.key.get_pressed()[pygame.locals.K_UP]:
        y -= 1
    if pygame.key.get_pressed()[pygame.locals.K_DOWN]:
        y += 1
# Spiellogik hier integrieren

# Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
    screen.fill((64, 64, 64))  # Dark Gray
    pygame.draw.circle(screen, (192, 32, 32), (x, y), 10)
    pygame.draw.rect(screen, (0,100,0), (280,150,100,50))
    pygame.draw.circle(screen, (139, 90, 43), (320, 300), 20)

# Fenster aktualisieren
    pygame.display.flip()

# Refresh-Zeiten festlegen
    clock.tick(60)

pygame.quit()
