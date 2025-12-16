import numpy as np
from vispy import app, scene


class Visualizer:
    def __init__(self, simulation, width=800, height=800):
        self.simulation = simulation

        # ÄNDERUNG 1: Weißer Hintergrund
        self.canvas = scene.SceneCanvas(keys='interactive', size=(width, height), show=True, bgcolor='white')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, 1, 1))

        self.scatter = scene.visuals.Markers()
        self.view.add(self.scatter)

        base_colors = np.array([
            [1.0, 0.0, 0.0, 1.0],  # Rot
            [0.0, 1.0, 0.0, 1.0],  # Grün
            [0.0, 0.0, 1.0, 1.0],  # Blau
            [0.0, 0.0, 0.0, 1.0]  # Schwarz (statt Gelb, besser auf Weiß)
        ])
        self.particle_colors = base_colors[self.simulation.particles.types]

        self.timer = app.Timer(interval=1 / 60, connect=self.update, start=True)
        self.frame_count = 0

    def update(self, event):
        # ÄNDERUNG 2: Lebenszeichen in der Konsole
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            print(f"FPS Check: Frame {self.frame_count} - Physik läuft...")

        self.simulation.update_accelerations()
        self.simulation.update_velocities()
        self.simulation.update_positions()

        self.simulation.particles.positions %= 1.0

        # ÄNDERUNG 3: Größere Punkte (size=10)
        self.scatter.set_data(
            pos=self.simulation.particles.positions,
            edge_width=0,
            face_color=self.particle_colors,
            size=10
        )

    def run(self):
        app.run()