#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Matplotlib imports
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path

# Other imports
import numpy
import shapely.geometry as geo
from itertools import cycle
from dataclasses import dataclass
import MPSPlots
from MPSPlots import colormaps

MPSPlots.use_ggplot_style()

linecycler = cycle(["-", "--", "-.", ":"])


@dataclass
class Colorbar:
    discreet: bool = False
    """ Buggy feature """
    position: str = 'right'
    """ Position of the colorbar """
    orientation: str = "vertical"
    """ Orientation of the colorbar """
    symmetric: bool = False
    """ Set symmetric colormap """
    log_norm: bool = False
    """ Log normalization of the colorbar """
    numeric_format: str = '%.3f'
    """ Format for the ticks on the colorbar """
    n_ticks: int = None
    """ Number of ticks for the colorbar """
    label_size: int = None
    """ Label size of the colorbar """
    size: str = "10%"
    """ Width of the colorbar """

    def _render_(self, ax) -> None:
        divider = make_axes_locatable(ax._ax)

        colorbar_ax = divider.append_axes(
            self.position,
            size=self.size,
            pad=0.15
        )

        cbar = plt.colorbar(
            mappable=ax._ax.collections[0],
            norm=None,
            cax=colorbar_ax,
            orientation=self.orientation,
            format=self.numeric_format
        )

        if self.n_ticks is not None:
            cbar.ax.locator_params(nbins=self.n_ticks)

        if self.n_ticks is not None:
            cbar.ax.tick_params(labelsize=self.label_size)


@dataclass
class Contour():
    x: numpy.ndarray
    """ y axis, can be vector or 2D grid """
    y: numpy.ndarray
    """ x axis, can be vector or 2D grid """
    scalar: numpy.ndarray
    """ Scalar 2D field """
    iso_values: numpy.ndarray
    """ Level values to which plot the iso contours """
    colormap: str = None
    """ Colormap to use for plottings """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def __post_init__(self):
        if self.colormap is None:
            self.colormap = colormaps.blue_black_red

    def _render_(self, ax) -> None:
        ax._ax.contour(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            level=self.iso_values,
            colors="black",
            linewidth=.5,
            zorder=self.layer_position
        )

        ax._ax.contourf(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            level=self.iso_values,
            cmap=self.colormap,
            zorder=self.layer_position
        )


