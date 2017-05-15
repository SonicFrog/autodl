from HTMLParser import HTMLParser
import requests

class PredicateLinkExtractor(HTMLParser):
    link = None

    def __init__(self, predicate):
        HTMLParser.__init__(self)
        self.predicate = predicate

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs and self.predicate(attrs):
                if self.link is None:
                    self.link = attrs['href']


class FirstMagnetExtractor(PredicateLinkExtractor):
    def __init__(self):
        PredicateLinkExtractor.__init__(
            self,
            lambda x: x['href'].startswith('magnet:')
        )


class FirstTorrentExtractor(HTMLParser):
    def __init__(self):
        PredicateLinkExtractor.__init__(
            self,
            lambda x : x['href'].endswith('\.torrent')
        )


class Finder:
    def _link(self, show, season, episode, **kwargs):
        current = self.get_url(show, season, episode)
        resp = requests.get(current)
        if resp.status_code != 200:
            raise requests.ConnectionError("Bad status code %d" %
                                           resp.status_code)
        parser = FirstMagnetExtractor()
        parser.feed(resp.content)
        if parser.link is None:
            raise ValueError("No results for %s.S%.2dE%.2d" %
                             (show, season, episode))
        return parser.link

    def find(self, episodes, **kwargs):
        magnets = []
        notfound = []

        for ep in episodes:
            try:
                mlink = self._link(ep.show, ep.season, ep.episode)
            except ValueError as err:
                print err.message
                notfound.append(ep)
                continue

            if not kwargs['do']:
                print "Found", mlink, "for", show, "S", season, "E", episode

            magnets.append(mlink)

        return magnets


class T411Finder(Finder):
    def __init__(self, **kwargs):
        if 'cookie' not in kwargs:
            raise ValueError("T411 needs a session cookie to function")

    def find(self, dler, show, season, episode):
        raise ValueError("Unimplemented")


class TPBFinder(Finder):
    URL = "https://thepiratebay.org/search/%s/0/99/0"
    EPISODE_FMT = "%s.S%.2d.E.%2d"

    def get_url(self, show, season, episode):
        return self.URL % (self.EPISODE_FMT % (show, season, episode))
