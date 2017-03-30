#!/usr/bin/env python
import argparse

from .scheduler import MiniSpider
from .extractor import Extractor
from .downloader import MiniSpiderDownloader


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
    parser.add_argument('-c', help=choose_help, nargs='+', dest='choose_block', type=int)

    timeout_help = 'Set timeout.default = 2'
    parser.add_argument('-time', help=timeout_help, nargs=1, dest='time_out', type=float)

    to_help = 'Choose match data to url_list[u] or resource[r] .default : [u] .'
    parser.add_argument('-to', help=to_help, nargs='?', dest='to', const='u')

    name_help = 'Name your extractor.it can be ignored.'
    parser.add_argument('-n', help=name_help, nargs=1, dest='name')

    start_help = 'Start.'
    parser.add_argument('-start', help=start_help, nargs='?', dest='start', const=True)

    download_help = 'Download all url from database.'
    parser.add_argument('-download', help=download_help, nargs='?', dest='download', const=True)

    make_help = 'Make extractor from user.'
    parser.add_argument('-m', help=make_help, nargs='+', dest='make')

    # Parse arguments.
    args = parser.parse_args()

    # Parse analysis url.
    if args.analysis_url:
        if len(args.analysis_url) == 1:
            print('Error: Please input what resource you are looking for!')
            return False
        if args.similarity:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:],
                                similarity_threshold=args.similarity[0])
            spider.analysis_url()
        else:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:], similarity_threshold=0.6)
            spider.analysis_url()

    # Choose block make regular expression.
    if args.choose_block:
        num = args.choose_block[0]
        start = None
        end = None

        if len(args.choose_block) == 2:
            start = args.choose_block[1]
        elif len(args.choose_block) == 3:
            start = args.choose_block[1]
            end = args.choose_block[2]

        pattern = MiniSpider().choose_block(num, start, end)

        # Print pattern.
        if len(pattern) == 2:
            print('Host:' + pattern[1])
            print(pattern[0])
        else:
            print(pattern)

        # Choose database.
        if args.to:
            name = None
            if args.name:
                name = args.name[0]
            if args.to[0] == 'u':
                Extractor().make_extractor(name, pattern=pattern, mode='url')
            elif args.to[0] == 'r':
                Extractor().make_extractor(name, pattern=pattern, mode='resource')
            print('The extractor was created successfully！')
        else:
            print("Error: Please input  '-to u' or '-to r'")
            return False

    # Make pattern by user.
    if args.make:
        pattern_user = args.make[0]

        # Get host, if possible.
        if len(args.make) == 2:
            pattern_user = pattern_user, args.make[1]

        # Choose database.
        if args.to:
            name = None
            if args.name:
                name = args.name[0]
            if args.to[0] == 'u':
                Extractor().make_extractor(name, pattern=pattern_user, mode='url')
            elif args.to[0] == 'r':
                Extractor().make_extractor(name, pattern=pattern_user, mode='resource')
            print('The extractor was created successfully！')
        else:
            print("Error: Please input  '-to u' or '-to r'")
            return False

    # Start project.
    if args.start:
        if args.start is True:
            MiniSpider().start()
        else:
            MiniSpider().start(args.start)

    # Start downloading.
    if args.download:
        if args.download is True:
            MiniSpiderDownloader().start()
        else:
            MiniSpiderDownloader().start(args.download)


if __name__ == '__main__':
    main()
