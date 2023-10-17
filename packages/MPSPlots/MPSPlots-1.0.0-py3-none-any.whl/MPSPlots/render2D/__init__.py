#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MPSPlots.render2D.artist import *
from MPSPlots.render2D.scene import SceneMatrix, SceneList
from MPSPlots.render2D.axis import Axis
from matplotlib.backends.backend_pdf import PdfPages


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig._mpl_figure.savefig(pp, format='pdf')

    pp.close()
