"""
Fill Line
=========
"""

import numpy
from MPSPlots.Render2D import Scene2D, Axis, FillLine


x = numpy.arange(100)
y0 = numpy.random.rand(100) + x
y1 = numpy.random.rand(100) - x

figure = Scene2D(
    unit_size=(8, 4),
    title='random data simple lines'
)

ax = Axis(
    row=0,
    col=0,
    x_label='x data',
    y_label='y data',
    show_legend=True
)

figure.add_axes(ax)

artist_0 = FillLine(
    x=x,
    y0=y0,
    y1=y1,
    label='Fill between lines',
    show_outline=True
)

_ = ax.add_artist(artist_0)

_ = figure.show()
