import os
import shutil
import re
import pprint

from kabaret import flow
from libreflow.utils.flow.import_files import (
    FileItem               as BaseFileItem,
    FilesMap               as BaseFilesMap,
    ImportFilesSettings    as BaseImportFilesSettings,
    ImportFilesAction      as BaseImportFilesAction
)


class FileItem(BaseFileItem):

    with flow.group("Entities"):
        asset_lib_name = flow.SessionParam()


class FilesMap(BaseFilesMap):

    @classmethod
    def mapped_type(cls):
        return FileItem


class ImportFilesSettings(BaseImportFilesSettings):

    files_map            = flow.Child(FilesMap)

    with flow.group("Regex"):
        film_regex       = flow.Param('{name}').ui(label='Film (Episode)')
        sequence_regex   = flow.Param('(SQ).*?([1-9]\d*)').ui(label='Sequence')
        shot_regex       = flow.Param('(SH).*?([1-9]\d*)').ui(label='Shot')
        asset_lib_regex  = flow.Param('{name}').ui(label='Asset lib')
    
    use_main_film        = flow.BoolParam(False)


class ImportFilesAction(BaseImportFilesAction):

    settings = flow.Child(ImportFilesSettings)

    def resolve_paths(self, paths):
        for path in paths:
            # Find matching file
            file_name = os.path.basename(path)
            match_file, task_names = self.resolve_file(file_name)

            # If the action was started from a task,
            # there is no need to resolve entities
            target_oid = None
            match_dict = None
            if self.source_task.get():
                target_oid = self.source_task.get()
            else:
                match_dict = self.resolve_entities(file_name, match_file)

            # Create item
            index = len(self.settings.files_map.mapped_items())
            item = self.settings.files_map.add(f'file{index+1}')

            # Set values
            item.file_path.set(path)
            item.file_name.set(file_name)
            item.file_match_name.set(match_file)
            item.file_extension.set(os.path.splitext(file_name)[1] if os.path.isfile(path) else None)

            item.film_name.set(
                match_dict['film'] if match_dict
                else self.get_entity_from_oid(target_oid, 'films')
            )
            item.sequence_name.set(
                match_dict['sequence'] if match_dict
                else self.get_entity_from_oid(target_oid, 'sequences')
            )
            item.shot_name.set(
                match_dict['shot'] if match_dict
                else self.get_entity_from_oid(target_oid, 'shots')
            )
            item.asset_lib_name.set(
                match_dict['asset_lib'] if match_dict
                else self.get_entity_from_oid(target_oid, 'asset_libs')
            )
            item.asset_type_name.set(
                match_dict['asset_type'] if match_dict
                else self.get_entity_from_oid(target_oid, 'asset_types')
            )
            item.asset_name.set(
                match_dict['asset'] if match_dict
                else self.get_entity_from_oid(target_oid, 'assets')
            )
            item.task_name.set(
                self.get_entity_from_oid(target_oid, 'tasks') if target_oid
                else task_names
            )
            item.file_target_oid.set(target_oid if target_oid else self.set_target_oid(item))

            # Define status
            
            # Valid if we know the matching file,
            # have all shot or asset data,
            # and one target task possible

            status = True
            if (
                match_file is None

                or any([
                    all(value is not None for value in [
                        item.film_name.get(),
                        item.sequence_name.get(),
                        item.shot_name.get()
                    ]),
                    all(value is not None for value in [
                        item.asset_lib_name.get(),
                        item.asset_type_name.get(),
                        item.asset_name.get(),
                    ])
                ]) is False

                or (
                    type(item.task_name.get()) is list
                    and len(item.task_name.get()) > 1
                )
            ):
                status = False

            item.file_status.set(status)

    def resolve_entities(self, file_name, match_file):
        pattern_dict = dict(
            film=self.settings.film_regex.get(),
            sequence=self.settings.sequence_regex.get(),
            shot=self.settings.shot_regex.get(),
            asset_lib=self.settings.asset_lib_regex.get(),
            asset_type=self.settings.asset_type_regex.get(),
            asset=self.settings.asset_regex.get()
        )

        match_dict = dict(
            film=None,
            sequence=None,
            shot=None,
            asset_lib=None,
            asset_type=None,
            asset=None
        )

        for key, pattern in pattern_dict.items():
            # For base entity (film and asset lib)
            if key in ('film', 'asset_lib'):
                if key == 'film':
                    map_items = self.root().project().films.mapped_items()
                else:
                    map_items = self.root().project().asset_libs.mapped_items()

                for item in reversed(map_items):
                    regexp = pattern.format(name=item.name())

                    match = re.search(regexp, file_name)
                    if match:
                        print(f'ImportFiles :: Find matching {key} ({match.group(0)})')
                        match_dict[key] = match.group(0)
                        break

                # Set main film if parameter enabled
                if (
                    key == 'film'
                    and match_dict[key] is None
                    and self.settings.use_main_film.get()
                ):
                    match_dict[key] = self.root().project().films.mapped_items()[0].name()

            # For sequence, shot, asset type and asset
            if key in ('sequence', 'shot', 'asset_type', 'asset'):
                regexp = pattern

                # Exception for asset
                if key == 'asset':
                    if match_dict['asset_type'] is not None:
                        regexp = pattern.format(
                            asset_type=match_dict['asset_type'],
                            match_file=match_file
                        )
                    else:
                        continue

                match = re.search(regexp, file_name)
                if match:
                    print(f'ImportFiles :: Find matching {key} ({match.group(0)})')
                    match_dict[key] = match.group(0)

        return match_dict

    def _fill_ui(self, ui):
        ui['custom_page'] = 'libreflow.andarta.flow.ui.importfiles.ImportFilesWidget'

