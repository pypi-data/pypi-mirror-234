import os
import re
import shutil
from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow.file import (
    TrackedFile            as BaseTrackedFile,
    TrackedFolder          as BaseTrackedFolder,
    Revision               as BaseRevision,
    TrackedFolderRevision  as BaseTrackedFolderRevision,
    FileSystemMap          as BaseFileSystemMap,
    GenericRunAction       as BaseGenericRunAction,
    UploadPlayblastToKitsu as BaseUploadPlayblastToKitsu
)
from libreflow.utils.os import remove_folder_content


class Revision(BaseRevision):
    pass


class TrackedFolderRevision(BaseTrackedFolderRevision):
    pass


class SessionChoiceValue(flow.values.SessionValue):
    
    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False

    def choices(self):
        raise NotImplementedError()

    def revert_to_default(self):
        choices = self.choices()

        if choices:
            self.set_watched(False)
            self.set(choices[0])
            self.set_watched(True)


class RevisionName(SessionChoiceValue):

    _file = flow.Parent(2)

    def choices(self):
        return self._file.get_revision_names(
            sync_status='Available',
            published_only=True
        )
    
    def revert_to_default(self):
        if self._file.is_empty():
            self.set('')
            return

        revision = self._file.get_head_revision(sync_status='Available')
        revision_name = ''
        
        if revision is None:
            choices = self.choices()
            if choices:
                revision_name = choices[0]
        else:
            revision_name = revision.name()
        
        self.set_watched(False)
        self.set(revision_name)
        self.set_watched(True)


class RevisionsMultiChoiceValue(flow.values.MultiChoiceValue):

    _file = flow.Parent(2)

    def choices(self):
        if self._file is not None:
            return sorted(self._file.get_revision_names(sync_status='Available', published_only=True), reverse=True)
        else:
            return ''

    def revert_to_default(self):
        if self._file is None or self._file.is_empty():
            self.set('')
            return

        revision = self._file.get_head_revision(sync_status='Available')
        revision_name = ''
        
        if revision is None:
            choices = self.choices()
            if choices:
                revision_name = choices[0]
        else:
            revision_name = revision.name()
        
        self.set(revision_name)
    
    def _fill_ui(self, ui):
        super(RevisionsMultiChoiceValue, self)._fill_ui(ui)
        if self._file is None or self._file.is_empty(on_current_site=True):
            ui['hidden'] = True


class AnimaticRevisionsMultiChoiceValue(RevisionsMultiChoiceValue):

    _action = flow.Parent()
    _shot = flow.Parent(6)
    HIDDEN = False

    def __init__(self, parent, name):
        super(AnimaticRevisionsMultiChoiceValue, self).__init__(parent, name)
        self._file = None
    
    def revert_to_default(self):
        self._file = None

        if self._action.animatic_path.get() != '':
            task_name, file_name = self._action.animatic_path.get().split('/')
            name, ext = os.path.splitext(file_name)

            if self._shot.tasks[task_name].files.has_file(name, ext[1:]):
                self._file = self._shot.tasks[task_name].files[file_name.replace('.', '_')]

        self.set([])
    
    def _fill_ui(self, ui):
        super(AnimaticRevisionsMultiChoiceValue, self)._fill_ui(ui)
        ui['hidden'] = self.HIDDEN


class AnimaticPathSessionValue(flow.values.SessionValue):

    _action = flow.Parent()
   
    def revert_to_default(self):
        value = self.root().project().get_action_value_store().get_action_value(
            self._action.name(),
            self.name(),
        )
        if value is None:
            default_values = {}
            default_values[self.name()] = self.get()

            self.root().project().get_action_value_store().ensure_default_values(
                self._action.name(),
                default_values
            )
            return self.revert_to_default()

        self.set(value)


class AbstractRVOption(BaseGenericRunAction):
    """
    Abstract run action which instantiate an RV runner,
    with its default version.
    """
    def runner_name_and_tags(self):
        return 'RV', []
    
    def get_version(self, button):
        return None


