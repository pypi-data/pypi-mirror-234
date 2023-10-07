import datetime
import timeago
from kabaret import flow
from libreflow.baseflow.users import User as BaseUser
from libreflow.baseflow.users import Users as BaseUsers


class KitsuUsersChoiceValue(flow.values.MultiChoiceValue):

    init = True
    kitsu_list = []

    def choices(self):
        if self.init == True:
            self.kitsu_list = self.root().project().kitsu_api().get_users()
            users = self.root().project().get_users().mapped_items()
            for user in users:
                if user.login.get() in self.kitsu_list:
                    self.kitsu_list.remove(user.login.get())
            self.init = False

        return self.kitsu_list

    def revert_to_default(self):       
        self.set([])
    
    def _fill_ui(self, ui):
        super(KitsuUsersChoiceValue, self)._fill_ui(ui)
        if self.choices() == []:
            ui['hidden'] = True


class KitsuUsersCreateAll(flow.values.SessionValue):

    DEFAULT_EDITOR = 'bool'

    _action = flow.Parent()

    def _fill_ui(self, ui):
        super(KitsuUsersCreateAll, self)._fill_ui(ui)
        if self._action.users_choices.choices() == []:
            ui['hidden'] = True


class User(BaseUser):

    last_visit = flow.Computed()
    libreflow_version = flow.Computed().ui(label="libreflow") 
    project_version = flow.Computed().ui(label="libreflow.andarta") 
    _last_visit = flow.IntParam(0)
    _last_libreflow_used_version = flow.Param(None)
    _last_project_used_version = flow.Param(None)

    def compute_child_value(self, child_value):
        if child_value is self.last_visit:
            if self._last_visit.get() == 0:
                child_value.set("never")
            else:
                
                last_connection = datetime.datetime.fromtimestamp(self._last_visit.get())
                now = datetime.datetime.now()
                child_value.set(timeago.format(last_connection, now))
        elif child_value is self.libreflow_version:
            from packaging import version
            requiered_version = version.parse(self.root().project().admin.project_settings.libreflow_version.get())
            user_current_version = self._last_libreflow_used_version.get()
            if not user_current_version:
                child_value.set("Unknown")
            else:
                user_current_version = version.parse(user_current_version)
                if requiered_version > user_current_version:
                    child_value.set("%s (!)" % str(user_current_version))
                else:
                    child_value.set("%s" % str(user_current_version))
        elif child_value is self.project_version:
            from packaging import version
            requiered_version = version.parse(self.root().project().admin.project_settings.project_version.get())
            user_current_version = self._last_project_used_version.get()
            if not user_current_version:
                child_value.set("Unknown")
            else:
                user_current_version = version.parse(user_current_version)
                if requiered_version > user_current_version:
                    child_value.set("%s (!)" % str(user_current_version))
                else:
                    child_value.set("%s" % str(user_current_version))


class CreateKitsuUsers(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    create_all    = flow.SessionParam(False, KitsuUsersCreateAll).ui(editor='bool').watched()
    users_choices = flow.Param([], KitsuUsersChoiceValue).ui(label='Users')

    _users = flow.Parent()

    def get_buttons(self):
        if self.users_choices.choices() == []:
            self.message.set('No new users were found on Kitsu.')
            return ['Cancel']
        self.users_choices.revert_to_default()
        return ['Create users', 'Cancel']

    def child_value_changed(self, child_value):
        if child_value is self.create_all:
            if child_value.get():
                self.users_choices.set(self.users_choices.choices())
            else:
                self.users_choices.revert_to_default()
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        kitsu_users = self.root().project().kitsu_config().users
        
        for user in self.users_choices.get():
            user_id = user.replace('.', '').replace('-', '')
            if not self._users.get_user(user):
                self._users.add_user(user_id, user)
                self.root().project().kitsu_api().set_user_login(user_id, user)
                print(f'Create user {user}')
        
        self._users.touch()
        kitsu_users.touch()


class Users(BaseUsers):

    create_users = flow.Child(CreateKitsuUsers)


class CheckUsersAction(flow.Action):

    def get_buttons(self):
        return ['Cancel']

    def needs_dialog(self):
        return False

    def run(self, button):
        project = self.root().project()
        users = project.admin.users
        print("\n                       #### USERS LAST CONNECTIONS AND VERSIONS ####")
        head = "|         user         |   last seen    |          libreflow         |      libreflow.thesiren    |"
        
        h = "" 
        for i in range(0,len(head)):
            h+= "-"
        print(h)
        print(head)
        print(h)

        for u in users.mapped_items():
            name = u.name()


            print("| %-20s | %14s | %-26s | %-26s |" % (name,
                    u.last_visit.get(),
                    u.libreflow_version.get(),
                    u.project_version.get(),
                    ))

        print(h + "\n")
