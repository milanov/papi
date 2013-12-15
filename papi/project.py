import pkgutil
import inspect
import shutil
import sys
import logging
from os import getcwd, mkdir
from os.path import exists, isfile, basename, join
from os.path import dirname, abspath, splitext, isdir

from papi.helpers import *
from papi.resource_objects import Resource, ModuleObject, SimpleModuleObject
from papi.output_generators import html_output


logger = logging.getLogger(__name__)
DEFAULT_OUTPUT_FORMAT = "html"
DEFAULT_DOCFORMAT = "reStructuredText"
DEFAULT_THEME = "default"


class Papi():

    """
    The documentation ``Papi`` class.

    """

    def __init__(self, options):
        self._theme_dir = self._get_theme_dir(options.theme)
        output_format = options.output_format
        self._output_generator = self._get_output_generator(output_format)
        self._format = options.format
        self._destination = self._get_output_destination(options.destination)
        self._resources = []

        for resource in expand_paths(options.resources):
            is_resource = isfile(resource) or ispackage_path(resource)
            if exists(resource) and is_resource:
                resource = Resource(resource)
                self._resources.append(resource)
            else:
                warning = "Resouce %s is not a package or module." % resource
                logger.warning(warning)

    def generate(self):
        for res in self._resources:
            format = self._format
            dest = self._destination
            theme_dir = self._theme_dir
            generator = self._output_generator(res, dest, format, theme_dir)
            generator.generate()

    def open_in_browser(self):
        """
        Open a generated project's documentation in
        the system's default web browser.
        """
        import webbrowser
        from urllib.request import pathname2url
        for res in self._resources:
            pathname = join(self._destination, res.docsdir, res.name + '.html')
            res_url = pathname2url(pathname)
            webbrowser.open(res_url)

    def _get_output_generator(self, output_format):
        generators = {'html': html_output.HTMLOutput}
        if output_format not in generators:
            warning = 'Invalid output format: %s' % output_format
            logger.warning(warning)
            output_format = DEFAULT_OUTPUT_FORMAT

        return generators[output_format]

    def _get_output_destination(self, destination):
        destination = abspath(destination)
        if not (destination and exists(destination) and isdir(destination)):
            destination = getcwd()

        return destination

    def _get_theme_dir(self, theme_name):
        templates_dir = join(dirname(abspath(__file__)), "templates")
        theme_dir = join(templates_dir, theme_name)
        if not exists(theme_dir) or not isdir(theme_dir):
            theme_dir = join(templates_dir, DEFAULT_THEME)
        return theme_dir
