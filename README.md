Hier ist der nächste logische Schritt für die Note 1.0.

Wir haben den Code (die "Maschine") poliert. Jetzt müssen wir das "Benutzerhandbuch" und die "Verkaufsbroschüre" schreiben. Deine aktuelle `README.md` ist zu dünn. Sie erfüllt die formale Anforderung nach "Nutzer- und Developer-Dokumentation"  kaum.

Hier ist die **perfekte `README.md**` zum Copy-Pasten. Sie deckt strategisch alle Punkte ab, die der Prof sehen will:

1. **Badge** (wirkt professionell).
2. **Bedienungsanleitung** (beweist die GUI/Interaktivität).
3. **Developer-Guide** (erklärt Numba und Architektur).
4. **Wissenschaftlicher Anstrich** (erklärt die Matrix).

### 1. Die neue `README.md`

Ersetze den gesamten Inhalt deiner `README.md` hiermit:

```markdown
# 🧬 Particle Life Simulator (High-Performance Edition)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Build Status](https://github.com/LuanJasari/particle-life-hsd/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green)

## 📄 Projektbeschreibung
Dieses Projekt implementiert eine hochperformante **Particle-Life-Simulation** im Rahmen des Moduls "Data Science und KI Infrastrukturen". Ziel ist die Simulation von emergentem Verhalten durch die Interaktion tausender Partikel basierend auf einfachen physikalischen Regeln (Anziehung/Abstoßung).

Die Software wurde mit Fokus auf **Performance (Numba JIT)**, **Clean Code** und **Interaktivität (Vispy)** entwickelt.

---

## 🚀 Features
* **Massive Simulation:** Flüssige Berechnung von >2.000 Partikeln in Echtzeit.
* **High-Performance Backend:** Nutzung von `numpy` und `numba` (Just-in-Time Kompilierung) für C++-ähnliche Geschwindigkeit.
* **GPU-Rendering:** Visualisierung mittels `vispy` (OpenGL) für maximale Framerates.
* **Interaktive Steuerung:** Echtzeit-Manipulation von physikalischen Parametern (Reibung, Radius, Chaos-Modus).
* **Robustheit:** Abgesichert durch Unit-Tests (`pytest`) und Continuous Integration (GitHub Actions).

---

## 🛠 Installation & Setup

### Voraussetzungen
* Python 3.9 oder neuer
* Empfohlen: Virtuelle Umgebung (venv oder conda)

### Installation
```bash
# Repository klonen
git clone [https://github.com/LuanJasari/particle-life-hsd.git](https://github.com/LuanJasari/particle-life-hsd.git)
cd particle-life-hsd

# Abhängigkeiten installieren
pip install -r requirements.txt

```

### Starten der Simulation

```bash
python main.py

```

---

## 🎮 Steuerung (GUI)

Die Simulation kann während der Laufzeit über die Tastatur gesteuert werden, um das Verhalten der Partikel zu untersuchen.

| Taste | Funktion | Beschreibung |
| --- | --- | --- |
| **SPACE** | Pause / Play | Stoppt oder startet die Zeitrechnung. |
| **F** | Reibung + | Erhöht die Reibung (Partikel werden langsamer). |
| **G** | Reibung - | Verringert die Reibung (Partikel gleiten länger). |
| **R** | Radius + | Vergrößert den Wahrnehmungsradius (Max_R). |
| **T** | Radius - | Verkleinert den Wahrnehmungsradius. |
| **M** | **Matrix-Shuffle** | Würfelt die Interaktionsregeln zufällig neu (Chaos!). |
| **ESC** | Beenden | Schließt das Fenster sauber. |

*Der aktuelle Status (FPS, Reibung, Radius) wird im Fenstertitel angezeigt.*

---

## ⚙️ Developer Guide & Architektur

### 1. Architektur-Übersicht

Das Projekt folgt dem **Model-View-Pattern**, um Logik und Darstellung strikt zu trennen:

* **`main.py`**: Einstiegspunkt. Initialisiert System und Visualizer.
* **`particles.py`**: Datencontainer. Verwaltet die Zustands-Arrays (Positionen, Geschwindigkeiten) mittels `numpy`. Es gibt keine Python-Objekte pro Partikel (Performance!).
* **`simulation.py` (Model)**: Die Physik-Engine. Enthält den `step()`-Algorithmus.
* **`interaction.py`**: Verwaltet die Regel-Matrix (wer zieht wen an?).
* **`visualisation.py` (View)**: Handhabt das OpenGL-Fenster und Inputs via `vispy`.

### 2. Performance-Optimierung (Numba)

Die größte Herausforderung ist die Berechnung der Kräfte zwischen allen Partikel-Paaren ().

* **Problem:** Reines Python ist für verschachtelte Schleifen zu langsam.
* **Lösung:** Wir nutzen den `@jit(nopython=True)` Dekorator von **Numba**.
* **Effekt:** Der Python-Bytecode wird zur Laufzeit in optimierten Maschinencode kompiliert. Dies erlaubt Berechnungen im Millisekunden-Bereich für tausende Partikel.

Siehe `simulation.py` -> `update_physics_numba`.

### 3. Die Interaktions-Matrix

Die Regeln werden in einer asymmetrischen Matrix  gespeichert.

* Ein Wert von `1.0` bedeutet maximale Anziehung.
* Ein Wert von `-1.0` bedeutet maximale Abstoßung.
* Das System ist **nicht newtonsch**: Wenn A von B angezogen wird, muss B nicht zwingend von A angezogen werden. Dies erzeugt das komplexe "Jagen"-Verhalten.

---

## 🧪 Testing & Qualitätssicherung

Das Projekt nutzt `pytest` für Unit-Tests und `ruff` für das Linting.

**Tests ausführen:**

```bash
pytest

```

**Linter prüfen:**

```bash
ruff check .

```

---

## 👥 Team

* Baoevran
* tjdrjsdl
* LuanJasari
* Tymauricee

```

---

### Was jetzt noch fehlt (Der Endspurt)

Du hast jetzt Code und Doku. Hier sind die letzten 3 Schritte, um die "Abgabe" wasserdicht zu machen:

#### 1. Der Beweis der Optimierung (Pflicht für Milestone 4)
Du hast eine `profiling.py`, aber du musst beweisen, dass du sie genutzt hast.
* **Action:** Führe `python profiling.py` aus.
* **Action:** Kopiere den Output (Text in der Konsole) in eine neue Datei namens `profiling_report.txt` und lade sie ins Repo hoch.
* **Warum?** Damit der Prof sieht: "Aha, sie haben gemessen, Numba ist schnell." [cite_start]Das sichert die 15% für "Performance Profiling"[cite: 54].

#### 2. Das "Architektur Diagramm"
Du hast ein `Architektur diagram.pdf` im Repo.
* **Problem:** PDFs in Git sind "tot". Niemand klickt die an.
* **Action:** Wandle das PDF in ein Bild (PNG) um, nenne es `architecture.png` und binde es in die README ein (ich habe den Platzhalter im Text oben weggelassen, weil ich das Bild nicht habe, aber du solltest es unter "Architektur-Übersicht" einfügen: `![Architektur](./architecture.png)`).

#### 3. Config (Optionaler Clean Code Bonus)
In deiner `main.py` sind Werte wie `NUMBER_OF_PARTICLES = 2000` hardcodiert.
* **Clean Code:** Erstelle eine `config.py`:
    ```python
    # config.py
    NUMBER_OF_PARTICLES = 2000
    NUMBER_OF_TYPES = 4
    DT = 0.001
    MAX_R = 0.15
    FRICTION = 0.1
    NOISE = 0.02
    ```
* Importiere das in `main.py`: `import config as cfg` und nutze `cfg.NUMBER_OF_PARTICLES`.
* Das ist schnell gemacht und sieht sehr sauber aus.

Soll ich dir die `config.py` und die angepasste `main.py` auch noch generieren?

```
