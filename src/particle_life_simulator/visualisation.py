import numpy as np
from vispy import app, scene

class Visualizer:
    """
    Visualisiert die Partikel-Simulation in Echtzeit mittels Vispy (OpenGL).
    
    Diese Klasse trennt die Darstellung (View) von der Physik (Model).
    Sie handhabt das Rendering der Partikel sowie die Benutzereingaben
    zur Steuerung der Simulationsparameter.
    """

    def __init__(self, simulation, width=800, height=800):
        """
        Initialisiert das Visualisierungs-Fenster und die Szene.
 
        Args:
            simulation (Simulation): Die Instanz der Physik-Simulation.
            width (int, optional): Breite des Fensters in Pixeln. Default: 800.
            height (int, optional): Höhe des Fensters in Pixeln. Default: 800.
        """
        self.simulation = simulation
        
        #interaktivität
        self.canvas = scene.SceneCanvas(keys='interactive', size=(width, height), show=True, bgcolor='black')
        self.canvas.title = "Particle Life - Press 'H' for Help"
        
        # View und Kamera einrichten
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, 1, 1))

        # Partikel-Visualisierung 
        self.scatter = scene.visuals.Markers()
        self.view.add(self.scatter) 

        # Farben vorbereiten (Mapping von Typ-ID zu RGBA)
        # 0=Rot, 1=Grün, 2=Blau, 3=weiß
        base_colors = np.array([
            [1.0, 0.2, 0.2, 1.0],  # Rot
            [0.2, 1.0, 0.2, 1.0],  # Grün
            [0.2, 0.2, 1.0, 1.0],  # Blau
            [1.0, 1.0, 1.0, 1.0]   # Weiß
        ])
        
        # Wir speichern die Farben basierend auf den Typen der Partikel
        self.particle_colors = base_colors[self.simulation.particles.types]
        
        # Timer für die Animationsschleife (ca. 60 FPS)
        self.timer = app.Timer(interval=1/60, connect=self.update, start=True)
        self.frame_count = 0

        # Tastatur-Events verknüpfen
        self.canvas.events.key_press.connect(self.on_key_press)
        
        print("--> [Visualizer] Fenster gestartet. Drücke 'H' für Steuerung.")

    def on_key_press(self, event):
        """
        Verarbeitet Tastatureingaben zur Steuerung der Simulation (Simple GUI).
        
        Args:
            event: Das KeyPress-Event von Vispy.
        """
        # 1. Pause
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
                self.canvas.title = "PAUSED"
            else:
                self.timer.start()
        
        # 2. Reibung ändern
        elif event.text == 'f':
            self.simulation.friction = min(1.0, self.simulation.friction + 0.05)
            print(f"Friction erhöht: {self.simulation.friction:.2f}")
        elif event.text == 'g':
            self.simulation.friction = max(0.0, self.simulation.friction - 0.05)
            print(f"Friction verringert: {self.simulation.friction:.2f}")

        # 3. Radius (Max_R) ändern
        elif event.text == 'r':
            self.simulation.max_r = min(0.5, self.simulation.max_r + 0.01)
            print(f"Max Radius erhöht: {self.simulation.max_r:.2f}")
        elif event.text == 't':
            self.simulation.max_r = max(0.01, self.simulation.max_r - 0.01)
            print(f"Max Radius verringert: {self.simulation.max_r:.2f}")

        # 4. Interaktionsmatrix neu würfeln (Chaos-Modus)
        elif event.text == 'm':
            print("Zufällige neue Regeln generiert!")
            n_types = self.simulation.interaction.num_types
            # Generiert Werte zwischen -1 und 1
            new_matrix = np.random.uniform(-1.0, 1.0, (n_types, n_types))
            self.simulation.interaction.matrix = new_matrix

        # 5. Hilfe ausgeben
        elif event.text == 'h':
            print("=== STEUERUNG ===")
            print("[SPACE] Pause/Play")
            print("[f] / [g] Reibung +/-")
            print("[r] / [t] Radius +/-")
            print("[m]     Neue Zufalls-Regeln (Matrix)")
            print("[ESC]   Beenden")

    def update(self, event):
        """
        Die Hauptschleife der Visualisierung.
        
        Wird vom Timer aufgerufen, berechnet den nächsten Physik-Schritt
        und aktualisiert die Grafik.
        
        Args:
            event: Timer-Event (enthält Zeitdelta etc.)
        """
        self.frame_count += 1
        
        # Physik berechnen (Model update)
        self.simulation.update_positions()

        # Grafik aktualisieren
        self.scatter.set_data(
            pos=self.simulation.particles.positions,
            edge_width=0,
            face_color=self.particle_colors,
            size=8
        )
        
        # Status im Fenstertitel anzeigen
        if self.frame_count % 30 == 0:
            fps = self.canvas.fps
            title = (f"FPS: {fps:.1f} | "
                     f"Friction: {self.simulation.friction:.2f} | "
                     f"Radius: {self.simulation.max_r:.2f}")
            self.canvas.title = title

    def run(self):
        """Startet die Vispy-Applikation."""
        app.run()
