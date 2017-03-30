#!/usr/bin/env python
import json
import re
import os

from .sql import MiniSpiderSQL


class Extractor:
    def __init__(self, content=None):
        self.content = content
        self.SQL = MiniSpiderSQL()

    def run_extractor(self, pattern, mode, source, host=None):
        result = []
        match_list = re.findall(pattern, self.content)
        for i in match_list:
            # If it is a href,add host.
            if host:
                i = host + i
            result.append(i)
        if mode == 'resource':
            self.SQL.insert_resource(result, source)
        elif mode == 'url':
            self.SQL.insert_url(result)

    def make_extractor(self, extractor_name=None, pattern='', mode=''):
        if pattern and mode:
            host = None
            # If extract href url.
            if len(pattern) == 2:
                host = pattern[1]
                pattern = pattern[0]
            # Make json data.
            if host:
                info = {
                    'pattern': pattern,
                    'mode': mode,
                    'host': host
                }
            else:
                info = {
                    'pattern': pattern,
                    'mode': mode
                }
            s = json.dumps(info)
            # If name is None, make a name.
            if extractor_name is None:
                extractor_list = self._find_all_extractor()
                for i in range(1, 100):
                    extractor_name = str(i) + '.extractor'
                    if extractor_name not in extractor_list:
                        break
            else:
                # Add suffix name.
                extractor_name = extractor_name + '.extractor'
            # Save extractor.
            with open(extractor_name, mode='w') as f:
                f.write(s)
        else:
            return False

    def run_all_extractor(self, source=None):
        extractor_list = self._find_all_extractor()
        for name in extractor_list:
            with open(name, mode='r') as f:
                info = json.loads(f.read())
                # Check href extractor.
                if len(info) == 3:
                    self.run_extractor(info['pattern'], info['mode'], source, info['host'])
                else:
                    self.run_extractor(info['pattern'], info['mode'], source)

    @staticmethod
    def _find_all_extractor():
        file_list = os.listdir(os.getcwd())
        extractor_list = []
        for i in file_list:
            try:
                suffix_name = i.rsplit('.')[1]
            except IndexError:
                continue
            if suffix_name == 'extractor':
                extractor_list.append(i)

        return extractor_list
