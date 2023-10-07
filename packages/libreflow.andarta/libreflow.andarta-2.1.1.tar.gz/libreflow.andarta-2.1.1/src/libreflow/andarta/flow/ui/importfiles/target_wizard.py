import os
from kabaret.app.ui.gui.widgets.flow.flow_view import QtCore, QtGui, QtWidgets
from libreflow.baseflow.ui.importfiles.target_wizard import (
    EntityItem             as BaseEntityItem,
    EntityList             as BaseEntityList,
    TargetWizardDialog     as BaseTargetWizardDialog
)


STYLESHEET = '''
    QLineEdit {
        padding: 0px;
    }
'''

class EntityItem(BaseEntityItem):

    DEFAULT_ICONS = {
        "Films": ("icons.flow", "film"),
        "Sequences": ("icons.flow", "sequence"),
        "Shots": ("icons.flow", "shot"),
        "Tasks": ("icons.gui", "cog-wheel-silhouette"),
        "Asset Libs": ("icons.gui", "cog-wheel-silhouette"),
        "Asset Types": ("icons.flow", "asset_family"),
        "Assets": ("icons.flow", "asset")
    }


class EntityList(BaseEntityList):

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        # For main list
        if self.header_text == "Type":
            EntityItem(self, display_name='Films')
            EntityItem(self, display_name='Assets')

        # Show map items if we have oid
        if self.map_oid is not None:
            try:
                items = self.page_widget.session.cmds.Flow.get_mapped_rows(self.map_oid)

                for item_data in items:
                    # For files, show only ones with same extension
                    if self.header_text == 'Files':
                        name, ext = os.path.splitext(item_data[1]['Name'])
                        ext = None if ext == '' else ext
                        if ext != self.dialog.item.file_extension.get():
                            continue
                    
                    item = EntityItem(self, data=item_data)
                    
                    # Set current item if there is the default value
                    if item_data[1]['Name'] == self.default_value:
                        self.setCurrentItem(item)
            except KeyError:
                None

            # Add create new entity option at the end of the list
            if self.header_text != "Type":
                EntityItem(self, display_name='Create', editable=True)
        
        # Set current item if there is only one
        if self.topLevelItemCount()-1 == 1 and any(x in self.header_text for x in ['Type', 'Files']) is False:
            self.setCurrentItem(self.topLevelItem(0))
        else:
            # For specific cases
            if self.header_text == 'Files':
                if self.dialog.item.file_match_name.get():
                    self.setCurrentItem(self.get_item(self.dialog.item.file_match_name.get()))
                
                self.dialog.button_add.setEnabled(
                    True if self.currentItem() else False
                )

            if self.header_text == 'Tasks':
                if type(self.dialog.item.task_name.get()) is str:
                    self.setCurrentItem(self.get_item(name=self.dialog.item.task_name.get()))
                elif type(self.dialog.item.task_name.get()) is list:
                    for task_name in self.dialog.item.task_name.get():
                        matching_task = self.get_item(name=task_name)
                        matching_task.setForeground(0, QtGui.QBrush(QtGui.Qt.green)) if matching_task else None

        self.blockSignals(False)


class TargetWizardDialog(BaseTargetWizardDialog):

    def __init__(self, files_list, item):
        super(BaseTargetWizardDialog, self).__init__(files_list.page_widget)
        self.list = files_list
        self.page_widget = files_list.page_widget
        self.item = item
      
        self.setStyleSheet(STYLESHEET)

        self.film_flow = ['Films', 'Sequences', 'Shots', 'Tasks', 'Files']
        self.asset_flow = ['Asset Libs', 'Asset Types', 'Assets', 'Tasks', 'Files']

        self.split_oid = self.page_widget.session.cmds.Flow.split_oid(
            self.item.file_target_oid.get(), True, self.page_widget.get_project_oid()
        )

        self.build()
