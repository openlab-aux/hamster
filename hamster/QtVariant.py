import sys
import os

default_variant = 'PySide'

env_api = os.environ.get('QT_API', 'pyqt')
if '--pyside' in sys.argv:
    variant = 'PySide'
elif '--pyqt4' in sys.argv:
    variant = 'PyQt4'
elif env_api == 'pyside':
    variant = 'PySide'
elif env_api == 'pyqt':
    variant = 'PyQt4'
else:
    variant = default_variant

if variant == 'PySide':
    print("Using PySide")
    from PySide import QtGui, QtCore, QtWebKit
    # This will be passed on to new versions of matplotlib
    os.environ['QT_API'] = 'pyside'

    def QtLoadUI(uifile, baseinstance=None, custom_widgets=None):
        from PySide.QtUiTools import QUiLoader
        from PySide.QtCore import QMetaObject

        class CustomUiLoader(QUiLoader):
            class_aliases = {
                'Line': 'QFrame',
            }

            def __init__(self, baseinstance=None, custom_widgets=None):
                super(CustomUiLoader, self).__init__(baseinstance)
                self._base_instance = baseinstance
                self._custom_widgets = custom_widgets or {}

            def createWidget(self, class_name, parent=None, name=''):
                # don't create the top-level widget, if a base instance is set
                if self._base_instance and not parent:
                    return self._base_instance

                if class_name in self._custom_widgets:
                    widget = self._custom_widgets[class_name](parent)
                else:
                    widget = QUiLoader.createWidget(
                        self, class_name, parent, name)

                if str(type(widget)).find(self.class_aliases.get(class_name, class_name)) < 0:
                    sys.modules['QtCore'].qDebug(str('PySide.loadUi(): could not find widget class "%s", defaulting to "%s"' % (class_name, type(widget))))

                if self._base_instance:
                    setattr(self._base_instance, name, widget)

                return widget

        loader = CustomUiLoader(baseinstance, custom_widgets)
        widget = loader.load(uifile)
        QMetaObject.connectSlotsByName(widget)
        return widget

elif variant == 'PyQt4':
    print("Using PyQt4")
    import sip
    api2_classes = [
        'QData', 'QDateTime', 'QString', 'QTextStream',
        'QTime', 'QUrl', 'QVariant',
    ]
    for cl in api2_classes:
        sip.setapi(cl, 2)
    from PyQt4 import QtGui, QtCore, QtWebKit
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.QString = str
    os.environ['QT_API'] = 'pyqt'

    def QtLoadUI(uifile, baseinstance=None):
        from PyQt4 import uic
        return uic.loadUi(uifile, baseinstance)
else:
    raise ImportError("Python Variant not specified")

#
# set all text encoding to utf-8
#
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("UTF-8"))
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("UTF-8"))
QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"))

__all__ = [QtGui, QtCore, QtLoadUI, QtWebKit, variant]
