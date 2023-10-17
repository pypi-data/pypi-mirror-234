#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Matplotlib imports
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Other imports
import numpy
from dataclasses import dataclass
import MPSPlots
from MPSPlots.render2D.axis import Axis

MPSPlots.use_ggplot_style()


class SceneProperties:
    def ax_inherit(function):
        def wrapper(self, value):
            for ax in self:
                setattr(ax, function.__name__, value)

        return wrapper

    @ax_inherit
    def x_scale_factor(self, value: int):
        pass

    @ax_inherit
    def y_scale_factor(self, value: int):
        pass

    @ax_inherit
    def font_size(self, value: int):
        pass

    @ax_inherit
    def line_width(self, value: int):
        pass

    @ax_inherit
    def line_style(self, value: int):
        pass

    @ax_inherit
    def legend_font_size(self, value: int):
        pass

    @ax_inherit
    def tick_size(self, value: int):
        pass

    @ax_inherit
    def x_limits(self, value: list):
        pass

    @ax_inherit
    def y_limits(self, value: list):
        pass

    @ax_inherit
    def x_label(self, value: list):
        pass

    @ax_inherit
    def y_label(self, value: list):
        pass

    @ax_inherit
    def water_mark(self, value: str):
        pass

    @ax_inherit
    def equal(self, value: bool):
        pass

    @ax_inherit
    def equal_limits(self, value: bool):
        pass

    @ax_inherit
    def show_legend(self, value: bool):
        pass

    @ax_inherit
    def show_grid(self, value: bool):
        pass

    @ax_inherit
    def show_ticks(self, value: bool):
        pass

    @ax_inherit
    def show_colorbar(self, value: int):
        pass

    def colorbar_n_ticks(self, value: int):
        for ax in self:
            ax.colorbar.n_ticks = value

    def colorbar_label_size(self, value: int):
        for ax in self:
            ax.colorbar.label_size = value

    font_size = property(None, font_size)
    line_width = property(None, line_width)
    line_style = property(None, line_style)
    legend_font_size = property(None, legend_font_size)
    tick_size = property(None, tick_size)
    x_limits = property(None, x_limits)
    y_limits = property(None, y_limits)
    x_scale_factor = property(None, x_scale_factor)
    y_scale_factor = property(None, y_scale_factor)
    x_label = property(None, x_label)
    y_label = property(None, y_label)
    water_mark = property(None, water_mark)
    equal = property(None, equal)
    equal_limits = property(None, equal_limits)
    show_legend = property(None, show_legend)
    show_grid = property(None, show_grid)
    show_ticks = property(None, show_ticks)
    show_colorbar = property(None, show_colorbar)
    colorbar_n_ticks = property(None, colorbar_n_ticks)
    colorbar_label_size = property(None, colorbar_label_size)

    @property
    def shape(self) -> numpy.ndarray:
        return numpy.array([self.number_of_column, self.number_of_row])

    @property
    def maximum_column_value(self) -> int:
        column_values = [ax.col for ax in self]
        return numpy.array(column_values).max()

    @property
    def maximum_row_value(self) -> int:
        row_values = [ax.row for ax in self]
        return numpy.array(row_values).max()

    @property
    def number_of_column(self) -> int:
        return self.maximum_column_value + 1

    @property
    def number_of_row(self) -> int:
        return self.maximum_row_value + 1

    def close(self) -> None:
        plt.close(self._mpl_figure)

    def save_figure(self, save_directory: str, **kwargs):
        plt.savefig(
            fname=save_directory,
            transparent=self.transparent_background,
            **kwargs
        )

    def show(self, save_directory: str = None, **kwargs):
        self._render_()
        if save_directory is not None:
            self.save_figure(save_directory=save_directory, **kwargs)

        # plt.legend(["algo1", "algo2", "algo3"], loc=1)
        # plt.legend(handles=None, labels=["hello there"], loc=2)

        plt.show()

        return self

    def _render_(self):
        """
        Renders the object.
        """
        if not self._axis_generated:
            self._generate_axis_()

        for ax in self._mpl_axis_list:
            ax._render_()

        if self.tight_layout:
            plt.tight_layout()

        return self

    def __getitem__(self, idx: int) -> Axis:
        """
        Returns ax from the SceneList

        :param      idx:  The index
        :type       idx:  int

        :returns:   axis corresponding to idx
        :rtype:     Axis
        """
        return self._mpl_axis_list[idx]

    def generate_mpl_figure(self) -> None:
        figure_size = self.shape * numpy.array(self.unit_size)
        self._mpl_figure = plt.figure(figsize=figure_size)
        self._mpl_figure.suptitle(self.title)

    # def __setitem__(self, idx: int, value) -> None:
    #     assert isinstance(value, MPSPlots.render2D.axis.Axis), f"Cannot assign type: {value.__class__} to Scene2D axis"
    #     self._axis[idx] = value

    # def __add__(self, other):
    #     assert isinstance(other, SceneMatrix), f"Cannot add two different classes {self.__class__} and {other.__class__}"
    #     for ax in other._axis:
    #         self.append_axis(ax)

    #     return self


