from pipedocs.exporters import BaseExporter
from typing import List
import os
import json

class JsonFolderExporter(BaseExporter):
    def export(result: List[dict], exporter_name):
        if not os.path.exists(exporter_name):
            os.makedirs(exporter_name, exist_ok=True)

        for pipeline in result:
            filename = f"{exporter_name}/{pipeline['name']}.json"
            with open(filename, 'w') as f:
                f.write(json.dumps(pipeline, indent=4))
                print(f'JsonFolderExporter wrote file {filename}')
#