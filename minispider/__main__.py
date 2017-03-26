#!/usr/bin/env python
import re
import urllib.request
import urllib.parse
import difflib
import argparse

from ssl import _create_unverified_context
from .sql import MiniSpiderSQL


class MiniSpider:
    def __init__(self, original_url, timeout=2, search=(), ssl_context=None, url_check=False, similarity_threshold=0.6,
                 display_number=10):
        # Parse chinese to ascii and delete parameters.
        self.url = original_url
        self.url_check = url_check
        self._check_url()
        # Create ssl context.
        if ssl_context:
            self.ssl_context = ssl_context
        else:
            self.ssl_context = _create_unverified_context()
        # Get Host.
        self.host = 'http://' + original_url.split('//')[1].split('/')[0]
        # Initialization parameters.
        self.timeout = timeout
        self.similarity_threshold = similarity_threshold
        self.pattern_list = []
        self.search_list = self._initialize_search(search)
        self.display_number = display_number
        # Initialize SQL.
        self.SQL = MiniSpiderSQL()

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
        # Temp function, need rewrite.
        match_list.sort()
        # Patch.
        if len(match_list) == 1:
            temp = []
            temp.append(match_list)
            return temp
        result = []
        flag = 0
        for index, item in enumerate(match_list):
            if self.similar(item, match_list[flag]) > self.similarity_threshold:
                if index == len(match_list) - 1 and flag == 0:
                    result.append('*')
                    for k in range(flag, index):
                        result.append(match_list[k])
                    flag = index
            else:
                result.append('*')
                for k in range(flag, index):
                    result.append(match_list[k])
                flag = index
        just_one = 0
        result_format = []
        temp = []
        for index, item in enumerate(result):
            if index == 0:
                continue
            if item == '*':
                just_one += 1
                result_format.append(temp)
                temp = []
                continue
            temp.append(item)
        if just_one == 0:
            result_format.append(temp)
        return result_format

    def _display_result(self, result):
        for index, item in enumerate(result):
            print('[%s]:' % index)
            flag = 1
            for i, j in enumerate(item):
                if i >= self.display_number:
                    if flag:
                        print('%s is not displayed' % (len(item) - self.display_number))
                        flag = 0
                    continue
                print('   %s' % j)

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

    @staticmethod
    def find_longest_match(match_list):
        a = match_list[0]
        b = match_list[1]
        o = difflib.SequenceMatcher(isjunk=None, a=a, b=b)
        size = o.find_longest_match(0, len(a), 0, len(b))[2]
        for index, item in enumerate(match_list):
            if index == 0 or index == len(match_list) - 1 or index == 1:
                continue
            else:
                b = item
            temp = o.find_longest_match(0, len(a), 0, len(b))[2]
            if temp < size:
                size = temp
        return size

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
    def _remove_suffix_name(_url, suffix_name):
        if _url.find(suffix_name[1:]):
            return _url[0:len(_url) - len(suffix_name) + 1]
        else:
            return _url

    @staticmethod
    def duplicate_eliminate(list_input):
        """ Delete all duplicate in a list."""
        result = []
        for i in list_input:
            if i not in result:
                result.append(i)

        return result

    def analysis_url(self):
        content = self._url_read()
        match_list = []
        self._pattern_make()
        for i in self.pattern_list:
            match = re.findall(i, content)
            for j in match:
                if self._check_match_url(j):
                    match_list.append(j)
        # Check if not match.
        if not match_list:
            print('Error!We find nothing!')
            return False
        # Classify the url into certain types.
        result = self._handle_match(match_list)
        # Choose specific block to make pattern.
        choose_block = 0
        specific_pattern = self.make_specific_pattern(result[choose_block])
        self.SQL.insert_url(result[choose_block])
        self._display_result(result)

    def make_specific_pattern(self, specific_block_list):
        # Delete all duplicate in this list.
        specific_block_list = self.duplicate_eliminate(specific_block_list)
        # Get longest match block.
        flag_only_one = 0
        try:
            same_size = self.find_longest_match(specific_block_list)
        except IndexError:
            flag_only_one = 1
            same_size = len(specific_block_list[0])
        same_block = specific_block_list[0][0:same_size]
        # Get suffix name and remove suffix name if possible.
        suffix_name = '\.' + self._get_suffix_name(specific_block_list[0])
        same_block = self._remove_suffix_name(same_block, suffix_name)
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
        if flag_only_one:
            char_supplement = ''
        else:
            char_supplement = '.+?'
        result_pattern = header + host + last_block + char_supplement + suffix_name
        return result_pattern


def main():
    # Make parser for terminal.
    description = 'MiniSpider makes it easy to create user-friendly spider.'
    usage = 'mini-spider [OPTION]... [URL]...'
    parser = argparse.ArgumentParser(prog='MiniSpider', description=description, usage=usage)

    # Add argument.
    analysis_help = 'Analysis a URL to make your extractor.suffix name follow the url.'
    parser.add_argument('-a', help=analysis_help, nargs='+', dest='analysis_url')

    similarity_threshold_help = 'Set similarity_threshold,default = 0.6'
    parser.add_argument('-st', help=similarity_threshold_help, nargs=1, dest='similarity', type=float)

    choose_help = 'Choose which block is you looking for.'
    parser.add_argument('-c', help=choose_help, nargs=1, dest='choose_block', type=int)

    timeout_help = 'Set timeout.default = 2'
    parser.add_argument('-t', help=timeout_help, nargs=1, dest='time_out', type=float)

    # Parse argument.
    args = parser.parse_args()

    # Parse analysis url.
    if args.analysis_url[0]:
        if not args.analysis_url[1]:
            print('WARNING: Please input what resource you are looking for!')
        if args.similarity:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:],
                                similarity_threshold=args.similarity[0])
            spider.analysis_url()
        else:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:], similarity_threshold=0.6)
            spider.analysis_url()


if __name__ == '__main__':
    main()
