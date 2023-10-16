# Copyright (C) 2016-2023 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Generic definitions to implement cell plugins."""

import contextlib
import importlib
import logging
import os
import pkgutil
import sys

import jinja2

LOGGER = logging.getLogger("pypimonitor")


def load_cell_plugins():
    """Iterator over the cell plugins."""
    for _, name, _ in pkgutil.walk_packages(
        path=sys.modules[__name__].__path__, prefix=f"{__name__}."
    ):
        module = importlib.import_module(name)
        for attr in dir(module):
            obj = getattr(module, attr)
            if (
                isinstance(obj, type)
                and issubclass(obj, Cell)
                and obj.keyword is not None
            ):
                yield obj


@contextlib.contextmanager
def temp_update(source, update):
    """Temporary update of a dictionary."""
    bak = {}
    new = set()
    for key in update:
        if key not in source:
            new.add(key)
            source[key] = update[key]
    for key in source:
        if key in update:
            bak[key] = source[key]
            source[key] = update[key]

    yield source

    for key, value in bak.items():
        source[key] = value
    for key in new:
        del source[key]


class Cell:
    """Render some piece of information about a package as HTML code."""

    #: Keyword referencing the plugin, used in the :ref:`yaml` file to enable
    #: this plugin. If ``None``, the class is an abstract class that cannot be
    #: used directly.
    keyword = None

    #: Title of the column.
    title = ""

    #: Default values for package arguments. See :ref:`defaultrequired` for more details.
    default = {}

    #: List of names of required package arguments. See :ref:`defaultrequired` for more details.
    required = []

    def __init__(self, renderer):
        self.renderer = renderer
        self.config = renderer.config

    @jinja2.pass_context
    def __call__(self, context, cell, package):
        filled = self.default.copy()
        filled.update(self.config["packages"][package].get(cell, {}))

        # Detecting missing parameters
        missing = set()
        for key in self.required:
            if key not in filled:
                missing.add(key)
        if missing:
            return self.render_error(
                context,
                self.keyword,
                package,
                "Missing argument(s) {}.".format(  #  pylint: disable=consider-using-f-string
                    ", ".join([f"'{key}'" for key in missing])
                ),
            )

        return self.render(context, package, filled)

    def render(self, context, package, cell):
        """Return the HTML code corresponding to this cell.

        :param context: Current `Jinja2 context
            <http://jinja.pocoo.org/docs/dev/api/#jinja2.runtime.Context>`_.
        :param str package: Package name.
        :param dict cell: Package arguments for this cell.
        :rtype: str
        :return: The HTML code to display in the given cell.
        """
        raise NotImplementedError()

    @staticmethod
    def render_error(context, cell, package, message):
        """Return the HTML code corresponding to an error.

        :param context: Current `Jinja2 context
            <http://jinja.pocoo.org/docs/dev/api/#jinja2.runtime.Context>`_.
        :param str cell: Cell name (plugin keyword).
        :param str package: Package name.
        :param str message: Human readable error message.
        :rtype: str
        :return: The HTML code to display in the given cell.
        """
        full_message = f"Package '{package}', cell '{cell}': {message}"
        LOGGER.error(full_message)
        return context.environment.get_template(
            os.path.join("cells", "cellerror.html")
        ).render(message=full_message)


class Jinja2(Cell):
    """Generic class for cells that are barely more than a template.

    When this class is used to render a cell, it renders template
    ``self.keyword``. When doing so, the template has access to the following
    variables:

    - `package`: the name of the package being processed, as a string;
    - `pypi`: the information about this package got from pypi, as a dictionary
      (for instance https://pypi.org/pypi/pypimonitor/json);
    - `cell`: the cell options (as defined in the :ref:`yaml` configuration,
      maybe completed with :ref:`default values <defaultrequired>`) as a
      dictionary.
    """

    def render(self, context, package, cell):
        """Return the HTML code corresponding to this cell."""
        with temp_update(
            dict(context),
            {"package": package, "pypi": self.renderer[package], "cell": cell},
        ) as arguments:
            return context.environment.get_template(self.template).render(**arguments)

    @property
    def template(self):
        """Return template path.

        By default, this is ``cells/KEYWORD.html``. One can redefine this class
        to provide alternative template path.
        """
        return os.path.join("cells", f"{self.keyword}.html")
