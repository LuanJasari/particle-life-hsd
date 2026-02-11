import numpy as np
from vispy import app, scene


class Visualizer:
    def __init__(self, simulation, width=800, height=800):
        self.simulation = simulation

        # Weißer Hintergrund für bessere Sichtbarkeit
        self.canvas = scene.SceneCanvas(keys='interactive', size=(width, height), show=True, bgcolor='white')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, 1, 1))

        self.scatter = scene.visuals.Markers()
        self.view.add(self.scatter)

        base_colors = np.array([
            [1.0, 0.0, 0.0, 1.0],  # Rot
            [0.0, 1.0, 0.0, 1.0],  # Grün
            [0.0, 0.0, 1.0, 1.0],  # Blau
            [0.0, 0.0, 0.0, 1.0]   # Schwarz
        ])
        self.particle_colors = base_colors[self.simulation.particles.types]

        self.timer = app.Timer(interval=1 / 60, connect=self.update, start=True)
        self.frame_count = 0

    def update(self, event):
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            print(f"FPS Check: Frame {self.frame_count} - Physik läuft...")

        # Aufruf der Physik-Engine
        self.simulation.update_accelerations()
        self.simulation.update_velocities()
        self.simulation.update_positions()

        # REDUNDANZ ENTFERNT: Das Wrapping erfolgt jetzt in simulation.py

        # Aktualisierung der Darstellung mit größeren Punkten
        self.scatter.set_data(
            pos=self.simulation.particles.positions,
            edge_width=0,
            face_color=self.particle_colors,
            size=10
        )

    def run(self):
        app.run()
