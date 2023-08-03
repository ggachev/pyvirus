# PyVirus
Projekt in Informatikwerstatt - Anwendungsentwicklung
Gruppe 5
Silvia, Anastasia, Karla, Gabriel

# Installation
1.  Pygame_Menu installieren:
    Im Terminal folgendes eingeben:
    python -m pip install pygame-menu
3. Spiel ueber PyVirus.py starten (Kann nur über eine IDE gestartet werden, z. B. PyCharm)

# Verlauf
25.11.2020 - Objekt startet in der Mitte und kann sich bis zur Rand bewegen.

26.11.2020 - Objekt wird nach treffen der Rand zurueckgesetzt, versuch kleine Viren zu spawnen

27.11.2020 - Virus Bild hinzugefuegt, kleine Viren erscheinen sporadisch, noch als quadrate

01.12.2020 - kleine Viren erscheinen als zufaellige Bilder, Kollisionspruefung funktioniert

02.12.2020 - Versuch den kelinen Virus an dem Grossen anzuhaengen

03.12.2020 - Kleine Viren können angehängt werden, diese können sich aber noch nicht bewegen

04.12.2020 - kleine Viren bewegen sich mit dem Hauptvirus

08.12.2020 - Geschwindigkeiten wurden eingefuegt, leider bewegt sich die Kette danach nicht wie gewollt

09.12.2020 - Viruskette bewegt sich korrekt, Geschwindigkeiten funktionieren

10.12.2020 - Funktion fuer Kollisionspruefung mit sich selbst eingebaut; Sleep von einer Sekunde nach Gameover eingebaut

11.12.2020 - Kommentierung und kleine Bugs beseitigen

15.12.2020 - Liste für Virenkette in ein Dictionary umgewandelt +Score datei hinzugefügt

16.12.2020 - Viren drehen sich anhand der Richtung um; kleine Viren werden nicht mehr unter der Virenkette gespawned(Funktion kleineViren erweitert)

17.12.2020 - Funktion kleineViren angepasst nach der Erweiterung; Textfelder hinzugefuegt

18.12.2020 - Versuch die Geschwindigkeitsanpassung zu optimieren; leider besteht das Problem immernoch, dass bei Aenderung der Geschwindigkeit manchmal sich die kleine Viren nicht an die Richtige Postition spawnen bzw. nicht in die richtige Richtung fuer X Schritte laufen

22.12.2020 - Ein Grundspiel ohne bekannte Fehler wurde erstellt. Damit können wir über das Ferien unsere Funktionen entwickeln. Silvi - Highscore Datei; Karla - Geschwindigkeitsanpassung; Nasti - Maske und Spritze; Gabriel - Randübergang mit Menue

06.01.2021 - Versuch alles zusammenzufassen, was wir entwickelt haben. Alles wurde zusammengeaffst, außer die Funktionen von Silvi.

07.01.2021 - Alles wurde zusammengefügt; Bugs wurde beseitigt sowie einen mit dem Rand

08.01.2021 - Namen werden in der Highscoredatei gespeichert

10.01.2021 - Weitere bugs wurden beseitigt

13.01.2021 - Es gibt neue Funktion, gewinnPruefung

14.01.2021 - Hauptvirus ist jetzt mit Maske als Bild, wenn man die Maske sammelt und die Viren drehen sich entsprechend der Richtung

15.01.2021 - Es wurden weitere Bugs und Anpassungen beseitigt/vorgenommen

19.01.2021 - Es wurden Sounds hinzugefügt

20.01.2021 - Hintergrundbild wurde von Silvi erstellt und hinzugefügt

21.01.2021 - Bugs mit Ton und Maske wurden behoben

26.01.2021 - Bug mit der Kollisiionsprüfung wurde beseitigt indem die Virenkettebewebung vor der Kollisionsprüfung stattfindet

27.01.2021 - Funktionen um Texte auszugeben wurden komprimiert. Weiterhin wurde der Code kommentiert.

28.01.2021 - Randuebergang wurde so gemacht, dass wenn z.B. der Virus von unten bzw. von rechts reingehet auch von unten bzw. von rechts rauskommt. Das ermoeglich ein Loch zweimal gleichzeitig zu benutzen. Kommentare wurden hinzugefuegt. 

02.02.2021 - Alle Sounds werden im Header deklariert und initialisiert. Bug mit dem Background Sound wurde beseitigt. Der Sound hat sich immer wieder gestarted, nachdem man das Manue geoeffnet und geschlossen wurde. Die Maske wird jetzt richtig zurueckgesetzt nach dem Gameover. Alle Bugs, die bekannt waren, wurden beseitigt.

03.-07.02.2021 - Endpräsentation erstellen und abegeben

09./10.02.2021 - Endpräsentation vorstellen
