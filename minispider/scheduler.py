#!/usr/bin/env python
import re
import urllib.request
import urllib.parse
import difflib
import json

from ssl import _create_unverified_context
from .sql import MiniSpiderSQL
from .extractor import Extractor


class MiniSpider:
    def __init__(self, original_url=None, timeout=2, search=(), ssl_context=None, url_check=True,
                 similarity_threshold=0.6,
                 display_number=100):
        # Parse chinese to ascii and delete parameters.
        self.url = original_url
        if self.url:
            self.url_check = url_check
            self._check_url()
            self.host = self.url.split('//')[0] + '//' + self.url.split('//')[1].split('/')[0]
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
        self.http_flag = 0

    def _url_read(self, url=None):
        if url is None:
            url = self.url

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as r:
            return self._content_decode(r.read())

    def _check_url(self):
        if self.url_check:
            # Add protocol if not exist.
            if self.url.split('://', 1)[0] not in ('http', 'https', 'ftp'):
                self.url = 'http://' + self.url
        # Parse chinese to ascii.
        self.url = urllib.parse.quote(self.url, safe='/:?=@&[]')

    def _handle_match(self, match_list):
        """ Handle match list by similarity threshold and add it to result."""
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
        tag_header = ''
        for index, item in enumerate(self.result):
            print('[%s]:' % index)
            not_print_flag = 1
            for i, j in enumerate(item):
                if i >= self.display_number:
                    if not_print_flag:
                        print('%s is not displayed' % (len(item) - self.display_number))
                        not_print_flag = 0
                    continue
                # Print tag url.
                if index >= self.http_flag:
                    if not tag_header:
                        tag_header = re.match('((?:[a-z]{0,10}\s*=\s*"))', j).group(0)
                    j = self.host + j.replace(tag_header, '')[0:-1]
                print('---(%s)%s' % (i, j))

    def _pattern_make_http(self):
        for i in self.search_list:
            temp = "http://\S+?\." + i
            self.pattern_list.append(temp)

    def _pattern_make_tag(self):
        for i in self.search_list:
            temp = '(?:[a-z]{0,10}\s*=\s*")/\S+\.%s\S*"' % i
            self.pattern_list.append(temp)

    @staticmethod
    def similar(str1, str2):
        if str1 == str2:
            return 1
        return float(difflib.SequenceMatcher(None, str1, str2).ratio())

    @staticmethod
    def _content_decode(content):
        charset = ('utf-8', 'gbk', 'gb2312', 'gb18030')
        for i in charset:
            try:
                return content.decode(i)
            except UnicodeDecodeError:
                pass

        raise Exception('Can not decode the url.')

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
        len_1 = len(str1)
        len_2 = len(str2)

        if len_1 >= len_2:
            length = len_2
        else:
            length = len_1

        for i in range(0, length):
            if str1[i] == str2[i]:
                continue
            else:
                return i

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
        return _url.rsplit('.', 1)[1].split('?')[0].replace('"', '')

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

        # Make http pattern.
        self._pattern_make_http()
        # Match http pattern.
        match_list = []
        for i in self.pattern_list:
            match = re.findall(i, content)
            for j in match:
                match_list.append(j)
            # Classify the url into certain types.
            self._handle_match(match_list)
            match_list = []
        # Get length of http pattern match list. First item is tag item.
        self.http_flag = len(self.result)

        # Delete http pattern.
        self.pattern_list = []

        # Make tag pattern.
        self._pattern_make_tag()
        # Match tag pattern.
        match_list = []
        for i in self.pattern_list:
            match = re.findall(i, content)
            for j in match:
                match_list.append(j)
            # Classify the url into certain types.
            self._handle_match(match_list)
            match_list = []

        # Check if not match.
        if not self.result:
            # Do some thing.
            print('Error!We find nothing!')
            return False

        # Save result、http_flag、host in temp file.
        temp = {
            'result': self.result,
            'http_flag': self.http_flag,
            'host': self.host
        }
        self._save_temp(temp)

        # Print result.
        self._display_result()

    def make_specific_http_pattern(self, specific_block_list):
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

        # If only one item,delete suffix name.
        if len(same_block) == len(specific_block_list[0]):
            latter_part = latter_part[0:len(latter_part) - len(self._get_suffix_name(specific_block_list[0])) - 1]

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
            char_supplement = '\S*'

        result_pattern = header + host + last_block + char_supplement + suffix_name

        return result_pattern

    def make_specific_tag_pattern(self, specific_block_list, host):
        """Make specific pattern for tag URL."""
        # Get longest match block.
        same_size = self.find_longest_size(specific_block_list)

        # Get same_block and it's length.
        same_block = specific_block_list[0][0:same_size]

        # Get header and delete header in same_block.
        header = re.match('((?:[a-z]{0,10}\s*=\s*"))', same_block).group(0)
        same_block = same_block.replace(header, '')
        same_length = len(same_block)

        # Get suffix name and add regular expression format.
        suffix_name = '\.' + self._get_suffix_name(specific_block_list[0])

        # If only one item,delete suffix name.
        if len(specific_block_list) == 1:
            same_block = same_block[0:same_length - len(self._get_suffix_name(specific_block_list[0])) - 2]

        # Make specific pattern.
        main_block = ''
        temp_block = ''
        for index, item in enumerate(same_block):
            temp = []
            if self._is_letter(item):
                temp.append('[a-z]')
            elif self._is_letter_capital(item):
                temp.append('[A-Z]')
            elif self._is_number(item):
                temp.append('[0-9]')
            else:
                temp.append(item)
            main_block = main_block + temp_block.join(temp)

        # Check if need supplement.
        if same_length == len(specific_block_list[0]):
            char_supplement = ''
        else:
            char_supplement = '\S*'

        pattern = header + '(' + main_block + char_supplement + suffix_name + ')' + '\S*"'
        return pattern, host

    def choose_block(self, num, start=None, end=None):
        # Choose block to make specific pattern. +1 used fix python array problem.
        block = self._read_temp()['result'][num]
        http_flag = self._read_temp()['http_flag']
        host = self._read_temp()['host']

        # Make tag pattern.
        if num >= http_flag:
            if start is not None and end is not None:
                specific_pattern = self.make_specific_tag_pattern(block[start:end + 1], host)
            elif start is not None:
                specific_pattern = self.make_specific_tag_pattern(block[start:start + 1], host)
            else:
                specific_pattern = self.make_specific_tag_pattern(block[0:], host)
        # Make http pattern.
        else:
            if start is not None and end is not None:
                specific_pattern = self.make_specific_http_pattern(block[start:end + 1])
            elif start is not None:
                specific_pattern = self.make_specific_http_pattern(block[start:start + 1])
            else:
                specific_pattern = self.make_specific_http_pattern(block[0:])

        return specific_pattern

    def start(self, url=None):
        # 1.Get url.
        if url is None:
            # If url is not provided, use SQL data.
            try:
                flag, url = MiniSpiderSQL().pop_url()
            except TypeError:
                raise Exception('Please input original url!')

        # 2.Read content.
        try:
            content = self._url_read(url)
            Extractor(content).run_all_extractor(0)
        except Exception as e:
            print(e)
        MiniSpiderSQL().display_all()

        # 3.Loop.
        while MiniSpiderSQL().num_available_url():
            flag, url = MiniSpiderSQL().pop_url()

            try:
                content = self._url_read(url)
                Extractor(content).run_all_extractor(flag)
            except Exception as e:
                MiniSpiderSQL().update_url_stats(flag, 1)
                print(e)

            MiniSpiderSQL().display_all()
