"""
Simple Line plus Scatter plot
=============================
"""

import numpy
from MPSPlots.Render2D import SceneList


x = numpy.arange(100)
y0 = numpy.random.rand(100)
y1 = numpy.random.rand(100)

figure = SceneList(
    unit_size=(8, 4),
    title='random data simple lines'
)

ax = figure.append_ax(
    x_label='x data',
    y_label='y data',
    show_legend=True,
    line_width=2
)

_ = ax.add_line(x=x, y=y0, label='line 0')
_ = ax.add_scatter(x=x, y=y0, label='line 1')

_ = figure.show()
