==============================================================
cell-tracking-BC: Base Classes for Cell Tracking in Microscopy
==============================================================



Brief Description
=================

The ``cell-tracking-BC`` project proposes a set of classes and tools for the processing and analysis of cell microscopy time-lapses/videos, typically in live-cell imaging. Its purpose is to serve as a basis for the development of computational pipelines and applications, for example to detect cell-related events such as division or death.



Installation
============

The ``cell-tracking-BC`` project is published on the `Python Package Index (PyPI) <https://pypi.org>`_ at: `https://pypi.org/project/cell-tracking-bc <https://pypi.org/project/cell-tracking-bc>`_. It requires version 3.8, or newer, of the interpreter. It should be installable from Python distribution platforms or Integrated Development Environments (IDEs). Otherwise, it can be installed from a command-line console:

- For all users, after acquiring administrative rights:
    - First installation: ``pip install cell-tracking-bc``
    - Installation update: ``pip install --upgrade cell-tracking-bc``
- For the current user (no administrative rights required):
    - First installation: ``pip install --user cell-tracking-bc``
    - Installation update: ``pip install --user --upgrade cell-tracking-bc``



Documentation
=============

The documentation is extremely limited at the moment. It currently takes the form of a `small PDF document <https://gitlab.inria.fr/edebreuv/cell-tracking-bc/-/raw/master/documentation/latex/main.pdf>`_. The tools `pdoc3 <https://pdoc3.github.io/pdoc>`_ and `pydoctor <https://github.com/twisted/pydoctor>`_ are also used to generate an `API documentation <https://edebreuv.gitlabpages.inria.fr/cell-tracking-bc>`_.



Thanks
======

The project is developed with `PyCharm Community <https://www.jetbrains.com/pycharm>`_.

The development relies on several open-source packages (see ``install_requires`` in ``setup.py``).

The code is formatted by `Black <https://github.com/psf/black>`_, *The Uncompromising Code Formatter*.

The imports are ordered by `isort <https://github.com/timothycrosley/isort>`_... *your imports, so you don't have to*.
