import tkinter as tk
import time

# Die Rechteckklasse		
class Disk(object):	
    def __init__ (self, x1, x2, y1, y2, color, textBox):
        self.item = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.item = canvas.create_text(x1+40, y1+40, text=textBox, font=("Courier",15,"bold"))
        self.x1 = x1
        self.y1 = y1

# Zeichnen von Linien, welche die einzelnen Felder miteinander verbinden
def arrow(x1, y1, x2, y2, width=3):
    canvas.create_line(x1+30, y1+30, x2+50, y2+50, width=width)

# Algorithmus, der alle möglichen Wege ausprobiert
def weg(n, string):

    # Abbruch, falls Ziel erreicht
    if(n == 24):
        string = string + " {}.".format(n)
        final.append(string)                                                                            # Hinzufügen der Lösung in eine Liste
        return
    else:
        string = string + " {}, ".format(n)                                                             # Hinzufügen des derzeitigen Tastenfeldes in den String
        content = dic[n]                                                                                # Auslesen des Dictionarys
        color = content[0]                                                                              # Farbe des Feldes
        letter = content[1]                                                                             # Buchstabe des Feldes
        xLine = n // 5                                                                                  # Begrenzung der Felder auf ihre Zeile
        yLine = n % 5                                                                                   # Begrenzung der Felder auf ihre Spalte
        for k, v in dic.items():
            if(((k // 5 == xLine) or (k % 5 == yLine)) and ((" {}, ".format(k)) not in string)):        # Überprüfen, ob Feld schon einmal besucht wurde
                if(((v[0] == color) or (v[1] == letter)) and (" {}, ".format(k) not in string)):        # Überprüfen, ob das Feld besucht werden darf
                    weg(k, string)                                                                      # Erneuter Aufruf der Funktion mit neuen Parametern

# Hauptprogramm
if __name__ == "__main__":

    # Tastenfeld aus der puzzle-Datei
    with open('tastenfeld5.puzzle', 'r') as file:
        keypad = []
        for line in file:
            key = []
            key.append(line[0])
            key.append(line[1])
            keypad.append(key)
        file.close()

    # Alles für das GUI vorbereiten
    # Fenster anlegen
    window = tk.Tk()
    window.title("Tastenfeld")

    # Frame anlegen
    frame = tk.Frame(window)
    frame.pack()

    # Canvas anlegen
    canvas = tk.Canvas(frame, bg="#f0e0b0", width=458, height=458)
    canvas.pack()

    # Farbendefinitionen
    colors = {
        "Y":"yellow",
        "B":"blue",
        "G":"green",
        "R":"red",
        "C":"cyan",
        "M":"magenta"
    }

    # Tastenfelder und Anfangskoordinaten
    rectangles = []
    x1 = 10; x2 = 90; y1 = 10; y2 = 90

    # Tastenfelder initialisieren und anordnen
    rectangle = 0
    for element in keypad:
        if ((rectangle % 5 == 0) and (rectangle != 0)):
            x1 = 10
            x2 = 90
            y1 += 90
            y2 += 90
        color = colors[element[0]]
        text = "{}\n\n{}".format(element[1], rectangle)
        rectangles.append(Disk(x1, x2, y1, y2, color, text))
        x1 += 90
        x2 += 90
        rectangle += 1

    # Tastenfelder anzeigen
    window.update()
    time.sleep(1)

    # Umwandeln der Tastenfelder in ein Dictionary
    dic = {}
    for x in range(25):
        dic[x] = keypad[x]

    # Liste, in der die einzelnen Lösungswege gespeichert werden
    final = []

    # Aufrufen der Funktion
    weg(0, "")

    print("\nAnzahl Moeglichkeiten: {}\n".format(len(final)))

    # Falls eine Lösung gefunden wurde
    if(len(final) != 0):
        lenBestWay = float('inf')

        # Finde den kürzesten Weg und gebe alle Lösungen aus
        for way in final:
            if(len(way) < lenBestWay):
                lenBestWay = len(way)
                bestWay = way
            print(way)

        print("\nKuerzester Weg: {}".format(bestWay))

        # Wandle den String in eine Liste um
        bestWay = bestWay.lstrip().replace("  ", "").replace(".", "").split(",")
        number = []
        for x in bestWay:
            number.append(int(x))

        # Die Felder, welche den kürzesten Lösungsweg darstellen, in der richtigen Reihenfolge verbinden
        for x in range(len(number)):
            if(x+1 == len(number)):
                break
            start = number[x]
            end = number[x+1]
            startRec = rectangles[start]
            endRec = rectangles[end]
            arrow(startRec.x1, startRec.y1, endRec.x1, endRec.y1)
            window.update()
            time.sleep(0.5)

    # Offenhalten der GUI
    window.mainloop()