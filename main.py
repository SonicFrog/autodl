#!/usr/bin/env python2

import sys
from argparse import ArgumentParser, ArgumentError
from downloader import TransmissionDownloader
from finder import TPBFinder, T411Finder
from fetcher import TvdbFetcher

clients = {
    'transmission': TransmissionDownloader,
}

finders = {
    'piratebay': TPBFinder,
    't411': T411Finder,
}

fetchers = {
    'tvdb': TvdbFetcher,
}

def arg_check(o, m, v):
    def opt_print(o):
        return "--" + o

    if v not in m:
        print opt_print(o), "invalid value", v + ".", "Possible values are:"
        s = ""
        for key in m:
            s = key + ", "
        print s
        sys.exit(1)


if __name__ == '__main__':
    parser = ArgumentParser(description="Auto-download series and animes")

    # Misc options
    parser.add_argument('--dump', action='store_const', const=True,
                        default=False, help="Dump a list for magnet links if possible")
    parser.add_argument('--dry-run', action='store_const', const=False,
                        default=True, help="Only show what would be done")

    # Torrent backend options
    parser.add_argument('--client', type=str, help="Torrent client for download",
                        default="transmission")
    parser.add_argument('--client-host', type=str, default='localhost',
                        help="Hostname for the torrent client")
    parser.add_argument('--client-port', type=int, default=9091,
                        help="Port of the torrent client")

    parser.add_argument('--torrent-source', type=str, default='piratebay',
                        help="Source for torrents/magnets")

    # T411 options
    parser.add_argument('--t411-login', type=str,
                        help="t411 username")
    parser.add_argument('--t411-passwd', type=str,
                        help='t411 password')

    parser.add_argument('--metadata', type=str, default="tvdb",
                        help="the metadata service to use")

    # Positional arguments
    parser.add_argument('show', type=str, help="Show name to download")
    parser.add_argument('season', type=int, default=1,
                        help="Season to start download from")
    parser.add_argument('episode', type=int, default=1,
                        help="Episode to start download from")

    args = parser.parse_args(sys.argv[1:])

    arg_check("torrent-source", finders, args.torrent_source)
    arg_check("client", clients, args.client)
    arg_check('metadata', fetchers, args.metadata)

    dler = clients[args.client](args.client_host, args.client_port)
    finder = finders[args.torrent_source]()
    fetcher = fetchers[args.metadata]()

    episodes = fetcher.fetch(args.show, args.season, args.episode)

    print "Now downloading %d episodes for %s" % (len(episodes), args.show)

    magnets = finder.find(episodes, do=args.dry_run)

    if args.dump:
        for m in magnets:
            print m
    else:
        for m in magnets:
            dler.add(m)
