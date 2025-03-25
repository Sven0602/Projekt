import tkinter as tk
from tkinter import ttk, filedialog
from ics import Calendar

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

def lade_und_aktualisiere():
    """Öffnet einen Datei-Dialog, lädt die ICS-Datei und aktualisiert die Tabelle."""
    dateipfad = filedialog.askopenfilename(filetypes=[("ICS Dateien", "*.ics")])
    if dateipfad:
        daten = lade_stundenplan(dateipfad)
        aktualisiere_tabelle(daten)

def aktualisiere_tabelle(daten):
    """Löscht alte Einträge und fügt neue Daten in die Tabelle ein."""
    tree.delete(*tree.get_children())  # Vorherige Einträge entfernen
    for row in daten:
        tree.insert("", tk.END, values=row)  # Daten hinzufügen

# Tkinter GUI erstellen
root = tk.Tk()
root.title("Stundenplan")

# Button zur Dateiauswahl
btn_laden = tk.Button(root, text="ICS-Datei öffnen", command=lade_und_aktualisiere)
btn_laden.pack(pady=10)

# Tabelle erstellen
columns = ("Datum", "Start", "Ende", "Fach")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Spaltenüberschriften setzen
for col in columns:
    tree.heading(col, text=col)

tree.pack(expand=True, fill="both")

# Hauptloop starten
root.mainloop()
