#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from QtVariant import QtCore, QtGui, QtLoadUI

log = logging.getLogger(__name__)
logging.getLogger('PyQt4').setLevel(logging.WARNING)


class ItemsWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ItemsWidget, self).__init__(parent)

        self.item_tree_view = ItemTreeView(self)
        self.add_item_button = QtGui.QPushButton("New Item", self)
        self.item_prop_widget = ItemPropertiesWidget(None, self)

        self.__setup_ui()

    def __setup_ui(self):
        vert_widget = QtGui.QWidget(self)
        vert = QtGui.QVBoxLayout(vert_widget)
        vert.addWidget(self.item_tree_view)
        vert.addWidget(self.add_item_button)

        hori_widget = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        hori_widget.addWidget(vert_widget)
        hori_widget.addWidget(self.item_prop_widget)

        hori = QtGui.QHBoxLayout(self)
        hori.addWidget(hori_widget)

        self.add_item_button.released.connect(self.item_added)

    def item_dropEvent(self, event):
        log.error("TODO: Implement item_dropEvent")

    def item_added(self):
        log.error("TODO: Implement item_added")

    def item_deleted(self):
        log.error("TODO: Implement item_deleted")

    def item_changed(self, item):
        log.error("TODO: Implement item_changed")

    def item_saved(self, data):
        log.error("TODO: Implement item_saved")


class ItemTreeView(QtGui.QTreeView):

    def __init__(self, parent):
        super(ItemTreeView, self).__init__(parent)
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Items"])
        self.setModel(self.model)

        self.setSelectionMode(QtGui.QTreeView.SingleSelection)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.setAnimated(True)

        self.model.itemChanged.connect(self.parent().item_changed)

    def dropEvent(self, event):
        self.parent().item_dropEvent(event)
        super(ItemTreeView, self).dropEvent(event)


class ItemPropertiesWidget(QtGui.QWidget):

    def __init__(self, data, parent):
        super(ItemPropertiesWidget, self).__init__(parent)
        self.edit_state = False

        self.__setup_ui(data)

        self.input_widgets = [
            [self.name_lineEdit, lambda w: w.setReadOnly],
            [self.description_textEdit, lambda w: w.setReadOnly],
            [self.usage_lineEdit, lambda w: w.setReadOnly],
            [self.owner_comboBox, lambda w: w.setEditable],
            [self.maintainer_comboBox, lambda w: w.setEditable],
        ]

    def __setup_ui(self, data):
        QtLoadUI(os.path.join("hamster", "ItemPropertiesWidget.ui"), self)

        self.save_button.setHidden(True)

        self.edit_button.released.connect(self.edit_properties)
        self.delete_button.released.connect(self.delete_item)
        self.save_button.released.connect(self.save_item)

        if data:
            log.error("TODO: Implement data fill for input widgets on creation")

    def edit_properties(self):
        self.edit_state = not self.edit_state

        if self.edit_state is True:
            self.save_button.setHidden(False)
            for widget in self.input_widgets:
                widget[1](widget[0])(False)
        else:
            self.save_button.setHidden(True)
            for widget in self.input_widgets:
                widget[1](widget[0])(True)

        '''
        for w in self.input_widgets:
            if self.edit_state is True:
                w.setReadOnly(False)
            else:
                w.setReadOnly(True)
        '''

    def delete_item(self):
        self.parent().parent().item_deleted()

    def save_item(self):
        log.error("TODO: Implement save_item")
        # self.parent().item_saved()


def test():
    pass
    #app = QtGui.QApplication(sys.argv)
    #
    #w = ItemsWidget()
    #w.resize(800, 400)
    #w.show()
    #
    #sys.exit(app.exec_())

if __name__ == '__main__':
    import signal

    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #import cProfile
    #stats_file = "stats.prof"
    #cProfile.run("test()", stats_file)

    test()

    print("done")
