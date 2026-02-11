import numpy as np
from vispy import app, scene

class Visualizer:
    def __init__(self, simulation, width=800, height=800):
        self.simulation = simulation
        self.canvas = scene.SceneCanvas(keys='interactive', size=(width, height), show=True, bgcolor='white')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, 1, 1))

        self.scatter = scene.visuals.Markers()
        self.view.add(self.scatter)

        base_colors = np.array([
            [1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 0.0, 1.0]
        ])
        self.particle_colors = base_colors[self.simulation.particles.types]
        self.timer = app.Timer(interval=1/60, connect=self.update, start=True)
        self.frame_count = 0

    def update(self, event):
        self.frame_count += 1
        self.simulation.update_positions() # Ruft sim.step() auf

        self.scatter.set_data(
            pos=self.simulation.particles.positions,
            edge_width=0,
            face_color=self.particle_colors,
            size=10
        )

    def run(self):
        app.run()
