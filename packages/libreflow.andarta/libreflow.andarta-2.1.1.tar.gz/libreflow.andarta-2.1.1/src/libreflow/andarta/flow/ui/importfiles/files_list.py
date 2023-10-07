from libreflow.baseflow.ui.importfiles.files_list import (
    FileItem              as BaseFileItem,
    FilesList             as BaseFilesList
)
from .target_wizard import TargetWizardDialog


class FileItem(BaseFileItem):
    pass


class FilesList(BaseFilesList):

    def refresh(self, force_update=False):
        if force_update:
            # Fetch map
            items = self.page_widget.get_files()
        
            for item in items:
                # Check if already exist
                exist = False
                for i in reversed(range(self.layout.count())):
                    if self.layout.itemAt(i).widget().oid == item.oid():
                        exist = True
                
                if not exist:
                    # Start target wizard if there are some unknown values
                    if not item.file_status.get():
                        dialog = TargetWizardDialog(self, item)
                        if dialog.exec() == 0:
                            self.page_widget.remove_file(item.name())
                            continue

                    # Create item
                    item = FileItem(self, item)
                    self.layout.addWidget(item)

        # Show list
        if self.page_widget.refresh_list_count() > 0:
            self.page_widget.button_import.setEnabled(True)
        else:
            self.page_widget.button_import.setEnabled(False)
            self.page_widget.list.hide()
            self.page_widget.dragdrop.show()
