#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_pdf import PdfPages

from MPSPlots.render2D.artist import *
from MPSPlots.render2D.scene import Scene2D, SceneList
from MPSPlots.render2D.axis import Axis


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig._mpl_figure.savefig(pp, format='pdf')

    pp.close()


# -
