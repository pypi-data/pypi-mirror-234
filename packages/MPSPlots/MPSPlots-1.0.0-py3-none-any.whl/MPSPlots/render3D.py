#   !/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import pyvista
import numpy
import matplotlib
from MPSPlots import colormaps


@dataclass
class UnstructuredMesh():
    coordinates: numpy.ndarray
    scalar: numpy.ndarray
    color_map: str = None
    symmetric_map: bool = True
    scalar_bar_args: dict = None

    def __post_init__(self):
        if self.colormap is None:
            self.colormap = colormaps.blue_black_red

    def _render_(self, figure, subplot: tuple):
        figure.subplot(*subplot)
        self.coordinates = numpy.array(self.coordinates).T
        points = pyvista.wrap(self.coordinates)

        if self.symmetric_map:
            max_abs = numpy.abs(self.scalar).max()
            if max_abs == 0:
                color_map_limit = [-1, 1]
            else:
                color_map_limit = [-max_abs, max_abs]
        else:
            color_map_limit = None

        figure.add_points(
            points,
            scalars=self.scalar,
            point_size=20,
            render_points_as_spheres=True,
            cmap=self.color_map,
            clim=color_map_limit,
            scalar_bar_args=self.scalar_bar_args
        )


class Scene3D:
    def __init__(self,
                 shape: tuple = (1, 1),
                 unit_size: tuple = (800, 800),
                 window_size: tuple = None,
                 background_color: str = 'white',
                 **kwargs):

        if window_size is None:
            window_size = (unit_size[1] * shape[1], unit_size[0] * shape[0])

        self.figure = pyvista.Plotter(
            theme=pyvista.themes.DocumentTheme(),
            window_size=window_size,
            shape=shape,
            **kwargs
        )

        self.figure.set_background(background_color)

    def add_unstructured_mesh(self, *args, **kwargs) -> None:
        """
        Adds an unstructured mesh to a plot. The  unstructured data is represented
        with 3d points in the volume. If scalars is given then the colormap is used.

        :param      args:    The arguments
        :type       args:    list
        :param      kwargs:  The keywords arguments
        :type       kwargs:  dictionary

        :returns:   No return
        :rtype:     None
        """
        if kwargs.get('scalar', None) is not None:
            return self.add_unstructured_mesh_with_scalar(*args, **kwargs)
        else:
            return self.add_unstructured_mesh_without_scalar(*args, **kwargs)

    def get_color_map_limit(self, scalar: numpy.ndarray, symmetric_map: bool):
        if symmetric_map:
            max_abs = numpy.abs(scalar).max()
            if max_abs == 0:
                color_map_limit = [-1, 1]
            else:
                color_map_limit = [-max_abs, max_abs]
        else:
            color_map_limit = None

        return color_map_limit

    def add_unstructured_mesh_with_scalar(self,
                                          coordinates: numpy.ndarray,
                                          scalar: numpy.ndarray = None,
                                          plot_number: tuple = (0, 0),
                                          color_map: str = colormaps.blue_black_red,
                                          scalar_bar_args: dict = None,
                                          symmetric_map: bool = True) -> None:

        self.figure.subplot(*plot_number)

        points = pyvista.wrap(coordinates)

        color_map_limit = self.get_color_map_limit(scalar=scalar, symmetric_map=symmetric_map)

        self.figure.add_points(
            points,
            scalars=scalar,
            point_size=20,
            render_points_as_spheres=True,
            cmap=color_map,
            clim=color_map_limit,
            scalar_bar_args=scalar_bar_args
        )

    def add_unstructured_mesh_without_scalar(self, coordinates: numpy.ndarray, plot_number: tuple = (0, 0)) -> None:
        self.figure.subplot(*plot_number)

        points = pyvista.wrap(coordinates)

        self.figure.add_points(
            points,
            point_size=20,
            render_points_as_spheres=True,
            cmap='white'
        )

    def add_mesh(self,
                 x: numpy.ndarray,
                 y: numpy.ndarray,
                 z: numpy.ndarray,
                 plot_number: tuple = (0, 0),
                 color_map: str = colormaps.blue_black_red,
                 **kwargs) -> None:

        if isinstance(color_map, str):  # works only for matplotlib 3.6.1
            color_map = matplotlib.colormaps[color_map]

        self.figure.subplot(*plot_number)

        mesh = pyvista.StructuredGrid(x, y, z)

        self.figure.add_mesh(
            mesh=mesh,
            cmap=color_map,
            style='surface',
            **kwargs
        )

        return self.figure

    def get_spherical_vector_from_coordinates(self, phi: numpy.ndarray, theta: numpy.ndarray, component: str, radius: float = 1.0):
        if component.lower() == 'theta':
            vector = [1, 0, 0]
        elif component.lower() == 'phi':
            vector = [0, 1, 0]
        elif component.lower() == 'r':
            vector = [0, 0, 1]

        x, y, z = pyvista.transform_vectors_sph_to_cart(theta, phi, radius, *vector)

        return numpy.c_[x.ravel(), y.ravel(), z.ravel()]

    def add_spherical_component_vector_to_ax(self, plot_number: tuple,
                                                   component: str,
                                                   theta: numpy.ndarray,
                                                   phi: numpy.ndarray,
                                                   radius: float = 1.03 / 2) -> None:
        self.figure.subplot(*plot_number)

        vector = self.get_spherical_vector_from_coordinates(
            phi=phi,
            theta=theta,
            component=component,
            radius=radius
        )

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, radius)

        spherical_vector.point_data["component"] = vector * 0.1

        vectors = spherical_vector.glyph(
            orient="component",
            scale="component",
            tolerance=0.005
        )

        self.figure.add_mesh(vectors, color='k')

    def add_theta_vector_field(self, plot_number: list, radius: float = 1.03 / 2) -> None:
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        self.add_spherical_component_vector_to_ax(
            plot_number=plot_number,
            component='theta',
            radius=radius,
            phi=phi,
            theta=theta
        )

    def add_phi_vector_field(self, plot_number: tuple, radius: float = 1.03 / 2) -> None:
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        self.add_spherical_component_vector_to_ax(
            plot_number=plot_number,
            component='phi',
            radius=radius,
            phi=phi,
            theta=theta
        )

    def add_r_vector_field(self, plot_number: tuple, radius: float = [1.03 / 2]) -> None:
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        self.add_spherical_component_vector_to_ax(
            plot_number=plot_number,
            component='r',
            radius=radius,
            phi=phi,
            theta=theta
        )

    def add_unit_sphere_to_ax(self, plot_number: tuple = (0, 0)):
        self.figure.subplot(*plot_number)
        sphere = pyvista.Sphere(radius=1)
        self.figure.add_mesh(sphere, opacity=0.3)

    def add_unit_axes_to_ax(self, plot_number: tuple = (0, 0)):
        self.figure.subplot(*plot_number)
        self.figure.add_axes_at_origin(labels_off=True)

    def add_text_to_axes(self, plot_number: tuple = (0, 0), text='', **kwargs):
        self.figure.subplot(*plot_number)
        self.figure.add_text(text, **kwargs)

    def show(self, save_directory: str = None, window_size: tuple = (1200, 600)):
        self.figure.show(
            screenshot=save_directory,
            window_size=window_size,
        )

        return self

    def close(self):
        self.figure.close()