class CompareWithAnimaticAction(AbstractRVOption):

    ICON = ('icons.libreflow', 'compare-previews')

    _file = flow.Parent()
    _shot = flow.Parent(5)
    _animatic_path = flow.SessionParam('', AnimaticPathSessionValue).ui(hidden=True)

    @classmethod
    def supported_extensions(cls):
        return ["mp4","mov"]

    def allow_context(self, context):
        self._animatic_path.revert_to_default()
        file_name = self._animatic_path.get().split('/')[1] if self._animatic_path.get() != '' else ''
        return (
            context 
            and self._file.format.get() in self.supported_extensions()
            and self._file.name() != file_name
        )

    def needs_dialog(self):
        if self._animatic_path.get() != '':
            task_name, file_name = self._animatic_path.get().split('/')
            self._animatic_path.set(
                self._get_last_revision_path(task_name, file_name)
            )

        return (self._animatic_path.get() == '')
    
    def get_buttons(self):
        if self._animatic_path.get() == '':
            self.message.set(
                '''
                <h2>Can\'t find the animatic.</h2>\n
                Check if path parameter is correctly setted in Action Value Store.
                '''
            )
        
        return ['Close']
    
    def extra_argv(self):
        return [
            '-wipe', '-autoRetime', '0',
            self._file.get_head_revision().get_path(),
            '[', '-volume', '0', self._animatic_path.get(), ']'
        ]

    def run(self, button):
        if button == 'Close':
            return
        
        return super(CompareWithAnimaticAction, self).run(button)

    def _get_last_revision_path(self, task_name, file_name):
        path = ''

        if self._shot.tasks.has_mapped_name(task_name):
            task = self._shot.tasks[task_name]
            name, ext = file_name.rsplit('.', 1)

            if task.files.has_file(name, ext):
                f = task.files[f'{name}_{ext}']
                r = f.get_head_revision()

                if r is not None and r.get_sync_status() == 'Available':
                    path = r.get_path()

        return path


class CompareInRVAction(AbstractRVOption):
    ICON = ('icons.libreflow', 'compare-previews')

    _file = flow.Parent()
    _shot = flow.Parent(5)
    
    revisions = flow.Param([], RevisionsMultiChoiceValue)
    animatic_path = flow.SessionParam('', AnimaticPathSessionValue).ui(hidden=True)
    animatic_revisions = flow.Param([], AnimaticRevisionsMultiChoiceValue).ui(label="Animatic Revisions")
   
    @classmethod
    def supported_extensions(cls):
        return ["mp4","mov"]

    def allow_context(self, context):
        return (
            context 
            and self._file.format.get() in self.supported_extensions()
            and len(self._file.get_revision_names(sync_status='Available', published_only=True)) >= 2 
        )

    def needs_dialog(self):
        self.animatic_path.revert_to_default()

        if self.animatic_path.get() != '':
            task_name, file_name = self.animatic_path.get().split('/')
            if self._file.name() == file_name.replace('.', '_'):
                self.animatic_revisions.HIDDEN = True
        
        return True

    def extra_argv(self):
        return ['-autoRetime', '0', '-layout', 'column', '-view', 'defaultLayout'] + self._revisions
       
    def get_buttons(self):
        self.revisions.set([self.revisions.choices()[0], self.revisions.choices()[1]])
        if not self.animatic_revisions.HIDDEN:
            self.animatic_revisions.revert_to_default()

        message = '<h3>Choose revisions to compare</h3>'
        if self.animatic_path.get() == '':
            message += '''<font color="#D66700">
            If you want the animatic, you need to specify the path parameter in Action Value Store
            </font>
            '''

        self.message.set(message)
        return ['Open', 'Cancel']
  
    def run(self, button):
        if button == "Cancel":
            return

        self._revisions = []

        for revision in self.revisions.get():
            if self._revisions == []:
                self._revisions += [self._file.get_revision(revision).get_path()]
                continue
            self._revisions += ['[', '-volume', '0', self._file.get_revision(revision).get_path(), ']']
               
        if self.animatic_revisions.get():               
            for antc_revision in self.animatic_revisions.get():
                self._revisions += [
                    '[', '-volume', '0',
                    self.animatic_revisions._file.get_revision(antc_revision).get_path(), ']'
                ]

        result = super(CompareInRVAction, self).run(button)
        return self.get_result(close=True)


