# -*- coding: utf-8 -*-
"""
@author: burger
"""


import ConfigParser


class Config(object):

    def __init__(self, f="../dotamining.conf"):
        c = ConfigParser.ConfigParser()
        c.read(f)
        self.__config = c

    def getApiKey(self):
        return self.__config.get("API", "key")


if __name__ == "__main__":
    c = Config()
    k = c.getApiKey()
    print(k)
