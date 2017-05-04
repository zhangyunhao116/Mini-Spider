#!/usr/bin/env python
import argparse

from .sql import MiniSpiderSQL
from .scheduler import MiniSpider
from .extractor import Extractor
from .downloader import MiniSpiderDownloader

__version__ = '0.0.4'


def main():
    # Make parser for terminal.
    description = 'MiniSpider makes it easy to create user-friendly spider.'
    usage = 'mini-spider [OPTION]... [URL]...'
    parser = argparse.ArgumentParser(prog='MiniSpider', description=description, usage=usage,
                                     epilog='Powered by ZYunH. Version:%s' % __version__)

    # Add arguments.
    analysis_help = 'Analysis a URL.'
    parser.add_argument('-a', help=analysis_help, nargs='+', dest='analysis_url', metavar='[URL]')

    similarity_threshold_help = 'Set similarity_threshold,default = 0.6'
    parser.add_argument('-st', help=similarity_threshold_help, nargs=1, dest='similarity', type=float,
                        metavar='[float]')

    choose_help = 'Choose block make extractor.'
    parser.add_argument('-c', help=choose_help, nargs='+', dest='choose_block', type=int, metavar='[num]')

    timeout_help = 'Set timeout.(default: 2)'
    parser.add_argument('-time', help=timeout_help, nargs=1, dest='time_out', type=float, metavar='[float]')

    to_help = 'Choose match data.(default: u)'
    parser.add_argument('-to', help=to_help, nargs='?', dest='to', const='u', choices=['u', 'r'])

    name_help = 'Name your extractor.it can be ignored.'
    parser.add_argument('-n', help=name_help, nargs=1, dest='name', metavar='[name]')

    start_help = 'Start spider to get url and resource.'
    parser.add_argument('-start', help=start_help, nargs='?', dest='start', const=True, metavar='URL')

    download_help = 'Download all url from database.'
    parser.add_argument('-download', help=download_help, nargs='?', dest='download', const=True, metavar='Path')

    make_help = 'Make extractor by user.'
    parser.add_argument('-m', help=make_help, nargs='+', dest='make', metavar='[RE]')

    export_help = 'Export url from database.'
    parser.add_argument('-export', help=export_help, nargs=1, dest='export_url', metavar='[FileName]')

    import_help = 'Import url into database.'
    parser.add_argument('-import', help=import_help, nargs=1, dest='import_url', metavar='[FileName]')

    list_help = 'List url in url_list or resource.options: "u" or "r"'
    parser.add_argument('-list', help=list_help, nargs='+', dest='list_url', metavar='')

    false_help = 'Disable classification function in -download.'
    parser.add_argument('-false', help=false_help, nargs='?', dest='false_set', const=True, metavar='')

    reset_help = 'Reset database stats = 1.(default: u)'
    parser.add_argument('-reset', help=reset_help, nargs='?', dest='reset', const='u', choices=['u', 'r'])

    # Parse arguments.
    args = parser.parse_args()

    # Parse analysis url.
    if args.analysis_url:
        if len(args.analysis_url) == 1:
            print('Error: Please input what resource you are looking for!')
            return False
        timeout = 2.0
        if args.time_out:
            timeout = args.time_out[0]
        if args.similarity:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:],
                                similarity_threshold=args.similarity[0], timeout=timeout)
            spider.analysis_url()
        else:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:], similarity_threshold=0.6,
                                timeout=timeout)
            spider.analysis_url()

    # Choose block make regular expression.
    elif args.choose_block:
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
    elif args.make:
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
    elif args.start:
        if args.start is True:
            MiniSpider().start()
        else:
            MiniSpider().start(args.start)

    # Start downloading.
    elif args.download:
        classify = True
        timeout = 2.0
        if args.false_set:
            classify = False
        if args.time_out:
            timeout = args.time_out[0]
        if args.download is True:
            MiniSpiderDownloader().start(classify=classify, timeout=timeout)
        else:
            MiniSpiderDownloader().start(args.download, classify=classify, timeout=timeout)

    # Import txt.
    elif args.import_url:
        # Choose database.
        if args.to:
            if args.to[0] == 'u':
                MiniSpiderSQL().import_txt(args.import_url[0], 'url_list')
            elif args.to[0] == 'r':
                MiniSpiderSQL().import_txt(args.import_url[0], 'resource')
            print('Import success!')
        else:
            print("Error: Please input  '-to u' or '-to r'")
            return False

    # Export txt.
    elif args.export_url:
        # Choose database.
        if args.to:
            if args.to[0] == 'u':
                MiniSpiderSQL().export_txt(args.export_url[0], 'url_list')
            elif args.to[0] == 'r':
                MiniSpiderSQL().export_txt(args.export_url[0], 'resource')
            print('Export success!')
        else:
            print("Error: Please input  '-to u' or '-to r'")
            return False

    # List database.
    elif args.list_url:
        num = 50
        if len(args.list_url) == 2:
            num = int(args.list_url[1])
        if args.list_url[0] == 'u':
            MiniSpiderSQL().list_url(table_name='url_list', num=num)
        elif args.list_url[0] == 'r':
            MiniSpiderSQL().list_url(table_name='resource', num=num)
        else:
            print("Error: Please input  '-list u' or '-list r'")
            return False

            # print(parser.print_help())

    # Reset database stats.
    elif args.reset:
        MiniSpiderSQL().reset(args.reset[0])

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
