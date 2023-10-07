from libreflow.baseflow.task import ManagedTask, ManagedTaskCollection


class Task(ManagedTask):
    pass


class Tasks(ManagedTaskCollection):

    def get_default_tasks(self):
        tm = self.root().project().get_task_manager()
        return tm.get_template_default_tasks('asset')
