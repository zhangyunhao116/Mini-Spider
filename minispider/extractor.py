#!/usr/bin/env python
import json
import re
import os
import sys

from .sql import MiniSpiderSQL


class Extractor:
    def __init__(self, content=None):
        self.content = content
        self.SQL = MiniSpiderSQL()

    def run_extractor(self, pattern, mode):
        result = []
        match_list = re.findall(pattern, self.content)
        for i in match_list:
            if self._check_match_url(i):
                result.append(i)
        if mode == 'resource':
            self.SQL.insert_resource(result)
        elif mode == 'url':
            self.SQL.insert_resource(result)

    def make_extractor(self, extractor_name=None, pattern='', mode=''):
        if pattern and mode:
            # Make json data.
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
            # Save extractor.
            with open(extractor_name, mode='w') as f:
                f.write(s)
        else:
            return False

    def run_all_extractor(self):
        extractor_list = self._find_all_extractor()
        for name in extractor_list:
            with open(name, mode='r') as f:
                info = json.loads(f.read())
                self.run_extractor(info['pattern'], info['mode'])

    @staticmethod
    def _check_match_url(match_item):
        # Delete the url containing blank.
        temp = match_item.replace(' ', '')
        if len(temp) < len(match_item):
            return False
        return True

    @staticmethod
    def _find_all_extractor():
        file_list = os.listdir(sys.path[0])

        extractor_list = []
        for i in file_list:
            try:
                suffix_name = i.rsplit('.')[1]
            except IndexError:
                continue
            if suffix_name == 'extractor':
                extractor_list.append(i)

        return extractor_list
