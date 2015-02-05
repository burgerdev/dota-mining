# -*- coding: utf-8 -*-
"""
@author: burger
"""

import json

import os


def _load_hero_mapping():
    fn = os.path.join(os.path.dirname(__file__), "heroes.txt")
    with open(fn) as f:
        res = json.load(f)
    heroes = res['result']['heroes']
    heroes = map(lambda d: (d["id"], d["localized_name"]), heroes)
    return dict(heroes)

heroes = _load_hero_mapping()


class Match(object):
    match_id = None
    match_seq_num = None
    start_time = None
    lobby_type = None
    radiant_team_id = None
    dire_team_id = None
    players = None

    def __init__(self, client=None):
        self.__client = client

    def fromJSON(self, s):
        self.match_id = s["match_id"]
        self.match_seq_num = s["match_seq_num"]
        self.start_time = s["start_time"]
        self.lobby_type = s["lobby_type"]
        if "radiant_team_id" in s:
            self.radiant_team_id = s["radiant_team_id"]
        if "rdire_team_id" in s:
            self.dire_team_id = s["dire_team_id"]
        self.players = []
        for item in s["players"]:
            p = Player()
            p.fromJSON(item)
            self.players.append(p)

    def detailsFromJSON(self, s):
        self.radiant_win = s["radiant_win"]

    def pretty(self):
        radiant = filter(lambda x: x.faction_id == 0, self.players)
        dire = filter(lambda x: x.faction_id == 1, self.players)
        vs = "{:<30s} {:>30s}"
        coll = ["{:^61s}".format(self)]
        if self.radiant_win is not None:
            if self.radiant_win:
                s = "Radiant Victory"
            else:
                s = "Dire Victory"
            coll.append("{:^61s}".format(s))
        for x, y in zip(radiant, dire):
            coll.append(vs.format(x.pretty(), y.pretty()))
        return "\n".join(coll)

    def __str__(self):
        if self.match_id is None:
            return "Match: uninitialized"
        # TODO use real player information
        if len(self.players) > 2:
            m = n = 5
        else:
            m = n = 1
        return "Match {}: {}v{}".format(self.match_id, m, n)

    def fillMatchDetails(self):
        assert self.__client is not None
        self.__client.getMatchDetails(dm_output=self)


class Player(object):
    account_id = None
    hero_id = None
    player_slot = None

    hero_name = None
    faction_id = None

    def fromJSON(self, s):
        if "account_id" in s:
            self.account_id = s["account_id"]
        self.hero_id = s["hero_id"]
        self.player_slot = s["player_slot"]

        self._canonicalize()

    def _canonicalize(self):
        self.hero_name = heroes[self.hero_id] if self.hero_id > 0 else None
        self.faction_id = 0 if self.player_slot >= 2**7 else 1

    def pretty(self):
        return "{} ({})".format(self.hero_name, self.account_id)

    def __str__(self):
        return "Player {}: {}".format(self.account_id, self.hero_name)
