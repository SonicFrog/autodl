#!/usr/bin/env python3

from tvdb_api import Tvdb

from urllib.parse import urlparse


class LocalMatcher:
    def __init__(self, shows, accessor):
        self.shows = shows
        self.accessor = accessor

    def collect(self):
        for v in self.shows:
            pass
