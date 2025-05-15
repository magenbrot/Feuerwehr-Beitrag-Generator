import json
import datetime
import os
import subprocess
import sys

# --- Konfiguration ---
file_path = 'package.json'
repo_name = 'magenbrot/Feuerwehr-Beitrag-Generator' # Dein GitHub Repository (Benutzer/Repo)
main_branch = 'main' # Name deines Hauptzweigs (oft 'main' oder 'master')

# --- Versionslogik ---
current_year_month = datetime.date.today().strftime('%Y.%m')
# Der PATCH-Zähler startet standardmäßig bei 0
new_patch = 0
old_version = None # Variable für die alte Version


print(f"Starte Prozess zur Aktualisierung der Version und Git/GitHub-Aktionen...")


# --- Datei prüfen ---
if not os.path.exists(file_path):
    print(f"Fehler: Datei '{file_path}' nicht gefunden.")
    sys.exit(1) # Skript beenden, wenn Datei nicht existiert

# --- JSON lesen und Version berechnen ---
try:
    print(f"\nLese '{file_path}' zur Versionsermittlung...")
    # JSON-Datei lesen
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Alte Version auslesen (Standardwert '0.0.0', falls 'version' nicht existiert)
    old_version = data.get('version', '0.0.0')
    print(f"Aktuelle Version in Datei: {old_version}")

    # Versuche, die alte Version zu parsen und den Patch zu erhöhen
    parts = old_version.split('.')

    # Prüfen, ob die alte Version das Format YYYY.MM.PATCH hat
    if len(parts) == 3:
        old_year_month = f"{parts[0]}.{parts[1]}"
        try:
            old_patch = int(parts[2])

            # Prüfen, ob Jahr und Monat der alten Version mit dem aktuellen übereinstimmen
            if old_year_month == current_year_month:
                new_patch = old_patch + 1
                print(f"Aktueller Monat/Jahr ({current_year_month}) stimmt überein. Erhöhe Patch von {old_patch} auf {new_patch}.")
            else:
                 print(f"Aktueller Monat/Jahr ({current_year_month}) unterscheidet sich von alter Version ({old_year_month}). Setze Patch auf 0.")
                 new_patch = 0 # Neuen Monat/Jahr -> Patch bei 0 starten
        except ValueError:
             print(f"Patch-Teil der alten Version '{parts[2]}' ist keine Zahl. Setze Patch auf 0.")
             new_patch = 0 # Patch ist keine Zahl -> Patch bei 0 starten
    else:
        print(f"Alte Version '{old_version}' hat nicht das Format YYYY.MM.PATCH. Setze Patch auf 0.")
        new_patch = 0 # Altes Format oder ungültiges Format -> Patch bei 0 starten


    # Neue Version im Format YYYY.MM.PATCH (Patch zweistellig formatiert) erstellen
    new_version = f"{current_year_month}.{new_patch:02d}"
    tag_name = new_version # Der Tag-Name ist die neue Version

    print(f"Berechnete neue Version: {new_version}")

    # Version im Daten-Dictionary aktualisieren
    data['version'] = new_version

    # Modifiziertes JSON zurück in die Datei schreiben
    # 'indent=2' sorgt für eine lesbare Formatierung
    print(f"\nSchreibe neue Version '{new_version}' in '{file_path}'...")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("Datei erfolgreich geschrieben.")
    print("-" * 30)

except FileNotFoundError:
     # Dies sollte hier eigentlich nicht passieren, da wir oben prüfen
     print(f"\nSchwerwiegender Fehler: Datei '{file_path}' nicht gefunden während des Lesens.")
     sys.exit(1)
except json.JSONDecodeError:
    print(f"\nFehler: Konnte '{file_path}' nicht parsen. Ungültiges JSON-Format.")
    sys.exit(1)
except Exception as e:
    print(f"\nEin unerwarteter Fehler beim Lesen/Schreiben der Datei ist aufgetreten: {e}")
    sys.exit(1)


# --- Git/Github Kommandos ausführen ---
print("Führe nun Git/Github Kommandos aus:")

commands_to_run = [
    (['git', 'add', file_path], f"Änderungen in {file_path} stagen"),
    (['git', 'commit', '-m', f'Update version to {new_version}'], f"Commit erstellen mit Nachricht 'Update version to {new_version}'"),
    (['git', 'tag', tag_name], f"Tag '{tag_name}' erstellen"),
    (['git', 'push', '--atomic', 'origin', main_branch, tag_name], f"Commit und Tag zu 'origin {main_branch}' pushen"),
    (['gh', 'release', 'create', tag_name, f'--repo={repo_name}', f'--title=Feuerwehr-Beitrag-Generator {tag_name}', '--generate-notes'], f"GitHub Release '{tag_name}' auf '{repo_name}' erstellen")
]

try:
    for command, description in commands_to_run:
        print(f"\n-> {description}")
        print(f"   Befehl: {' '.join(command)}")

        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd='.'
        )

        print("   [OK]")
        if result.stdout:
            print("   Stdout:\n" + result.stdout.strip())
        if result.stderr:
            print("   Stderr:\n" + result.stderr.strip())


    print("\n" + "="*30)
    print("Alle Schritte erfolgreich abgeschlossen!")
    print("="*30)
    sys.exit(0)

except FileNotFoundError:
     # Diese Exception wird geworfen, wenn z.B. 'git' oder 'gh' nicht gefunden werden
     print(f"\nFehler: Ein benötigter Befehl wurde nicht gefunden.")
     print(f"Stelle sicher, dass Git und gh (Github CLI) installiert sind und im PATH liegen.")
     sys.exit(1)
except subprocess.CalledProcessError as e:
    # Diese Exception wird geworfen, wenn ein Kommando mit einem Fehlercode zurückkehrt
    print(f"\nFehler beim Ausführen eines Befehls:")
    print(f"Befehl: {' '.join(e.cmd)}")
    print(f"Rückgabecode: {e.returncode}")
    if e.stdout:
        print("Stdout des Fehlers:\n" + e.stdout.strip())
    if e.stderr:
         print("Stderr des Fehlers:\n" + e.stderr.strip())
    print("\nAbbruch: Ein Git/Github Befehl ist fehlgeschlagen.")
    sys.exit(1)
