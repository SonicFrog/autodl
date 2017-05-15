from tvdb_api import Tvdb
from collections import namedtuple

class Fetcher:
    def fetch_show(self, show):
        return self.__fetch(show)

    def fetch_shows(self, shows):
        data = {}
        for x in shows:
            if x not in data.keys():
                data[x] = self.fetch_show(x)
        return data

Episode = namedtuple('Episode', ['show', 'name', 'season', 'episode'])

class TvdbFetcher(Fetcher):
    def __init__(self):
        self.api = Tvdb(actors = False)

    def __fetch(self, show):
        assert isinstance(show, str)
        return self.api[show]

    def __make_from_tvdb(self, show, season, episode):
        return Episode(show = show['seriesname'], season = season,
                       episode = episode, name = show[season][episode]['episodename'])

    def __fetch_range(self, show, season, episode):
        episodes = []
        for s in range(season, len(show)):
            for e in range(episode, len(show[s])):
                episodes.append(self.__make_from_tvdb(show, s, e))
        return episodes

    def fetch(self, show, season, episode):
        showobj = self.__fetch(show)
        return self.__fetch_range(showobj, season, episode)