@dataclass
class Mesh():
    scalar: numpy.ndarray
    """ 2 dimensional numpy array representing the mesh to be plotted """
    colormap: str = None
    """ Colormap to be used for the plot """
    x: numpy.ndarray = None
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    y: numpy.ndarray = None
    """ Array representing the y axis, if not defined a numpy arrange is used instead """
    show_colorbar: bool = False
    """ Boolean option to show or not the colorbar of the mesh """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """
    colormap_norm: object = None
    """ Norm object for the colormap """
    colorbar: Colorbar = None
    """ Colorbar object for the mesh """

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.scalar.shape[1])

        if self.y is None:
            self.y = numpy.arange(self.scalar.shape[0])

        if self.colorbar is None:
            self.colorbar = Colorbar()

        if self.colormap is None:
            self.colormap = colormaps.blue_black_red

    def _render_(self, ax):
        image = ax._ax.pcolormesh(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            self.scalar,
            cmap=self.colormap,
            shading='auto',
            zorder=self.layer_position,
            norm=self.colormap_norm
        )

        image.set_edgecolor('face')

        if self.show_colorbar:

            self.colorbar._render_(ax=ax)
            return image, ax.colorbar

        return image


@dataclass
class Polygon():
    instance: object
    """ Shapely geo instance representing the polygone to be plotted """
    name: str = ''
    """ Name to be added to the plot next to the polygon """
    alpha: float = 0.4
    """ Opacity of the polygon to be plotted """
    facecolor: str = 'lightblue'
    """ Color for the interior of the polygon """
    edgecolor: str = 'black'
    """ Color for the border of the polygon """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def _render_(self, ax) -> None:
        if isinstance(self.instance, geo.MultiPolygon):
            for polygon in self.instance.geoms:
                self.add_polygon_to_ax(polygon, ax)

        else:
            self.add_polygon_to_ax(self.instance, ax)

    def add_polygon_to_ax(self, polygon, ax, add_name: str = None):
        collection = self.get_polygon_path(polygon)

        ax._ax.add_collection(collection, autolim=True)

        ax._ax.autoscale_view()

        if add_name:
            ax._ax.scatter(polygon.centroid.x, polygon.centroid.y)
            ax._ax.text(polygon.centroid.x, polygon.centroid.y, self.name)

    def get_polygon_path(self, polygon):
        exterior_coordinate = numpy.asarray(polygon.exterior.coords)

        exterior_coordinate[:, 0] *= self.x_scale_factor
        exterior_coordinate[:, 1] *= self.y_scale_factor

        path_exterior = Path(exterior_coordinate)

        path_interior = []
        for ring in polygon.interiors:
            interior_coordinate = numpy.asarray(ring.coords)
            path_interior.append(Path(interior_coordinate))

        path = Path.make_compound_path(
            path_exterior,
            *path_interior
        )

        patch = PathPatch(path)

        collection = PatchCollection(
            [patch],
            alpha=self.alpha,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor
        )

        return collection


@dataclass
class FillLine():
    x: numpy.ndarray
    """ Array representing the x axis """
    y0: numpy.ndarray
    """ Array representing the inferior y axis to be filled with color """
    y1: numpy.ndarray
    """ Array representing the superior y axis to be filled with color """
    label: str = ""
    color: str = None
    """ Color for the fill """
    line_style: str = None
    """ Line style for the unique line default is next in cycle """
    line_width: float = 1
    """ Line width of the artists """
    show_outline: bool = True
    """ Show the outline of the filling """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def _render_(self, ax) -> None:
        if self.line_style is None:
            self.line_style = next(linecycler)

        ax._ax.fill_between(
            self.x * self.x_scale_factor,
            self.y0 * self.y_scale_factor,
            self.y1 * self.y_scale_factor,
            color=self.color,
            linestyle=self.line_style,
            alpha=0.7,
            label=self.label,
            zorder=self.layer_position
        )

        if self.show_outline:
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y1 * self.y_scale_factor,
                color='k',
                linestyle='-',
                linewidth=self.line_width,
                zorder=self.layer_position
            )

            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y0 * self.y_scale_factor,
                color='k',
                linestyle='-',
                linewidth=self.line_width,
                zorder=self.layer_position
            )


@dataclass
class STDLine():
    x: numpy.ndarray
    """ Array representing the x axis """
    y_mean: numpy.ndarray
    """ Array representing the mean value of y axis """
    y_std: numpy.ndarray
    """ Array representing the standard deviation value of y axis """
    label: str = ""
    """ Label to be added to the plot """
    color: str = None
    """ Color for the artist to be ploted """
    line_style: str = None
    """ Line style for the y_mean line default is straight lines '-' """
    line_width: float = 1
    """ Line width of the artists """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def _render_(self, ax):
        if self.line_style is None:
            self.line_style = '-'

        y0 = self.y_mean - self.y_std / 2
        y1 = self.y_mean + self.y_std / 2

        line = ax._ax.plot(
            self.x * self.x_scale_factor,
            self.y_mean * self.y_scale_factor,
            color=self.color,
            linestyle=self.line_style,
            linewidth=self.line_width,
            zorder=self.layer_position
        )

        ax._ax.fill_between(
            self.x * self.x_scale_factor,
            y0 * self.y_scale_factor,
            y1 * self.y_scale_factor,
            color=line[-1].get_color(),
            linestyle='-',
            alpha=0.3,
            label=self.label,
            zorder=self.layer_position
        )


@dataclass
class Line():
    y: numpy.ndarray
    """ Array representing the y axis """
    x: numpy.ndarray = None
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    label: str = None
    """ Label to be added to the plot """
    color: str = None
    """ Color for the artist to be ploted """
    line_style: str = '-'
    """ Line style for the unique line default is next in cycle """
    line_width: float = 1
    """ Line width of the artists """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.y.size)

        self.y = numpy.asarray(self.y)
        self.x = numpy.asarray(self.x)

    def _render_(self, ax):
        if isinstance(self.line_style, str) and self.line_style.lower() == 'random':
            self.line_style = next(linecycler)

        if numpy.iscomplexobj(self.y):
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y.real * self.y_scale_factor,
                label=self.label + "[real]",
                color=self.color,
                linestyle=self.line_style,
                linewidth=self.line_width,
                zorder=self.layer_position
            )

            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y.imag * self.y_scale_factor,
                label=self.label + "[imag]",
                color=self.color,
                linestyle=self.line_style,
                linewidth=self.line_width,
                zorder=self.layer_position
            )

        else:
            ax._ax.plot(
                self.x * self.x_scale_factor,
                self.y * self.y_scale_factor,
                label=self.label,
                color=self.color,
                linestyle=self.line_style,
                linewidth=self.line_width,
                zorder=self.layer_position
            )


@dataclass
class VerticalLine():
    x: float
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    y_min: float = None
    """ Array representing the y axis """
    y_max: float = None
    """ Array representing the y axis """
    label: str = None
    """ Label to be added to the plot """
    color: str = None
    """ Color for the artist to be ploted """
    line_style: str = '-'
    """ Line style for the unique line default is next in cycle """
    line_width: float = 1
    """ Line width of the artists """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def _render_(self, ax):
        if isinstance(self.line_style, str) and self.line_style.lower() == 'random':
            self.line_style = next(linecycler)

        ax._ax.vlines(
            x=self.x * self.x_scale_factor,
            ymin=self.y_min,
            ymax=self.y_max,
            colors=self.color,
            label=self.label,
            linestyle=self.line_style,
            linewidth=self.line_width,
            zorder=self.layer_position
        )


@dataclass
class Scatter():
    y: numpy.ndarray
    """ Array representing the y axis """
    x: numpy.ndarray = None
    """ Array representing the x axis, if not defined a numpy arrange is used instead """
    label: str = None
    """ Label to be added to the plot """
    color: str = 'black'
    """ Color for the artist to be ploted """
    marker: str = 'o'
    """ Line style for the unique line default is next in cycle """
    marker_size: float = 4
    """ Size of the markers """
    line_style: str = 'None'
    """ Line style for the unique line default is next in cycle """
    line_width: str = 1
    """ Line style for the unique line default is next in cycle """
    alpha: float = 0.4
    """ Opacity of the polygon to be plotted """
    edge_color: str = 'black'
    """ Scatter edge color """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    layer_position: int = 1
    """ Position of the layer """

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.y.size)

        self.y = numpy.asarray(self.y)
        self.x = numpy.asarray(self.x)

    def _render_(self, ax):
        ax._ax.scatter(
            self.x * self.x_scale_factor,
            self.y * self.y_scale_factor,
            label=self.label,
            color=self.color,
            marker=self.marker,
            s=self.marker_size,
            edgecolor=self.edge_color,
            linestyle=self.line_style,
            linewidth=self.line_width,
            alpha=self.alpha,
            zorder=self.layer_position
        )


@dataclass
class Text():
    position: tuple = (0.0, 0.0)
    """ Box position of the text """
    font_size: int = 8
    """ Font size of the text """
    weight: str = 'normal'
    """ Weight of the text """
    color: str = 'black'
    """ Color of the text """
    text: str = ''
    """ String to be plotted """
    add_box: bool = False
    """ Boolean to enable a box around the text """
    layer_position: int = 1
    """ Position of the layer """
    localisation: str = 'lower right'

    def _render_(self, ax):
        artist = AnchoredText(
            self.text,
            loc=self.localisation,
            prop=dict(size=self.font_size, color=self.color, weight=self.weight, position=(0, 0)),
            frameon=self.add_box,
            bbox_to_anchor=self.position,
            # bbox_transform=ax._ax.transAxes,#ax._ax.transData,
            borderpad=0,
        )

        ax._ax.get_figure().add_artist(artist)


@dataclass
class PatchPolygon():
    coordinates: numpy.ndarray = None
    """ Coordinate of the vertices """
    name: str = ''
    """ Name to be added to the plot next to the polygon """
    alpha: float = 0.4
    """ Opacity of the polygon to be plotted """
    facecolor: str = 'lightblue'
    """ Color for the interior of the polygon """
    edgecolor: str = 'black'
    """ Color for the border of the polygon """
    x_scale_factor: float = 1
    """ Scaling factor for the x axis """
    y_scale_factor: float = 1
    """ Scaling factor for the y axis """
    label: str = None
    """ Label to be added to the plot """

    def __post_init__(self):
        self.coordinates = numpy.asarray(self.coordinates)
        self.coordinates[:, 0] *= self.x_scale_factor
        self.coordinates[:, 1] *= self.y_scale_factor

    def _render_(self, ax) -> None:
        polygon = plt.Polygon(
            self.coordinates,
            facecolor=self.facecolor,
            alpha=self.alpha,
            edgecolor=self.edgecolor,
            label=self.label
        )

        ax._ax.add_patch(polygon)

        ax._ax.autoscale_view()


if __name__ == '__main__':
    from MPSPlots.render2D import SceneList
    figure = SceneList(tight_layout=True)

    ax = figure.append_ax(y_label='Y label')

    ax.add_scatter(
        x=[0, 1, 2, 3],
        y=[0, 1, 2, 3],
        marker='o',
        label='test',
        color='black',
        marker_size=100,
        edge_color='red',
        line_width=3

    )

    ax.add_line(
        x=[0, 1, 2, 3],
        y=[0, 1, 2, 3],
        label='test',
        color='black',
        line_width=3

    )

    ax.add_text(
        position=(1, 0),
        text='test text',
        add_box=True,
        color='red',
        weight='bold'

    )

    ax.add_polygon(
        coordinates=[[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]],
        x_scale_factor=2,
    )

    figure.show()
# -
