# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 17:01:42 2015

@author: burger
"""

from dotamining import Client, Config


if __name__ == "__main__":

    conf = Config(f="dotamining.conf")
    c = Client(conf.getApiKey())
#    hist = c.getMatchHistory()
#    for m in hist:
#        print(m.pretty())
    m = c.getMatchDetails(match_id="1214555568")
    print(m.pretty())
