# AbacusMathSolver

AbacusMathSolver ist ein interaktives Lernwerkzeug, das Kindern hilft, grundlegende mathematische Aufgaben mit einem Abacus 20 zu lösen und ihre Antworten mithilfe einer Kamera zu überprüfen. Das Programm stellt zufällige Rechenaufgaben und überprüft die Antwort durch Farberkennung der Kugeln auf dem Abacus. Ein Audiofeedback gibt Rückmeldung, ob die Antwort richtig oder falsch ist.

## Features

- **Matheaufgaben:** Zufällig generierte Additionsaufgaben.
- **Kameraüberprüfung:** Die Lösung wird mit Hilfe einer Kamera und OpenCV überprüft.
- **Audiofeedback:** Die Aufgabenstellung und die Rückmeldung zur Antwort erfolgen per Audio.
- **Live-Feedback:** Echtzeit-Visualisierung der Kugeln auf dem Bildschirm.

## Anforderungen

Stelle sicher, dass folgende Software und Bibliotheken installiert sind:

- Python 3.x
- OpenCV
- NumPy
- pyttsx3 (für Text-to-Speech)
- Eine Kamera (Webcam oder externe Kamera)

## Installation

1. **Python installieren:** Stelle sicher, dass Python 3.x auf deinem System installiert ist. Lade Python hier herunter: [Python Download](https://www.python.org/downloads/).

2. **Projekt klonen:**
   ```bash
   git clone https://github.com/Jobba7/AbacusMathSolver.git
   cd AbacusMathSolver
   ```

3. **Virtuelle Umgebung erstellen und aktivieren (optional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Für macOS/Linux
   venv\Scripts\activate     # Für Windows
   ```

4. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```
   Abhängigkeiten aktualisieren (für Entwickler):
   ```bash
   pip freeze > requirements.txt
   ```

## Ausführung

### Schritt-für-Schritt-Anleitung

1. **Kamera anschließen:** Stelle sicher, dass deine Kamera verbunden und funktionsfähig ist.

2. **Programm starten:**
   ```bash
   python main.py
   ```

3. **Aufgabenstellung hören:** Sobald das Programm gestartet wird, stellt es eine Matheaufgabe, die du mit den Kugeln auf dem Abacus lösen sollst. Beispiel: "Bitte rechne 3 plus 5."

4. **Kugeln legen:** Lege die entsprechende Anzahl roter und blauer Kugeln auf den Abacus, um die Aufgabe zu lösen.

5. **Ergebnis hören:** Das Programm überprüft die Anzahl der Kugeln und gibt eine Rückmeldung per Audio, ob die Antwort richtig oder falsch ist. Danach wird eine neue Aufgabe gestellt.