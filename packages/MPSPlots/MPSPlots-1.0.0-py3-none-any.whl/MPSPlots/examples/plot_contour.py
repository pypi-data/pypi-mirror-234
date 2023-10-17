"""
Mesh
====
"""

import numpy
from MPSPlots.Render2D import SceneList

x_grid, y_grid = numpy.mgrid[0:100, 0:100]
scalar = x_grid**2 + y_grid**2

figure = SceneList(
    unit_size=(8, 4),
    title='random data contour line'
)

ax = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=False
)

_ = ax.add_contour(
    scalar=scalar,
    x=x_grid,
    y=y_grid,
    iso_values=0.1
)

_ = figure.show()

# -
