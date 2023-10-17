from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QDockWidget, QWidget, QLabel, QTextEdit

from huza.base.widget import MainQWidget

try:
    from huza.mainwindow import MainWindow_Form
except ImportError:
    MainWindow_Form = None
from huza.util.constant import *


def init_docks(self: MainWindow_Form, docks: dict, layout: list):
    """docks = {
        'main': QDockWidget(""),
        'para': QDockWidget(""),
        'setup': QDockWidget(""),
        'info': QDockWidget(""),
        'monitor': QDockWidget(""),
    }
    layout = [('add', 'left', 'para'),
         ('split', 'para', 'setup', 'h'),
         ('split', 'setup', 'main', 'h'),
         ('split', 'main', 'info', 'v'),
         ('tabify','para','monitor')
         ]

    :param self:
    :type self:
    :param docks_dict:
    :type docks_dict:
    :return:
    :rtype:
    """
    for k, v in docks.items():
        self.docks[k] = v
        self.dockviews[k] = {}
    for l in layout:
        hand = l[0]
        if hand == DOCK_LAYOUT_ADD:
            _, oriz, dockname = l
            self.form.addDockWidget(DockWidgetAreadict[oriz], self.docks[dockname])
        elif hand == DOCK_LAYOUT_SPLIT:
            _, d1, d2, ori = l
            self.form.splitDockWidget(self.docks[d1], self.docks[d2], Orientiondict[ori])
        elif hand == DOCK_LAYOUT_TABILY:
            _, d1, d2 = l
            self.form.tabifyDockWidget(self.docks[d1], self.docks[d2])


def setDockView(self, name, displayname, dockname, formclass, showthisview=True, widgetclass=MainQWidget):
    def _check_name_exist(name):
        """保证dockviews下的id唯一"""
        for k, v in self.dockviews.items():
            for uname, ui in v.items():
                if uname == name:
                    return k
        return None

    dock = self.docks.get(dockname)
    if dock.windowTitle() == name:
        return
    if showthisview:
        dock.setWindowTitle(displayname)
        dock.setVisible(True)
    dockviews = self.dockviews[dockname]
    if name in dockviews:
        w = dockviews.get(name)
        if showthisview:
            dock.setWidget(w)
        if hasattr(w, 'refresh'):
            w.refresh()
        return w.ui()
    else:
        nameexist = _check_name_exist(name)
        if nameexist is not None:
            raise Exception(f'dockviews已经存在相同的id，位于[{nameexist}]')

        w = widgetclass(self.form)
        w.signal.connect(self.signalHeadle)
        ui = formclass(self)
        ui._name_sig = name  # 用于标记名称
        ui.setupUi(w)
        w._ui = ui
        if showthisview:
            dock.setWidget(w)
        dockviews[name] = w
        return ui
