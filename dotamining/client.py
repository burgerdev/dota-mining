# -*- coding: utf-8 -*-
"""
@author: burger
"""

import json
import urllib

from data import Match

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Client(object):
    apiurl = "https://api.steampowered.com"
    language = "en_us"

    def __init__(self, apikey):
        self.__apikey = apikey

    def _getUrl(self, method, parameters):
        s = "/".join((self.apiurl, method))
        params = urllib.urlencode(parameters)
        return "{}/?{}".format(s, params)

    def _prepare_dict(self, d):
        # extend dict to contain all needed arguments
        assert "key" not in d
        d["key"] = self.__apikey
        if "language" not in d:
            d["language"] = self.language
        return d

    def getMatchHistory(self, *args, **kwargs):
        params = self._prepare_dict(kwargs)
        url = self._getUrl("IDOTA2Match_570/GetMatchHistory/V001", params)
        f = urllib.urlopen(url)
        d = json.load(f)

        # TODO realize as iterator
        matches = []
        for matchDict in d['result']['matches']:
            try:
                match = Match.fromJSON(matchDict)
                if match is not None:
                    matches.append(match)
            except Exception as e:
                print(e)
                logger.warn("Skipped result")
                raise
        return matches

    def getMatchDetails(self, *args, **kwargs):
        if "dm_output" in kwargs:
            match = kwargs.pop("dm_output")
        else:
            match = Match(client=self)

        params = self._prepare_dict(kwargs)
        url = self._getUrl("IDOTA2Match_570/GetMatchDetails/V001", params)
        f = urllib.urlopen(url)
        d = json.load(f)

        match.detailsFromJSON(d["result"])

        return match
