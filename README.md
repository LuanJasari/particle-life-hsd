# 🧬 Particle Life Simulator

## Projektbeschreibung
Dieses Projekt implementiert eine "Particle Life"-Simulation in Python. Ziel ist es, **emergentes Verhalten** durch die Interaktion tausender Partikel zu simulieren. Das System basiert auf einfachen Regeln (Anziehung/Abstoßung), die komplexe, zell- oder lebensähnliche Strukturen erzeugen.

## Features
* **Simulation:** Dynamisches Partikelsystem mit >2000 Partikeln.
* **Interaktionen:** Definierbar über eine Interaktionsmatrix (Attraction/Repulsion).
* **Vielfalt:** Mindestens 4 verschiedene Partikeltypen (Farben).
* **Performance:** Optimierte Berechnung mittels **NumPy** (und optional **Numba** für JIT-Kompilierung).
* **Visualisierung:** Echtzeit-Darstellung via **Vispy** (GPU) oder **Pygame**.

## Setup & Installation

Stelle sicher, dass du Python 3.8+ installiert hast.

### Repository klonen und starten
Führe die folgenden Befehle in deinem Terminal aus:

```bash
git clone [https://github.com/LuanJasari/Biology-inspired-algorithms---emergent-behavier.git](https://github.com/LuanJasari/Biology-inspired-algorithms---emergent-behavier.git)
cd Biology-inspired-algorithms---emergent-behavier

pip install -r requirements.txt
python main.py
