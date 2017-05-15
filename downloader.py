import requests
import json
import os
from base64 import b64encode

class Downloader:
    def add(self, data, **kwargs):
        if data.startswith("magnet:"):
            if not kwargs['do']:
                print "Adding magnet %s to downloader" % data
                return None
            return self.add_magnet(data)

        if not kwargs['do']:
            print "Adding torrent to downloader"
            return None

        return self.add_torrent(data)

class TransmissionDownloader(Downloader):
    csrf = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://%s:%d/transmission/rpc" % (host, port)

        self.__fetch_csrf(self, self.url)

    def __fetch_csrf(self, url, override = False):
        if self.csrf is not None and not override:
            return

        resp = requests.post(self.url)

        if resp.status_code == 409:
            self.csrf = resp.headers['X-Transmission-Session-Id']

    def add_torrent(self, torrent):
        content = None
        try:
            s = os.stat(torrent)
            with os.fdopen(open(torrent)) as f:
                content = f.read()
        except OSError as err:
            content = torrent

        return self.__raw_torrent(content)

    def __post_tr_req(self, payload):
        print self.csrf
        headers = {'X-Transmission-Session-Id': self.csrf}

        resp = requests.post(self.url, data=json.dumps(payload), headers=headers)
        if resp.status_code != 200:
            raise ValueError("Bad response from torrent client")

        jresp = json.loads(resp.content)
        if jresp['result'] != 'success':
            raise ValueError("Request failed %s" % jresp['result'])

    def __raw_torrent(self, content):
        return self.__post_torrent(self, b64encode(content))

    def __post_torrent(self, torrent):
        req = {
            'arguments': {
                'metainfo': torrent,
                'paused': False,
            },
            'method': 'torrent-add',
        }
        return self.__post_tr_req(req)

    def add_magnet(self, magnet):
        req = {
            'arguments': {
                'filename': magnet,
                'paused': False,
            },
            'method': 'torrent-add',
        }

        return self.__post_tr_req(req)
