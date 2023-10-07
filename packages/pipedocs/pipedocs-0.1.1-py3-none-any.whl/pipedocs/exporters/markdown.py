from pipedocs.exporters import BaseExporter

class MarkdownExporter(BaseExporter):
    def export(result: str, exporter_name):
        # TODO: create location if it doesn't exist
        with open(exporter_name, 'w') as f:
            f.write(result)
