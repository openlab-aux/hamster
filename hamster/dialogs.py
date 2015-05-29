#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from hamster.QtVariant import QtGui, QtLoadUI

log = logging.getLogger(__name__)


class LoginDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        QtLoadUI(os.path.join("hamster", "LoginDialog.ui"), self)
        self.setWindowTitle("Login Information")

    @staticmethod
    def getLoginData(parent=None):
        dialog = LoginDialog(parent)
        result = dialog.exec_()
        u = dialog.username_lineEdit.text()
        p = dialog.password_lineEdit.text()

        return (u.strip(), p.strip(), result == QtGui.QDialog.Accepted)


class NewUserDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(NewUserDialog, self).__init__(parent)
        QtLoadUI(os.path.join("hamster", "NewUserDialog.ui"), self)
        self.setWindowTitle("New User")

    @staticmethod
    def getUserData(parent=None):
        dialog = NewUserDialog(parent)
        result = dialog.exec_()
        u = dialog.username_lineEdit.text()
        m = dialog.mail_lineEdit.text()
        p = dialog.password_lineEdit.text()

        return (u.strip(), m.strip(), p.strip(), result == QtGui.QDialog.Accepted)


def test():
    pass

if __name__ == '__main__':
    import signal

    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #import cProfile
    #stats_file = "stats.prof"
    #cProfile.run("test()", stats_file)

    test()

    print("done")
