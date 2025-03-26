import tkinter as tk
import arrow
from ics import Calendar
import requests

# Funktion zum Laden der ICS-Datei
def load_schedule_from_url(dozent):
    ics_urls = {
        "GIO": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Gio",
        "LEM": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Lem",
        "SCB": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Scb",
        "SCC": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Scc",
        "SHO": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Sho",
        "NEM": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Nem",
        "GIN": "https://intranet.bib.de/ical/3ded6754b78e68ad3edb0d89313f843f/Gin"
    }
    
    start_of_week = arrow.now().floor('week')
    end_of_week = start_of_week.shift(days=6)  # Bis Sonntag

    # Alle Zellen leeren
    for day in days:
        for i in range(1, 6):
            entries[day][i].config(state="normal")
            entries[day][i].delete(0, tk.END)

    try:
        response = requests.get(ics_urls[dozent])
        response.raise_for_status()
        calendar = Calendar(response.text)
        
        # Debugging: Anzahl der geladenen Events
        print(f"Geladene Events für {dozent}: {len(calendar.events)}")

        fill_schedule_with_events(calendar.events, start_of_week, end_of_week)
    except requests.RequestException as e:
        print(f"Fehler beim Laden der Datei für {dozent}: {e}")

# Funktion zum Einfügen der Events
def fill_schedule_with_events(events, start_of_week, end_of_week):
    weekday_mapping = {
        "Monday": "Montag",
        "Tuesday": "Dienstag",
        "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag",
        "Friday": "Freitag",
        "Saturday": "Samstag",
        "Sunday": "Sonntag"
    }

    for event in events:
        event_start = event.begin.to('local').datetime  # Lokale Zeit
        
        # Debugging: Event-Daten ausgeben
        print(f"Event: {event.name} | Start: {event_start} | Tag: {event_start.strftime('%A')}")
        
        if start_of_week.datetime <= event_start <= end_of_week.datetime:
            event_day = weekday_mapping.get(event_start.strftime('%A'), None)
            event_time = event_start.strftime('%H:%M')
            event_title = event.name
            
            # Debugging: Event wird für diesen Zeitraum verwendet
            print(f"--> Event im Zeitraum: {event_title} am {event_day} um {event_time}")

            if event_day in entries:
                for j, block in enumerate(blocks):
                    start_time, _ = block.split(" ")[1].split("-")
                    
                    event_hour, event_minute = map(int, event_time.split(":"))
                    start_hour, start_minute = map(int, start_time.strip().split(":"))
                    
                    # Erlaube eine Toleranz von ±15 Minuten
                    if abs((event_hour * 60 + event_minute) - (start_hour * 60 + start_minute)) <= 15:
                        current_text = entries[event_day][j+1].get()
                        new_text = event_title if not current_text else f"{current_text}\n{event_title}"
                        entries[event_day][j+1].delete(0, tk.END)
                        entries[event_day][j+1].insert(0, new_text)
                        entries[event_day][j+1].config(state="readonly")

# Funktion zum Aktualisieren des Stundenplans
def update_schedule(*args):
    dozent = selected_dozent.get()
    if dozent:
        load_schedule_from_url(dozent)

# Tkinter-GUI
root = tk.Tk()
root.title("Stundenplan")
root.geometry("900x500")

days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
entries = {day: {} for day in days}

blocks = [
    "1. 8:00-9:30", 
    "2. 9:45-11:15", 
    "3. 11:30-13:00", 
    "4. 13:45-15:15", 
    "5. 15:30-17:00"
]

dozenten = ["GIO", "LEM", "SCB", "SCC", "SHO", "NEM", "GIN"]
selected_dozent = tk.StringVar()

# GUI Layout
tk.Label(root, text="Dozent auswählen", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=6, sticky="nsew")
dozent_menu = tk.OptionMenu(root, selected_dozent, *dozenten, command=update_schedule)
dozent_menu.grid(row=1, column=0, columnspan=6, sticky="nsew")

tk.Label(root, text="Block", font=("Helvetica", 12)).grid(row=2, column=0, sticky="nsew")

for i, block in enumerate(blocks):
    tk.Label(root, text=block, font=("Helvetica", 10)).grid(row=i+3, column=0, sticky="nsew")

for i, day in enumerate(days):
    tk.Label(root, text=day, font=("Helvetica", 12)).grid(row=2, column=i+1, sticky="nsew")
    for j in range(1, 6):
        entry = tk.Entry(root, state="readonly", justify="center")
        entry.grid(row=j+2, column=i+1, sticky="nsew")
        entries[day][j] = entry

# Grid-Layout anpassen
for i in range(6):
    root.grid_columnconfigure(i, weight=1, uniform="equal")
for i in range(9):
    root.grid_rowconfigure(i, weight=1, uniform="equal")

selected_dozent.set(dozenten[0])
update_schedule()
root.mainloop()