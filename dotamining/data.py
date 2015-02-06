# -*- coding: utf-8 -*-
"""
@author: burger
"""

import json
import os

from pony.orm import Database, Required, Set, PrimaryKey, Optional


database = Database("sqlite", "testdb.sqlite", create_db=True)


def _load_hero_mapping():
    fn = os.path.join(os.path.dirname(__file__), "heroes.txt")
    with open(fn) as f:
        res = json.load(f)
    heroes = res['result']['heroes']
    heroes = map(lambda d: (d["id"], d["localized_name"]), heroes)
    return dict(heroes)

heroes = _load_hero_mapping()


class Match(database.Entity):
    match_id = PrimaryKey(str)
    start_time = Required(int)
    lobby_type = Required(int)
    radiant_win = Optional(bool)
    heroes = Set(lambda: Hero)

    match_seq_num = None
    radiant_team_id = None
    dire_team_id = None
    players = None

    @staticmethod
    def fromJSON(s):
        ID = str(s["match_id"])
        match = Match.get(match_id=ID)
        if match is not None:
            return None
        d = {"match_id": ID,
             "start_time": s["start_time"],
             "lobby_type": s["lobby_type"],
             "heroes": []}
        match = Match(**d)
        heroes = []
        for item in s["players"]:
            p = Player.fromJSON(item)
            h = Hero.fromJSON(item, match.match_id, p.account_id)
            heroes.append(h)
        match.heroes = heroes
        return match

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


class Hero(database.Entity):
    match_id = Required(lambda: Match)
    account_id = Required(lambda: Player)
    hero_id = Required(int)
    radiant = Required(bool)

    @staticmethod
    def fromJSON(s, match_id, account_id):
        d = {"match_id": match_id,
             "account_id": account_id}
        d["hero_id"] = s["hero_id"]
        d["radiant"] = s["player_slot"] < 2**7
        return Hero(**d)


class Player(database.Entity):
    account_id = PrimaryKey(str)
    heroes = Set(lambda: Hero)
    ranking = Optional(float)

    @staticmethod
    def fromJSON(s):
        d = {'heroes': []}
        if "account_id" in s:
            d["account_id"] = str(s["account_id"])
        else:
            d["account_id"] = "-1"
        p = Player.get(account_id=str(d["account_id"]))
        if p is not None:
            return p
        return Player(**d)


database.generate_mapping(create_tables=True)

if __name__ == "__main__":
    import logging
    logging.info("Setting up database...")
    database.generate_mapping(create_tables=True)