class UploadPlayblastToKitsu(BaseUploadPlayblastToKitsu):

    def _ensure_kitsu_entity(self):
        if self._kitsu_entity is None:
            # kitsu = self.root().project().kitsu_api()
            kitsu_bd = self.root().project().kitsu_bindings()
            file_settings = get_contextual_dict(self._file, 'settings')
            # entity_data = kitsu_bindings.get_entity_data(file_settings)
            # self._kitsu_entity = kitsu_bindings.get_kitsu_entity(entity_data)
            film_name = file_settings.get('film_display_name', file_settings.get('film'))
            sequence_name = file_settings.get('sequence_display_name', file_settings.get('sequence'))
            shot_name = file_settings.get('shot_display_name', file_settings.get('shot'))

            print(film_name, sequence_name, shot_name)

            if shot_name and sequence_name:
                data = kitsu_bd.get_entity_data({
                    'entity_type': 'shot',
                    'shot': shot_name,
                    'sequence': sequence_name,
                    'episode': film_name
                })
                self._kitsu_entity = kitsu_bd.get_kitsu_entity(data)
            else:
                asset_name = file_settings.get('asset_display_name', file_settings.get('asset'))

                if asset_name:
                    data = kitsu_bd.get_entity_data({
                        'entity_type': 'asset',
                        'asset': asset_name
                    })
                    self._kitsu_entity = kitsu_bd.get_kitsu_entity(data)
        
        return self._kitsu_entity


