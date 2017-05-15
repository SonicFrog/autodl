#!/usr/bin/env python3

import os
import re

class TransmissionAccessor:
    def __init__(self, uri):
        pass

    def access(self, show, season = 1, episode = 1):
        pass


class LocalAccessor:

    REGEX = "%s.S%0.2d.E%0.2d.*"

    def __init__(self, directory):
        self.directory = directory

    def __dir_access(self, directory, show, season, episode):
        regex = (self.REGEX % (show, season, episode)).r
        for ent in os.scandir(self.directory):
            if ent.is_dir():
                return self.__dir_access(ent.path, show , season,episode)

            if regex.match(ent.name, re.IGNORE_CASE) is not None:
                return ent.path

        return None

    def access(self, show, season = 1, episode = 1):
        return self.__dir_access(self.directory, show, season, episode)
