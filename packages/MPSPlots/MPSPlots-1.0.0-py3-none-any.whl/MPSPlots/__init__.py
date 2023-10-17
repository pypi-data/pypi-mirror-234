from MPSPlots.tools.directories import style_directory
import matplotlib.pyplot as plt


def use_mpsplots_style():
    plt.style.use(style_directory.joinpath('mps_plot.mplstyle'))


def use_new_age_style():
    plt.style.use(style_directory.joinpath('new_age.mplstyle'))


def use_ggplot_style():
    # plt.style.use('ggplot')
    plt.style.use(style_directory.joinpath('ggplot.mplstyle'))


def use_default_style():
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.rcParams["font.family"] = "serif"


use_ggplot_style()  # default

# -