@dataclass
class SceneList(SceneProperties):
    unit_size: tuple = (10, 3)
    tight_layout: bool = True
    transparent_background: bool = False
    title: str = ""
    ax_orientation: str = 'vertical'

    def __post_init__(self):
        self._mpl_axis_list = []
        self._axis_generated = False

    @property
    def next_row_number(self) -> int:
        if self.ax_orientation == 'horizontal':
            row_number = 0
        elif self.ax_orientation == 'vertical':
            row_number = len(self._mpl_axis_list)

        return row_number

    @property
    def next_column_number(self) -> int:
        if self.ax_orientation == 'horizontal':
            column_number = len(self._mpl_axis_list)
        elif self.ax_orientation == 'vertical':
            column_number = 0

        return column_number

    def append_ax(self, **ax_kwargs: dict) -> None:
        """
        Appends axis to the list.

        :param      ax:   The axis to append to scene
        :type       ax:   Axis

        :returns:   No returns
        :rtype:     None
        """
        axis = Axis(
            col=self.next_column_number,
            row=self.next_row_number,
            **ax_kwargs
        )

        self._mpl_axis_list.append(axis)

        return axis

    def _generate_axis_(self):
        self.generate_mpl_figure()

        grid = gridspec.GridSpec(
            ncols=self.number_of_column,
            nrows=self.number_of_row,
            figure=self._mpl_figure
        )

        for axis in self._mpl_axis_list:
            subplot = self._mpl_figure.add_subplot(
                grid[axis.row, axis.col],
                projection=axis.projection
            )

            axis._ax = subplot

        self.axis_generated = True

        return self


@dataclass
class SceneMatrix(SceneProperties):
    unit_size: tuple = (10, 3)
    tight_layout: bool = True
    transparent_background: bool = False
    title: str = ""

    def __post_init__(self):
        self._mpl_axis_list = []
        self._axis_generated = False

    def set_axis_row(self, value) -> None:
        for ax in self._mpl_axis_list:
            ax.row = value

    def set_axis_col(self, value) -> None:
        for ax in self._mpl_axis_list:
            ax.col = value

    def set_style(self, **style_dict):
        for ax in self:
            ax.set_style(**style_dict)

        return self

    @property
    def axis_matrix(self):
        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)
        for ax in self._mpl_axis_list:
            ax_matrix[ax.row, ax.col] = ax

        return ax_matrix

    def append_ax(self, row: int, column: int, **ax_kwargs: dict) -> None:
        """
        Appends axis to the list.

        :param      ax:   The axis to append to scene
        :type       ax:   Axis

        :returns:   No returns
        :rtype:     None
        """
        axis = Axis(
            col=column,
            row=row,
            **ax_kwargs
        )

        self._mpl_axis_list.append(axis)

        return axis

    def _generate_axis_(self):
        self.generate_mpl_figure()

        grid = gridspec.GridSpec(
            ncols=self.number_of_column,
            nrows=self.number_of_row,
            figure=self._mpl_figure
        )

        ax_matrix = numpy.full(
            shape=(self.number_of_row, self.number_of_column),
            fill_value=None
        )

        for axis in self._mpl_axis_list:
            subplot = self._mpl_figure.add_subplot(grid[axis.row, axis.col], projection=axis.projection)
            ax_matrix[axis.row, axis.col] = subplot
            axis._ax = subplot

        self.axis_generated = True

        return self


# -
