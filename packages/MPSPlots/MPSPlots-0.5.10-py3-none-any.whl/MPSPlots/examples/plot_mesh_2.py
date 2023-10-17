"""
Mesh - Matrix
=============
"""

import numpy
from MPSPlots.Render2D import SceneMatrix

x, y, = numpy.mgrid[0:100, 0:100]

figure = SceneMatrix(
    unit_size=(4, 2),
    title='random data simple lines'
)

ax_0 = figure.append_ax(
    row=0,
    column=0,
    x_label='x data',
    y_label='y data',
    show_legend=False
)

ax_1 = figure.append_ax(
    row=1,
    column=0,
    x_label='x data',
    y_label='y data',
    show_legend=False
)


ax_2 = figure.append_ax(
    row=1,
    column=1,
    x_label='x data',
    y_label='y data',
    show_legend=False
)

_ = ax_0.add_mesh(
    scalar=x + y,
    x=x,
    y=y,
    show_colorbar=True
)

_ = ax_1.add_mesh(
    scalar=(x - 50)**2 + (y - 50)**2,
    x=x,
    y=y,
    show_colorbar=True
)

_ = ax_2.add_mesh(
    scalar=x**2 + y**2,
    x=x,
    y=y,
    show_colorbar=True
)


figure.show_colorbar = False

_ = figure.show()

# -
