from typing import List

from pipedocs.commands import BaseRunCommand
from pipedocs.exceptions import UsageError
from pipedocs.importers import LocalImporter
from pipedocs.utils.misc import load_object
from pipedocs.generators import Generator

class Command(BaseRunCommand):
    requires_project = False
    default_settings = {}

    def syntax(self):
        return "[options] <generator_file>"

    def short_desc(self):
        return "Run a self-contained generator (without creating a project)"

    def long_desc(self):
        return "Run the generator defined in the given file"

    def run(self, args, opts):
        generator_classes = self._classes_from_args(class_=Generator, class_name='Generator', args=args, opts=opts)
        importer = LocalImporter(input=opts.input[0])
        pipeline_definitions: List[dict] = importer.import_()

        generatorcls = generator_classes.pop()
        generator = generatorcls()
        result: List[dict] = generator.generate(pipeline_definitions)

        for exporter_name in self.settings['EXPORTERS']:
            exporter_cls_name = self.settings['DOC_EXPORTERS'][self.settings['EXPORTERS'][exporter_name]['format']]
            exporter = load_object(exporter_cls_name)
            exporter.export(result, exporter_name)
