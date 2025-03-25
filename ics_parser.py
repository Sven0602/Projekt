from ics import Calendar
from datetime import datetime

def lade_stundenplan(dateipfad):
    """Liest eine ICS-Datei ein und gibt eine Liste mit Stundenplandaten zurück."""
    with open(dateipfad, "r", encoding="utf-8") as f:
        kalender = Calendar(f.read())

    stundenplan = []
    for event in kalender.events:
        datum = event.begin.date()  # Datum des Termins
        startzeit = event.begin.strftime("%H:%M")  # Startzeit
        endzeit = event.end.strftime("%H:%M")  # Endzeit
        fach = event.name  # Name des Fachs

        stundenplan.append((datum, startzeit, endzeit, fach))

    return stundenplan

# Test mit einer Datei
if __name__ == "__main__":
    datei = "lem.ics"  # Hier kannst du eine Datei deiner Wahl eintragen
    daten = lade_stundenplan(datei)
    
    for eintrag in daten:
        print(eintrag)  # Zeigt alle Termine aus der Datei an
