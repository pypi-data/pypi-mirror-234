from typing import List
import glob
import json

from pipedocs.importers.base import BaseImporter

class LocalImporter(BaseImporter):
    def __init__(self, input):
        self.input = input

    def import_(self) -> List[dict]:
        resources_raw = []
        for filename in glob.glob(f'{self.input}/**/*.json', recursive=True):
            #print(f'>>>> filename {filename}')
            with open(filename, 'r') as f:
                content = f.read()
            assert len(content) > 0
            r = json.loads(content)
            assert type(r) == dict
            resources_raw.append(r)
        return resources_raw
