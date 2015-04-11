#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def test(base_url):
    pass

if __name__ == '__main__':
    import signal

    base_url = "http://localhost:8080/"

    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #import cProfile
    #stats_file = "stats.prof"
    #cProfile.run("test()", stats_file)

    test(base_url)

    print("done")
