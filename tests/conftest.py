import os

# Zwingt Numba, den JIT-Compiler zu umgehen und als reines Python zu laufen.
# Dies sichert 100% Sichtbarkeit für das Coverage-Tool.
os.environ["NUMBA_DISABLE_JIT"] = "1"
