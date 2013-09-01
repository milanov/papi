import shutil
from os.path import exists, join
from os import mkdir
from genshi.template import MarkupTemplate


class HTMLOutput():

    def __init__(self, resource, destination, format, theme_dir):
        self._resource = resource
        self._destination = destination
        self._format = format
        self._theme_dir = theme_dir

    def generate(self):
        self._copy_resources()
        for module in self._resource.modules:
            self._generate_resource(module)
            for cls in module.classes:
                self._generate_resource(cls, isclass=True)

    def _copy_resources(self):
        doc_dir = join(self._destination, self._resource.docsdir)
        if exists(doc_dir):
            shutil.rmtree(doc_dir)
        mkdir(doc_dir)
        shutil.copytree(join(self._theme_dir, "css"), join(doc_dir, "css"))
        shutil.copytree(join(self._theme_dir, "js"), join(doc_dir, "js"))
        shutil.copytree(join(self._theme_dir, "img"), join(doc_dir, "img"))

    def _generate_resource(self, res, isclass=False):
        template_file = "class.html" if isclass else "module.html"

        templatedir_path = join(self._theme_dir, template_file)
        with open(templatedir_path, 'r') as content_file:
            content = content_file.read()
        tmpl = MarkupTemplate(content)
        stream = tmpl.generate(resource=res,
                               module_tree=self._resource.module_tree,
                               project_name=self._resource.name)

        resource_path = join(self._destination,
                             self._resource.docsdir, res.name + '.html')
        f = open(resource_path, 'w+')
        f.write(stream.render('xhtml'))
        f.close()
