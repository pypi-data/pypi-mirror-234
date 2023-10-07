"""
Mesh
====
"""

import numpy
from MPSPlots.Render2D import SceneList

x = numpy.arange(100)
y = numpy.arange(100)
scalar = numpy.random.rand(100, 100)

figure = SceneList(
    unit_size=(8, 4),
    title='random data simple lines'
)

ax = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=False
)

_ = ax.add_mesh(
    scalar=scalar,
    x=x,
    y=y,
    show_colorbar=True
)

_ = figure.show()

# -
