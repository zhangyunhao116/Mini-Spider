#!/usr/bin/env python
import re
import urllib.request
import urllib.parse
import difflib
import json

from ssl import _create_unverified_context
from .sql import MiniSpiderSQL

class MiniSpider:
    def __init__(self, original_url=None, timeout=2, search=(), ssl_context=None, url_check=False,
                 similarity_threshold=0.6,
                 display_number=20):
        # Parse chinese to ascii and delete parameters.
        if original_url:
            self.url = original_url
            self.url_check = url_check
            self._check_url()
            self.host = 'http://' + original_url.split('//')[1].split('/')[0]
        # Create ssl context.
        if ssl_context:
            self.ssl_context = ssl_context
        else:
            self.ssl_context = _create_unverified_context()
        # Initialization parameters.
        self.temp_file_name = 'mini-spider.temp'
        self.timeout = timeout
        self.similarity_threshold = similarity_threshold
        self.pattern_list = []
        self.search_list = self._initialize_search(search)
        self.display_number = display_number
        self.result = []

    def _url_read(self):
        req = urllib.request.Request(self.url)
        with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as r:
            temp = r.read()
            temp = self._content_decode(temp)
            return temp

    def _check_url(self):
        if self.url_check:
            # Add protocol if not exist.
            if self.url.split('://', 1)[0] != 'http' or 'https':
                self.url = 'http://' + self.url
        # Parse chinese to ascii.
        self.url = urllib.parse.quote(self.url, safe='/:?=@&[]')

    def _handle_match(self, match_list):
        # If match_list = [], return False.
        if len(match_list) == 0:
            return False

        # Eliminate duplicate and sort().
        match_list = self.duplicate_eliminate(match_list)
        match_list.sort()

        # If match_list only have one item.
        if len(match_list) == 1:
            self.result.append(match_list)
            return True

        # Handle.
        temp = []
        flag = 0

        for index, item in enumerate(match_list):
            if self.similar(match_list[flag], item) >= self.similarity_threshold:
                temp.append(item)
                continue
            else:
                flag = index
                self.result.append(temp)
                temp = []
                temp.append(item)
        if len(temp):
            self.result.append(temp)

    def _display_result(self):
        for index, item in enumerate(self.result):
            print('[%s]:' % index)
            flag = 1
            for i, j in enumerate(item):
                if i >= self.display_number:
                    if flag:
                        print('%s is not displayed' % (len(item) - self.display_number))
                        flag = 0
                    continue
                print('---(%s)%s' % (i, j))

    def _pattern_make(self):
        for i in self.search_list:
            temp = "http://.+?\." + i
            self.pattern_list.append(temp)

    @staticmethod
    def similar(str1, str2):
        if str1 == str2:
            return 1
        return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

    @staticmethod
    def _check_match_url(match_item):
        # Delete the url containing blank.
        temp = match_item.replace(' ', '')
        if len(temp) < len(match_item):
            return False
        return True

    @staticmethod
    def _content_decode(content):
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return content.decode('gbk')
            except UnicodeDecodeError:
                return content.decode('gb2312')

    @staticmethod
    def _initialize_search(search):
        temp = []
        if type(search) == str:
            temp.append(search)
            return temp
        for i in search:
            temp.append(i)
        return temp

    def find_longest_size(self, match_list):
        # If only one item, return.
        if len(match_list) == 1:
            return len(match_list[0])

        size = len(match_list[0])
        for index, item in enumerate(match_list):
            if index == len(match_list) - 1:
                break
            temp = self._find_longest_match(item, match_list[index + 1])
            if temp < size:
                size = temp

        return size

    @staticmethod
    def _find_longest_match(str1, str2):
        o = difflib.SequenceMatcher(isjunk=None, a=str1, b=str2)
        return o.find_longest_match(0, len(str1), 0, len(str2))[2]

    @staticmethod
    def _is_letter(match_str):
        pattern = '[a-z]'
        if re.findall(pattern, match_str):
            return True
        else:
            return False

    @staticmethod
    def _is_letter_capital(match_str):
        pattern = '[A-Z]'
        if re.findall(pattern, match_str):
            return True
        else:
            return False

    @staticmethod
    def _is_number(match_str):
        pattern = '[0-9]'
        if re.findall(pattern, match_str):
            return True
        else:
            return False

    @staticmethod
    def _get_suffix_name(_url):
        return _url.rsplit('.', 1)[1]

    @staticmethod
    def duplicate_eliminate(list_input):
        """ Delete all duplicate in a list."""
        result = []
        for i in list_input:
            if i not in result:
                result.append(i)

        return result

    def _save_temp(self, content_list):
        s = json.dumps(content_list)
        with open(self.temp_file_name, mode='w') as f:
            f.write(s)

    def _read_temp(self):
        with open(self.temp_file_name, mode='r') as f:
            result = json.loads(f.read())
        return result

    def analysis_url(self):
        # Read URL content.
        content = self._url_read()
        # Make pattern.
        self._pattern_make()

        match_list = []
        for i in self.pattern_list:
            match = re.findall(i, content)
            for j in match:
                if self._check_match_url(j):
                    match_list.append(j)
            # Classify the url into certain types.
            self._handle_match(match_list)
            match_list = []
        # Check if not match.
        if not self.result:
            # Do some thing.
            print('Error!We find nothing!')
            return False

        # Save result in temp file.
        self._save_temp(self.result)

        # Print result.
        self._display_result()

    def make_specific_pattern(self, specific_block_list):
        """Make specific pattern for entire URL."""
        # Get longest match block.
        same_size = self.find_longest_size(specific_block_list)

        # Get same_block.
        same_block = specific_block_list[0][0:same_size]

        # Get suffix name and add regular expression format.
        suffix_name = '\.' + self._get_suffix_name(specific_block_list[0])

        # Split same block.
        header = same_block.split('//')[0] + '//'
        latter_part = same_block.split('//')[1]
        # Split latter part.
        latter_part_list = latter_part.split('/')
        host = latter_part_list[0]
        # Make specific pattern.
        last_block = ''
        for index, item in enumerate(latter_part_list):
            temp = []
            if index == 0:
                continue
            for j in item:
                if self._is_letter(j):
                    temp.append('[a-z]')
                elif self._is_letter_capital(j):
                    temp.append('[A-Z]')
                elif self._is_number(j):
                    temp.append('[0-9]')
                else:
                    temp.append(j)
            # Format list.
            pass

            pattern_block = ''.join(temp)
            last_block = last_block + '/' + pattern_block
        # Check if need supplement.
        if len(same_block) == len(specific_block_list[0]):
            char_supplement = ''
        else:
            char_supplement = '.+?'

        result_pattern = header + host + last_block + char_supplement + suffix_name

        return result_pattern

    def choose_block(self, num, start=0, end=None):
        block = self._read_temp()[num]
        if end is None:
            end = len(block)
        elif start != end:
            # Fix python list do not include end.
            end += 1

        if start == end:
            # Use one item make specific pattern.
            specific_pattern = self.make_specific_pattern(block[start:start + 1])
        else:
            # Use list make specific pattern.
            specific_pattern = self.make_specific_pattern(block[start:end])

        return specific_pattern

    def start(self):
        if self.url is None:
            # If url is not provided, use SQL data.
            url = MiniSpiderSQL().pop_url()
        else:
            url = self.url
        if url is None:
            return False

