import re
import urllib.request
import urllib.parse
import difflib
import time

from ssl import _create_unverified_context


class MiniSpider:
    def __init__(self, url, timeout=2, ssl_context=None, url_check=False):
        # Parse chinese to ascii and delete parameters.
        self.url = url
        self.url_check = url_check
        self._check_url()
        # Create ssl context.
        if ssl_context:
            self.ssl_context = ssl_context
        else:
            self.ssl_context = _create_unverified_context()
        # Initialization parameters.
        self.timeout = timeout

    def _url_read(self):
        req = urllib.request.Request(self.url)
        with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as r:
            temp = r.read().decode('utf-8')
            print(temp)
            return temp

    def _check_url(self):
        if self.url_check:
            # Add protocol if not exist.
            if self.url.split('://', 1)[0] != 'http' or 'https':
                self.url = 'http://' + self.url
        # Parse chinese to ascii.
        self.url = urllib.parse.quote(self.url, safe='/:?=@&[]')

    def handle_match(self, match_list):
        for i in match_list:
            v = i.split('/')
            for j in v:
                if ' ' in j and i in match_list:
                    match_list.remove(i)
        match_list.sort()
        result = []
        flag = 0
        all_sort = 0
        for index, item in enumerate(match_list):
            if self.similarity(item, match_list[flag]) > 0.6:
                if index == len(match_list) - 1 and flag == 0:
                    result.append(all_sort)
                    for k in range(flag, index):
                        result.append(match_list[k])
                    flag = index
                    all_sort += 1
            else:
                result.append(all_sort)
                for k in range(flag, index):
                    result.append(match_list[k])
                flag = index
                all_sort += 1
        # print(result)
        for u in result:
            print(u)
        return result

    def analysis_url(self):
        content = self._url_read()
        pattern = '(http://.+?\.doc)'
        match_list = re.findall(pattern, content)
        if not match_list:
            print('Error!We find nothing!')
            return False
        match_list = self._check_match_url(match_list)
        result = self.handle_match(match_list)

    @staticmethod
    def similarity(str1, str2):
        if str1 == str2:
            return 1
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    @staticmethod
    def _check_match_url(match_list):
        temp = match_list
        for i in temp:
            v = i.split('/')
            for j in v:
                if ' ' in j and i in temp:
                    temp.remove(i)
        return temp

    def test(self):
        pass


if __name__ == '__main__':
    url = 'http://ciee.cau.edu.cn/art/2017/3/17/art_13728_504531.html'
    a = MiniSpider(url)

    q = time.time()
    a.analysis_url()
    print(time.time() - q)
