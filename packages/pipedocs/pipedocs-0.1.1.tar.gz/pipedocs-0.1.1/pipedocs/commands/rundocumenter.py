from pipedocs.commands import BaseRunCommand
from pipedocs.exceptions import UsageError
from pipedocs.importers import LocalImporter
from pipedocs.utils.misc import load_object
from pipedocs.documenters import Documenter

class Command(BaseRunCommand):
    requires_project = False
    default_settings = {}

    def syntax(self):
        return "[options] <documenter_file>"

    def short_desc(self):
        return "Run a self-contained documenter (without creating a project)"

    def long_desc(self):
        return "Run the documenter defined in the given file"

    def run(self, args, opts):
        documenter_classes = self._classes_from_args(class_=Documenter, class_name='Documenter', args=args, opts=opts)
        importer = LocalImporter(input=opts.input[0])
        resources_raw = importer.import_()

        documentercls = documenter_classes.pop()
        documenter = documentercls()
        resources = [documenter.parse_resource(r) for r in resources_raw]
        result = documenter.document(resources)

        for exporter_name in self.settings['EXPORTERS']:
            exporter_cls_name = self.settings['DOC_EXPORTERS'][self.settings['EXPORTERS'][exporter_name]['format']]
            exporter = load_object(exporter_cls_name)
            exporter.export(result, exporter_name)
