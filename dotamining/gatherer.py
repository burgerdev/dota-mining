# -*- coding: utf-8 -*-
"""
@author: burger
"""

import time

from pony.orm import db_session, commit
from data import Match

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Gatherer(object):
    def __init__(self, client):
        self.__client = client

    @db_session
    def run(self):
        params = dict()
        matches = []
        while True:
            logger.info("Requesting from Steam server ...")
            matches = self.__client.getMatchHistory(**params)
            if len(matches) == 0:
                logger.debug("Reached end of queue.")
                # time.sleep(100)
                # TODO continue working
                break

            logger.info("Processing {} matches ...".format(len(matches)))
            for match in matches:
                self._storeMatch(match)
                params["start_at_match_id"] = match.match_id
                logger.debug("Processed {}".format(match.match_id))

    def _storeMatch(self, match):
        # be nice to steam servers
        time.sleep(1)
        self.__client.getMatchDetails(match_id=match.match_id, dm_output=match)
        commit()
        


if __name__ == "__main__":
    from config import Config
    from client import Client
    conf = Config(f="../dotamining.conf")
    c = Client(conf.getApiKey())
    g = Gatherer(c)

    try:
        g.run()
    finally:
        logger.info("Shutting down")
