from kabaret.app.ui.gui.widgets.flow.flow_view import QtCore, QtGui, QtWidgets, CustomPageWidget
from libreflow.baseflow.ui.importfiles.custom_widget import (
    WaitThread             as BaseWaitThread,
    PopUpDialog            as BasePopUpDialog,
    DragDropWidget         as BaseDragDropWidget,
    ImportFilesWidget      as BaseImportFilesWidget
)

from .files_list import FilesList

STYLESHEET = '''
    QLineEdit#PresetComboBox {
        border: none;
        padding: 0px;
    }
'''


class WaitThread(BaseWaitThread):
    pass


class PopUpDialog(BasePopUpDialog):
    pass


class DragDropWidget(BaseDragDropWidget):
    pass


class ImportFilesWidget(BaseImportFilesWidget):

    def build(self):
        self.setStyleSheet(STYLESHEET)
        self.clear_map()

        glo = QtWidgets.QGridLayout(self)

        self.dragdrop = DragDropWidget(self)

        self.popup = PopUpDialog(self)
        self.popup.hide()
        
        self.list = FilesList(self)
        self.list.hide()

        self.list_count = QtWidgets.QLabel(str(self.list.get_count())+' files')
        
        self.button_settings = QtWidgets.QPushButton('Settings')
        self.button_settings.clicked.connect(self._on_button_settings_clicked)
        self.button_settings.setAutoDefault(False)

        self.button_import = QtWidgets.QPushButton('Import')
        self.button_import.clicked.connect(self._on_button_import_clicked)
        self.button_import.setAutoDefault(False)
        self.button_import.setEnabled(False)
     
        glo.addWidget(self.list_count, 0, 0)
        glo.addWidget(self.dragdrop, 1, 0, 1, 3)
        glo.addWidget(self.list, 1, 0, 1, 3)
        glo.addWidget(self.popup, 1, 0, 1, 3)
        glo.addWidget(self.button_settings, 2, 0)
        glo.addWidget(self.button_import, 2, 2)
        glo.setColumnStretch(1, 1)
    
        self.wait = WaitThread()
        if not self.wait.isRunning():
            self.wait.start()
            self.wait.finished.connect(self._add_base_files)