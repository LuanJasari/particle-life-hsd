# 🧬 Particle Life Simulator

## Projektbeschreibung
Dieses Projekt implementiert eine **Particle-Life-Simulation** in Python. Ziel ist es, **emergentes Verhalten** durch die Interaktion tausender Partikel zu simulieren. Das System basiert auf einfachen Regeln wie Anziehung und Abstoßung, die dennoch komplexe, zell- oder lebensähnliche Strukturen erzeugen.

## Features
- **Simulation:** Dynamisches Partikelsystem mit mehr als 2000 Partikeln  
- **Interaktionen:** Steuerbar über eine Interaktionsmatrix (Attraction/Repulsion)  
- **Vielfalt:** Mindestens 4 verschiedene Partikeltypen  
- **Performance:** Optimiert mit **NumPy**, optional **Numba** (JIT)  
- **Visualisierung:** Echtzeit-Rendering über **Vispy** (GPU) oder **Pygame**


## Software Architektur

Das Projekt folgt einem datenorientierten Design (Data-Oriented Design), um Python-Performance-Limits zu umgehen:

* **ParticleSystem:** Verwaltet die Zustandsdaten (Positionen, Geschwindigkeiten, Typen) in flachen, zusammenhängenden NumPy-Arrays (SoA - Structure of Arrays). Dies maximiert Cache-Lokalität.
* **Interaction:** Berechnet eine vorberechnete Lookup-Matrix für Interaktionsregeln, um zur Laufzeit O(1) Zugriffe auf Kraft-Koeffizienten zu ermöglichen.
* **Simulation (Physics Engine):**
    * Die kritische Pfadberechnung (O(N^2) Interaktionen) wurde mittels **Numba JIT (Just-In-Time Compiler)** optimiert.
    * Der Python-Bytecode wird zur Laufzeit in optimierten Maschinen-Code kompiliert.
    * Dadurch erreichen wir C++ ähnliche Performance und können >1500 Partikel bei 60 FPS simulieren.
* **Visualizer:** Entkoppeltes Frontend basierend auf `vispy` (OpenGL), das die NumPy-Arrays direkt auf die GPU mapped, ohne teures Kopieren von Objekten.

## Setup & Installation

### Voraussetzungen
- Python **3.8+**

## Steuerung / Konfiguration

- **SPACE**: Simulation pausieren/fortsetzen  
- **R**: Simulation zurücksetzen  
- **ESC**: Beenden  

Die Parameter der Interaktionsmatrix können in `config.py` angepasst werden.

## Team
- Baoevran  
- tjdrjsdl  
- LuanJasari  
- Tymauricee

### Repository klonen und starten
```bash
git clone https://github.com/LuanJasari/particle-life-hsd.git
cd particle-life-hsd

pip install -r requirements.txt
python main.py

