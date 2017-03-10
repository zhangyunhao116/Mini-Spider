from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode
from os import path, getcwd, remove
from time import time, sleep
from ssl import _create_unverified_context


class Downloader:
    """This class is used to handle the Download requests that arrive at the server."""

    def __init__(self, url, filename='', block_size=1024 * 1024, ssl_context=None, headers={}, timeout=2):
        # If filename is not specified,it is equal to the default value provided by url.
        if filename == '':
            filename = url.split('/')[-1]
        # Parse chinese.
        url = quote(url, safe='/:?=@&')
        # Create ssl context.
        if ssl_context:
            self.ssl_context = ssl_context
        else:
            self.ssl_context = _create_unverified_context()
        # Create work path.
        self.work_path = ''
        # Initialization parameters.
        self.url = url
        self.filename = self.work_path + filename
        self.log_filename = self.work_path + filename + '._temp_log'
        self.block_size = int(block_size)
        self.block_list = []
        self.headers = headers
        self.timeout = timeout
        self.content_length_now = 0
        self.content_length_size = 0
        # File Info.
        self.file_type = 'Unknown'
        self.server_code = 0
        self.info = {}
        # Progress speed.
        self._speed_time = 0
        self._speed_pre_second = 0
        # Error detect
        self._error_timer = 0

    def get_server_info(self):
        req = Request(self.url)
        if self.headers:
            for k, v in self.headers.items():
                req.add_header(k, v)

        # Add header to tell the server where to start.
        req.add_header('Range', 'bytes=0-1')

        with urlopen(req, context=self.ssl_context, timeout=self.timeout) as f:
            for k, v in f.getheaders():
                # Save info.
                self.info[k] = v
                # Save important info.
                if k == 'Content-Range':
                    self.content_length_size = int(v.split('/')[-1])
                if k == 'Content-Type':
                    self.file_type = v
            # Save server code.
            self.server_code = f.getcode()

    def support_resume(self):
        if self.server_code == 0:
            self.get_server_info()
        if self.server_code == 206:
            return True
        else:
            return False

    def _headers_read(self, filename):
        result = []

        with open(filename, 'r') as content:
            for line in content:
                if line[-1] == '\n':
                    line = line[0:-1]
                result.append(line)

        for i in result:
            temp = i.split(':')
            self.headers[temp[0]] = temp[1]

    def _log_save(self, content_length):
        content = [content_length]
        file = open(self.log_filename, mode='w')
        for index, item in enumerate(content):
            file.write(str(content[index]) + '\n')
        file.close()

    def _log_read(self):
        result = []

        with open(self.log_filename, 'r') as content:
            for line in content:
                if line[-1] == '\n':
                    line = line[0:-1]
                result.append(line)

        return result[0]

    def _log_delete(self):
        remove(self.log_filename)

    def _log_check(self):
        if path.isfile(self.log_filename):
            self.content_length_now = int(self._log_read())
        else:
            self._log_save(0)

    def _error(self):
        self._error_timer += 1
        if self._error_timer == 5:
            self._error_timer = 0
            sleep(1)

    def _create_block_list(self):
        block_number = int((self.content_length_size - self.content_length_now) / self.block_size) + 1
        l = [x * self.block_size for x in range(0, block_number)]
        if l[-1] > self.content_length_size:
            l[-1] = self.content_length_size + 1
        else:
            l.append(self.content_length_size)
        for i in range(1, len(l)):
            temp = [l[i - 1], l[i]]
            self.block_list.append(tuple(temp))

    def _progress_bar(self):
        progress = (self.content_length_now / self.content_length_size)
        size_mb = self.content_length_size / (1024 * 1024)
        _time = (time() - self._speed_time)
        self._speed_pre_second = int(self.block_size) / (_time * 1024 * 1024)
        s = 'All:%.2f mb,%.2f%% , speed: %.2fmb/s' % (size_mb, progress * 100, self._speed_pre_second)
        # s_terminal = 'All:%.2f mb,%.2f%% , speed: %.2fmb/s \r' % (size_mb, progress * 100, self._speed_pre_second)
        # stdout.write(s_terminal)
        # stdout.flush()
        print(s)

    def download(self):
        if self.support_resume():
            # Create block list.
            self._create_block_list()
            # Check log file.
            self._log_check()
            # Start download.
            for start, end in self.block_list:
                # Ignore downloaded parts.
                if start < self.content_length_now:
                    continue
                # Try download.
                self._speed_time = time()
                try:
                    self._download(start, end)
                except Exception as e:
                    print(e)
                    self._log_save(start)
                    self._error()
                    break
                # Update progress.
                self.content_length_now = end
                self._log_save(self.content_length_now)
                # Print progress.
                self._progress_bar()
            # Delete log file
            if self.content_length_now == self.content_length_size:
                self._log_delete()
        else:
            self._download(self.content_length_now, self.content_length_size)

    def auto_download(self):
        try:
            self.get_server_info()
        except Exception:
            self.auto_download()
            return 0
        _speed_average = 0
        _temp_speed_sum = 0
        _temp_speed_sum_timer = 0
        _speed_average_list = []
        while self.content_length_now != self.content_length_size:
            if _temp_speed_sum_timer == 5:
                _speed_average = _temp_speed_sum / _temp_speed_sum_timer
                _speed_average_list.append(_speed_average)
                i = len(_speed_average_list)
                if i > 1:
                    if _speed_average_list[i - 2] > _speed_average_list[i - 1]:
                        self.block_size -= 1024 * 1024 * 0.5
                    else:
                        self.block_size += 1024 * 1024 * 0.5
                    print('Changed: %s' % self.block_size)
                _temp_speed_sum_timer = 0
            _temp_speed_sum_timer += 1
            try:
                self.download()
                print(_temp_speed_sum_timer)
                _temp_speed_sum += self._speed_pre_second
            except Exception:
                return 0

    def re_download(self):
        try:
            self.get_server_info()
        except Exception as e:
            print(e)
            self.re_download()
            self._error()
            return 0
        try:
            if self.content_length_size == path.getsize(self.filename):
                return 0
        except Exception as e:
            print(e)
            self._error()
            pass
        while self.content_length_now != self.content_length_size:
            try:
                self.download()
            except Exception:
                self._error()
                return 0

    def _download(self, begin, end):
        req = Request(self.url)
        if self.headers:
            for k, v in self.headers.items():
                req.add_header(k, v)
        byte_range = 'bytes=' + str(begin) + '-' + str(end - 1)
        req.add_header('Range', byte_range)
        with urlopen(req, context=self.ssl_context, timeout=self.timeout) as r:
            with open(self.filename, mode='ab+') as f:
                f.seek(self.content_length_now)
                f.truncate()
                f.write(r.read())

    def _url_open(self):
        req = Request(self.url)
        if self.headers:
            for k, v in self.headers.items():
                req.add_header(k, v)
        with urlopen(req, context=self.ssl_context, timeout=self.timeout, data={}) as r:
            return r.read()


if __name__ == "__main__":
    url = 'http://www.dy2018.com/i/96869.html'
    # url = 'http://tug.org/cgi-bin/mactex-download/MacTeX.pkg'
    # url = 'ed2k://|file|[算法（第四版）.中文版.图灵程序设计丛书]Algorithms.-.Fourth.Edition.谢路云.影印版（高清）.pdf'
    # url = 'https://download.jetbrains.8686c.com/idea/ideaIU-2016.3.2.dmg'
    print(url)

    headers = {
        'User-Agent=': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    }
    a = Downloader(url, block_size=1024 * 20, headers=headers)
    a._headers_read(filename='chrome.txt')
    print(a._url_open())
    """注意请求的Length是闭区间，而python的数组是左闭右开区间"""