class ShotType(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_types.get()


class ShotIndex(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_indexes.get()


class ShotVersion(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_versions.get()


class RenameImageSequence(flow.Action):

    title = flow.SessionParam('<h2>Rename image sequence</h2>').ui(editor='label', wrap=True).ui(editable=False, label='')
    revision = flow.SessionParam(None, RevisionName).watched()
    shot_type = flow.SessionParam(None, ShotType).watched()
    shot_index = flow.SessionParam(None, ShotIndex).watched()
    shot_version = flow.SessionParam(None, ShotVersion).watched()
    summary_ = flow.SessionParam('').ui(editor='label', wrap=True).ui(editable=False, label='')

    _folder = flow.Parent()
    _files = flow.Parent(2)
    _shot = flow.Parent(5)

    def __init__(self, parent, name):
        super(RenameImageSequence, self).__init__(parent, name)
        self._first_file = None

    def allow_context(self, context):
        return context and not self._folder.is_empty(on_current_site=True)
    
    def needs_dialog(self):
        self.revision.revert_to_default()
        self.shot_type.revert_to_default()
        self.shot_index.revert_to_default()
        self.shot_version.revert_to_default()
        self.message.revert_to_default()
        self.summary_.revert_to_default()
        
        files = self._get_file_sequence()

        if not files:
            self.message.set('The selected revision is empty.')
        elif self.shot_type.get() is None:
            self.message.set('You must define at least one shot type in the project settings.')
        elif self.shot_index.get() is None:
            self.message.set('You must define at least one shot index in the project settings.')
        elif self.shot_version.get() is None:
            self.message.set('You must define at least one shot version in the project settings.')
        else:
            self.summary_.set(
                f'Current name:\t{files[0]}\n\nNew name:\t{self._get_new_name(files[0])}'
            )
        
        return True
    
    def get_buttons(self):
        return ['Rename', 'Cancel']
    
    def child_value_changed(self, child_value):
        if child_value in (self.revision, self.shot_type, self.shot_index, self.shot_version):
            files = self._get_file_sequence()

            if not files:
                self.message.set('The selected revision is empty.')
                self.summary_.set('')
            else:
                self.message.set('')
                self.summary_.set(
                    f'Current name:\t{files[0]}\n\nNew name:\t{self._get_new_name(files[0])}'
                )
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        revision = self.revision.get()

        if revision is None:
            raise Exception('You are trying to run this action on an empty file !')
        
        new_prefix = self._get_new_prefix()

        if new_prefix is None:
            return self.get_result(close=False)
        
        src_dir = self._folder.get_revision(revision).get_path()
        dst_dir = self._ensure_folder_revision()

        for im in os.listdir(src_dir):
            new_im = self._get_new_name(im, new_prefix)
            shutil.copy2(os.path.join(src_dir, im), os.path.join(dst_dir, new_im))
            print(f'{os.path.join(src_dir, im)} -> {os.path.join(dst_dir, new_im)}')
    
    def _get_new_name(self, current_name, suffix=None):
        return f'{suffix or self._get_new_prefix() or ""}.{self._get_suffix(current_name)}'
    
    def _get_new_prefix(self):
        # m = re.search(r'\d+', self._shot.name())
        # shot_num = f'{int(m.group()):02}' if m else '<undefined>'
        # m = re.search(r'\d+', self.revision.get())
        # rev_num = f'V{int(m.group())}' if m else '<undefined>'
        params = (self.shot_type.get(), self.shot_index.get(), self.shot_version.get())
        if None in params:
            return None
        else:
            return '_'.join(params)
    
    def _get_suffix(self, current_name):
        try:
            return current_name.split('.', maxsplit=1)[1]
        except IndexError:
            return ''
    
    def _ensure_folder_revision(self):
        name = self._folder.name() + '_ok'
        
        if not self._files.has_folder(name):
            folder = self._files.add_folder(name, tracked=True)
            folder.file_type.set('Outputs')
        else:
            folder = self._files[name]
        
        rev = folder.get_revision(self.revision.get())

        if rev is None:
            rev = folder.add_revision(self.revision.get())

        path = rev.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            remove_folder_content(path)
        
        return path
    
    def _get_file_sequence(self):
        folder = self._folder.get_revision(self.revision.get()).get_path()
        files = os.listdir(folder)
        files = [
            f for f in files
            if os.path.isfile(os.path.join(folder, f))
        ]
        return files


class ConvertToMP4(flow.Action):

    revision = flow.SessionParam(None, RevisionName)

    _file = flow.Parent()
    _files = flow.Parent(2)

    def allow_context(self, context):
        return context and self._file.format.get() == 'mov'
    
    def get_buttons(self):
        self.revision.revert_to_default()
        return ['Confirm', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        ffmpeg_exe = self.root().project().admin.project_settings.ffmpeg_path.get()
        src_path = self._file.get_revision(self.revision.get()).get_path()
        dst_path = self._ensure_mp4_path()

        # print(f'{ffmpeg_exe} -i {src_path} -vcodec h264 -acodec mp2 {dst_path}')

        os.system(f'"{ffmpeg_exe}" -i {src_path} -vcodec h264 -acodec mp2 {dst_path}')
    
    def _ensure_mp4_path(self):
        name = self._file.name().rsplit('_', maxsplit=1)[0]
        rev_name = self.revision.get()

        if not self._files.has_file(name, 'mp4'):
            f = self._files.add_file(name, 'mp4', tracked=True)
        else:
            f = self._files[f'{name}_mp4']
        
        rev = f.get_revision(rev_name)

        if rev is None:
            rev = f.add_revision(rev_name)
        
        path = rev.get_path()
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        return path


class TrackedFile(BaseTrackedFile):
    
    compare_rv = flow.Child(CompareInRVAction).ui(
        label="Compare in RV"
    )
    compare_antc = flow.Child(CompareWithAnimaticAction).ui(
        label='Compare with animatic'
    )
    compress = flow.Child(ConvertToMP4)


class TrackedFolder(BaseTrackedFolder):
    
    rename_sequence = flow.Child(RenameImageSequence)
    # pass


class FileSystemMap(BaseFileSystemMap):
    pass
