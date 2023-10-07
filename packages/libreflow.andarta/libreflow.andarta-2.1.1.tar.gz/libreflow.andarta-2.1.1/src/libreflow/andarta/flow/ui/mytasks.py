import webbrowser
from libreflow.baseflow.ui.mytasks import (
    MyTasksPageWidget      as BaseMyTasksPageWidget
)


class MyTasksPageWidget(BaseMyTasksPageWidget):

    def build(self):
        super(MyTasksPageWidget, self).build()
        self.header.fdt_button.hide()
        self.header.kitsu_tasks.clicked.disconnect()
        self.header.kitsu_tasks.clicked.connect(self._on_kitsu_tasks_button_clicked)

    def _on_kitsu_tasks_button_clicked(self):
        webbrowser.open(self.get_server_url() + '/todos')
