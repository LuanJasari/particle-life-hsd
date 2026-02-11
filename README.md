# 🧬 Particle Life Simulator

## Projektbeschreibung
Dieses Projekt implementiert eine **Particle-Life-Simulation** in Python. Ziel ist es, **emergentes Verhalten** durch die Interaktion tausender Partikel zu simulieren. Das System basiert auf einfachen Regeln wie Anziehung und Abstoßung, die dennoch komplexe, zell- oder lebensähnliche Strukturen erzeugen.

## Features
- **Simulation:** Dynamisches Partikelsystem mit mehr als 2000 Partikeln  
- **Interaktionen:** Steuerbar über eine Interaktionsmatrix (Attraction/Repulsion)  
- **Vielfalt:** Mindestens 4 verschiedene Partikeltypen  
- **Performance:** Optimiert mit **NumPy**, optional **Numba** (JIT)  
- **Visualisierung:** Echtzeit-Rendering über **Vispy** (GPU) oder **Pygame**

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

