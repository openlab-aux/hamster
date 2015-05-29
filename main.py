#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from hamster.QtVariant import QtGui
from hamster.items import ItemsWidget
from hamster.dialogs import LoginDialog, NewUserDialog
from hamster.lsms import Lsms, LsmsException

log = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, server_url):
        super(MainWindow, self).__init__()
        self.setGeometry(400, 400, 800, 400)
        self.setWindowTitle("Hamster (lsmsd client)")

        self.server_url = server_url
        self.lsms = Lsms(self.server_url)
        things = self.lsms.select_all("items")

        self.items_widget = ItemsWidget(things, self)
        self.setCentralWidget(self.items_widget)

        self.__setup_ui()

    def __setup_ui(self):
        login_action = QtGui.QAction('Login', self)
        login_action.triggered.connect(self.login_changed)

        config_action = QtGui.QAction('Config', self)
        config_action.triggered.connect(self.config_changed)

        new_user_action = QtGui.QAction('New User', self)
        new_user_action.triggered.connect(self.new_user)

        self.toolbar = self.addToolBar('Bla')
        self.toolbar.addAction(login_action)
        self.toolbar.addAction(config_action)
        self.toolbar.addAction(new_user_action)

    def login_changed(self):
        u, p, ok = LoginDialog.getLoginData(self)

        if ok:
            self.lsms.set_credentials(u, p)

    def config_changed(self):
        text, ok = QtGui.QInputDialog.getText(
            self, 'Backend configuration', 'Server URL')

        if ok:
            log.info("New Server url: '%s'", text.strip())
            self.server_url = text.strip()
            self.lsms = Lsms(self.server_url)

    def new_user(self):
        u, m, p, ok = NewUserDialog.getUserData(self)

        if ok:
            try:
                payload = {'Name': u, 'EMail': m, 'Password': p}
                log.info("User created: %s", self.lsms.create_thing("users", payload))
            except LsmsException as e:
                #log.error(e)
                if e.status_code == 403:
                    QtGui.QMessageBox.critical(self, "User can not be created",
                                               "The given username already exists")

    def create_thing(self, payload):
        log.info("Creating thing in database")
        try:
            return int(self.lsms.create_thing("items", payload))
        except LsmsException as e:
            if e.status_code == 401:
                log.warning(e)
                QtGui.QMessageBox.critical(self, "Thing can not be created",
                                           "Username or password incorrect")

        return None


def test(base_url):
    app = QtGui.QApplication(sys.argv)

    w = MainWindow(base_url)
    w.show()

    #w = ItemsWidget()
    #w.resize(800, 400)
    #w.show()

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
