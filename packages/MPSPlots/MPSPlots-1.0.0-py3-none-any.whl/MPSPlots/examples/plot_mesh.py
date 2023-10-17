"""
Mesh - Line
===========
"""

import numpy
from MPSPlots.Render2D import SceneList

x, y, = numpy.mgrid[0:100, 0:100]

figure = SceneList(
    unit_size=(8, 4),
    title='random data simple lines'
)

ax_0 = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=False
)

ax_1 = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=False
)

artist_0 = ax_0.add_mesh(
    scalar=x + y,
    x=x,
    y=y,
    show_colorbar=True
)


artist_1 = ax_1.add_mesh(
    scalar=x**2,
    x=x,
    y=y,
    show_colorbar=True
)

_ = figure.show()

# -
