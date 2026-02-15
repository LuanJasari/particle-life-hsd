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

## 📊 Performance Benchmarks

Um die Effizienz der Optimierung zu beweisen, wurde ein standardisiertes Profiling durchgeführt (Script: `profiling.py`). Die Ergebnisse belegen, dass der Python-Interpreter-Overhead durch `numba` eliminiert wurde.

**Test-Szenario:**
* **Anzahl Partikel:** 1.500
* **Zeitschritte:** 200 (Headless Mode)
* **Komplexität:** $O(N^2)$ Interaktionen pro Frame

**Ergebnisse:**
* **Durchschnittliche Framerate:** **80.40 FPS**
* **Berechnungszeit pro Frame:** ~12 ms
* **Bottleneck-Analyse:** >99% der Rechenzeit finden innerhalb der kompilierten `step()`-Funktion statt (No Python Overhead).

---

## 🛠 Installation & Setup

### Voraussetzungen
* Python 3.10 oder neuer
* Empfohlen: Virtuelle Umgebung (venv oder conda)

### Installation
```bash
# Repository klonen
git clone [https://github.com/LuanJasari/src.git](https://github.com/LuanJasari/particle-life-hsd.git)
cd src

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
* **`particles.py`**: Datencontainer. Verwaltet die Zustands-Arrays (Positionen, Geschwindigkeiten) mittels `numpy`. Es gibt keine Python-Objekte pro Partikel (Memory Optimization).
* **`simulation.py` (Model)**: Die Physik-Engine. Enthält den `@jit`-optimierten Algorithmus.
* **`interaction.py`**: Verwaltet die Regel-Matrix (wer zieht wen an?).
* **`visualisation.py` (View)**: Handhabt das OpenGL-Fenster und Inputs via `vispy`.

### 2. Performance-Optimierung (Numba)

Die größte Herausforderung ist die Berechnung der Kräfte zwischen allen Partikel-Paaren ().

* **Problem:** Reines Python ist für verschachtelte Schleifen zu langsam.
* **Lösung:** Wir nutzen den `@jit(nopython=True)` Dekorator von **Numba**.
* **Effekt:** Der Python-Bytecode wird zur Laufzeit in optimierten Maschinencode kompiliert.

### 3. Die Interaktions-Matrix

Die Regeln werden in einer asymmetrischen Matrix gespeichert.

* Ein Wert von `1.0` bedeutet maximale Anziehung.
* Ein Wert von `-1.0` bedeutet maximale Abstoßung.
* Das System ist **nicht newtonsch**: Wenn A von B angezogen wird, muss B nicht zwingend von A angezogen werden. Dies erzeugt das komplexe "Jagen"-Verhalten.

---

## 🧪 Testing & Qualitätssicherung

Das Projekt nutzt `pytest` für Unit-Tests und `ruff` für das Linting. Die Tests decken die physikalische Korrektheit und die Datenstrukturen ab.

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
