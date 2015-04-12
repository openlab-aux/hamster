#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from hamster.QtVariant import QtGui
from hamster.items import ItemsWidget

log = logging.getLogger(__name__)


def test(base_url):
    app = QtGui.QApplication(sys.argv)

    w = ItemsWidget()
    w.resize(800, 400)
    w.show()

    sys.exit(app.exec_())

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
