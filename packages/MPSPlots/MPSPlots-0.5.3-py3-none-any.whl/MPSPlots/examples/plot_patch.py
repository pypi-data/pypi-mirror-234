"""
STD line
========
"""

import numpy
from MPSPlots.Render2D import SceneList


x = numpy.arange(100)
y = numpy.random.rand(10, 100)
y_mean = numpy.mean(y, axis=0)
y_std = numpy.std(y, axis=0)

figure = SceneList(
    unit_size=(8, 4),
    title='Polygon'
)

ax = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=True
)

coordinates = [(0, 0), (0, 1), (1, 1), (1, 1)]

_ = ax.add_polygon(
    coordinates=coordinates,
    edgecolor='black',
    facecolor='red'
)

_ = figure.show()
