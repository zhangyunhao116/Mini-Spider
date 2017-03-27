#!/usr/bin/env python
import argparse

from .scheduler import MiniSpider
from .extractor import Extractor


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
    parser.add_argument('-t', help=timeout_help, nargs=1, dest='time_out', type=float)

    to_help = 'Choose match data to url_list[u] or resource[r] .default : [u] .'
    parser.add_argument('-to', help=to_help, nargs=1, dest='to', default='u')

    name_help = 'Name your extractor.it can be ignored.'
    parser.add_argument('-n', help=name_help, nargs=1, dest='name')

    start_help = 'Start.'
    parser.add_argument('-start', help=start_help, nargs=1, dest='start')

    # Parse arguments.
    args = parser.parse_args()

    # Parse analysis url.
    if args.analysis_url:
        if not args.analysis_url[1]:
            print('WARNING: Please input what resource you are looking for!')
        if args.similarity:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:],
                                similarity_threshold=args.similarity[0])
            spider.analysis_url()
        else:
            spider = MiniSpider(args.analysis_url[0], search=args.analysis_url[1:], similarity_threshold=0.6)
            spider.analysis_url()

    # Choose block make regular expression.
    if args.choose_block:
        length = len(args.choose_block)
        if length == 3:
            pattern = MiniSpider().choose_block(args.choose_block[0], args.choose_block[1], args.choose_block[2])
        elif length == 2:
            pattern = MiniSpider().choose_block(args.choose_block[0], args.choose_block[1])
        else:
            pattern = MiniSpider().choose_block(args.choose_block[0])
        print(pattern)
        if args.to:
            if args.name and args.to[0] == 'u':
                Extractor().make_extractor(args.name, pattern, mode='url')
            elif args.name and args.to[0] == 'r':
                Extractor().make_extractor(args.name, pattern, mode='resource')
            elif args.to[0] == 'u':
                Extractor().make_extractor(pattern=pattern, mode='url')
            elif args.to[0] == 'r':
                Extractor().make_extractor(pattern=pattern, mode='resource')

    if args.start:
        Extractor().run_all_extractor()