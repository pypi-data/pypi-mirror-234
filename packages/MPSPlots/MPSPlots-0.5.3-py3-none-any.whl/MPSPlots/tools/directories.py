#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import MPSPlots


__all__ = [
    'root_path',
    'project_path',
    'example_directory',
    'doc_path',
    'doc_css_path',
    'style_directory',
    'logo_path',
    'version_path',
    'examples_path',
]

root_path = Path(MPSPlots.__path__[0])

project_path = root_path.parents[0]

example_directory = root_path.joinpath('examples')

doc_path = root_path.parents[0].joinpath('docs')

doc_css_path = doc_path.joinpath('source/_static/default.css')

style_directory = root_path.joinpath('styles')

logo_path = doc_path.joinpath('images/logo.png')

version_path = root_path.joinpath('VERSION')

examples_path = root_path.joinpath('examples')


if __name__ == '__main__':
    for path_name in __all__:
        path = locals()[path_name]
        print(path)
        assert path.exists(), f"Path {path_name} do not exists"

# -
