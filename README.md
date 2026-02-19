# 🧬 Particle Life Simulator (High-Performance Edition)
## 📄 Projektbeschreibung

Dieses Projekt implementiert eine hochperformante Particle-Life-Simulation im Rahmen des Moduls „Data Science und KI Infrastrukturen“. Ziel ist die Simulation emergenten Verhaltens durch die Interaktion tausender Partikel auf Basis einfacher physikalischer Regeln (Anziehung und Abstoßung).

Die Software wurde mit besonderem Fokus auf Performance (Numba JIT), saubere Architektur (Model-View-Pattern) und GPU-beschleunigte Visualisierung (Vispy/OpenGL) entwickelt.

## 🧠 Physikalische Logik

Die Simulation basiert auf einem vereinfachten, nicht-newtonschen Partikelmodell mit periodischen Randbedingungen (Torus-Geometrie).

### 1️⃣ Geometrie – Periodische Randbedingungen

Es existieren keine Wände. Stattdessen wird eine Torus-Topologie verwendet:

Verlässt ein Partikel rechts den Raum, erscheint es links wieder. Verlässt es oben den Raum, erscheint es unten wieder. Kräfte wirken ebenfalls über die Randgrenzen hinweg. Die Distanz wird stets als kürzester Weg auf dem Torus berechnet.

### 2️⃣ Kraftmodell

Für zwei Partikel i und j gilt:

F(r) = A_ij * (1 - r / R),  für r < R
F(r) = 0                 sonst


Dabei gilt:

r = Abstand zwischen Partikeln

R = max_r (Interaktionsradius)

A_ij = Eintrag in der Interaktionsmatrix

**Eigenschaften des Modells:**

Lineare Kraftabnahme

Keine Singularität bei r → 0

Numerisch stabil

Kompakte Wechselwirkungszone

Asymmetrische Interaktionen erlaubt

**Das System ist bewusst nicht newtonsch:**

Wenn A von B angezogen wird, muss B nicht zwingend von A angezogen werden.
Dies erzeugt das charakteristische „Jagen“-Verhalten und komplexe emergente Muster.

### 3️⃣ Numerische Integration

Die Bewegungsgleichungen werden mittels explizitem Euler-Verfahren integriert:

v(t+1) = (1 - γ dt) v(t) + F dt
x(t+1) = x(t) + v(t+1) dt


Dabei:

γ = friction (Dämpfung)

dt = Zeitschritt

Die Dämpfung sorgt für Stabilität und verhindert Energieexplosion.

#
### 4️⃣ Algorithmische Komplexität

Die Kraftberechnung erfolgt paarweise:

O(N²)


Das bedeutet:

Jeder Partikel interagiert mit jedem anderen. Für N Partikel entstehen N² Interaktionen pro Frame.

Durch Nutzung von Numba JIT (nopython=True) wird der Python-Overhead vollständig eliminiert, wodurch C++-ähnliche Performance erreicht wird.

## 🚀 Features

Massive Simulation: Flüssige Berechnung von 2.000 Partikeln in Echtzeit

High-Performance Backend: numpy + numba

GPU-Rendering: vispy (OpenGL)

Interaktive Parametersteuerung

Unit-Tests mit pytest

Continuous Integration via GitHub Actions

Clean Code & modulare Architektur

## 📊 Performance Benchmarks
**Test-Szenario**:

1.500 Partikel

200 Zeitschritte (Headless Mode)

O(N²) Interaktionen

**Ergebnisse**:

Durchschnittliche Framerate: 80.40 FPS

Berechnungszeit pro Frame: ~12 ms

99% der Rechenzeit innerhalb des kompilierten JIT-Kernels

Kein messbarer Python-Interpreter-Overhead

## 🛠 Installation & Setup
### Voraussetzungen

Python 3.12

Git im System-Pfad

Virtuelle Umgebung (venv oder conda)

OpenGL-fähiger Grafiktreiber

### Installation
pip install git+https://github.com/LuanJasari/particle-life-hsd.git


### Starten:

particle-life

## 🎮 Steuerung (GUI)
**Taste	Funktion	Beschreibung**
SPACE	Pause / Play	Stoppt oder startet die Zeit
F	Reibung +	Erhöht die Dämpfung
G	Reibung -	Verringert die Dämpfung
R	Radius +	Vergrößert max_r
T	Radius -	Verkleinert max_r
M	Matrix Shuffle	Neue zufällige Interaktionsmatrix
ESC	Beenden	Schließt das Fenster

Der aktuelle Status (FPS, Reibung, Radius) wird im Fenstertitel angezeigt.

## ⚙️ Architektur (Model-View-Pattern)
*main.py*:

Initialisiert Simulation und Visualizer.

*particles.py*:

Verwaltet Zustandsarrays:

Positionen (Nx2 NumPy Array)

Geschwindigkeiten (Nx2 NumPy Array)

Typen (N Array)

Keine Python-Objekte pro Partikel → Speicheroptimierung.

*simulation.py* (Model):

Enthält den JIT-kompilierten Physik-Kernel.

*interaction.py*:

Verwaltet die asymmetrische Interaktionsmatrix.

*visualisation.py* (View):

OpenGL-Rendering und Input-Handling via vispy.

## 🧪 Testing & Qualitätssicherung

### Unit-Tests mit pytest:

poetry run pytest --cov=particle_life_simulator


### Linting mit ruff:

poetry run ruff check .

## 👥 Team

Baoevran

tjdrjsdl

LuanJasari

Tymauricee
