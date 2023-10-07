from kabaret import flow
from libreflow.baseflow.asset import (
    Asset               as BaseAsset,
    AssetFamily         as BaseAssetFamily,
    AssetType           as BaseAssetType,
    AssetTypeCollection as BaseAssetTypeCollection,
    AssetLibrary        as BaseAssetLibrary,
    AssetLibraryCollection as BaseAssetLibraryCollection,
    AssetCollection
)

from .task import Tasks


class Asset(BaseAsset):
    
    tasks = flow.Child(Tasks).ui(expanded=True)

    def ensure_tasks(self):
        """
        Creates the tasks of this asset based on the default
        tasks created with a template named `asset`, skipping
        any existing task.
        """
        default_tasks = self.tasks.get_default_tasks()

        for dt in default_tasks:
            if not self.tasks.has_mapped_name(dt.name()) and not dt.optional.get():
                t = self.tasks.add(dt.name())
                t.enabled.set(dt.enabled.get())
        
        self.tasks.touch()
    
    def _fill_ui(self, ui):
        ui['custom_page'] = 'libreflow.baseflow.ui.task.TasksCustomWidget'


class CreateKitsuAssets(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')

    _asset_lib = flow.Parent(4)
    _asset_type = flow.Parent(2)
    _assets = flow.Parent()

    def get_buttons(self):
        return ['Create assets', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()
        kitsu_api = self.root().project().kitsu_api()
        episode_name = self._asset_lib.code.get() or self._asset_lib.name() # TODO: add getter to lib for this
        if episode_name == 'MAIN_PACK':
            episode_name = 'default_episode'
        assets_data = kitsu_api.get_assets_data(self._asset_type.name(), episode_name)

        for data in assets_data:
            name = data['name']

            if not self._assets.has_mapped_name(name):
                s = self._assets.add(name)
                s.display_name.set(name)
                s.code.set(name)
            elif not skip_existing:
                s = self._assets[name]
            else:
                continue
            
            print(f'Create asset: {self._asset_type.name()} - {data["name"]}')
        
        self._assets.touch()


class Assets(AssetCollection):

    create_assets = flow.Child(CreateKitsuAssets)

    def add(self, name, object_type=None):
        a = super(Assets, self).add(name, object_type)
        a.ensure_tasks()
        
        return a


class AssetFamily(BaseAssetFamily):
    
    assets = flow.Child(Assets).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            edits = super(AssetFamily, self).get_default_contextual_edits(context_name)
            edits['path_format'] = 'lib/{asset_type}/{asset_family}/{asset}/{task}/{file_mapped_name}/{revision}/{asset}_{file_base_name}'
            return edits


class AssetType(BaseAssetType):
    
    assets = flow.Child(Assets).ui(expanded=True)
    asset_families = flow.Child(flow.Object).ui(hidden=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            edits = super(AssetType, self).get_default_contextual_edits(context_name)
            edits['path_format'] = 'lib/{asset_type}/{asset}/{task}/{file_mapped_name}/{revision}/{asset}_{file_base_name}'
            return edits


class CreateKitsuAssetsFromTypes(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')

    _asset_types = flow.Parent()
    _asset_lib = flow.Parent(2)

    def get_buttons(self):
        return ['Create assets', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()

        episode_name = self._asset_lib.code.get() or self._asset_lib.name() # TODO: add getter to lib for this
        if episode_name == 'MAIN_PACK':
            episode_name = 'default_episode'
        kitsu_api = self.root().project().kitsu_api()
        assets_data = kitsu_api.get_assets_data(episode_name=episode_name)

        for data in assets_data:
            name = data['name']

            if name == 'x':
                continue
            
            asset_type_name = kitsu_api.get_asset_type(data)['name']
            
            if not self._asset_types.has_mapped_name(asset_type_name):
                at = self._asset_types.add(asset_type_name)
                at.display_name.set(asset_type_name)
                at.code.set(asset_type_name)
            elif not skip_existing:
                at = self._asset_types[asset_type_name]
            else:
                continue
            
            print(f'Create asset type: {data["name"]}')

            if not at.assets.has_mapped_name(name):
                a = at.assets.add(name)
                a.display_name.set(name)
                a.code.set(name)
        
        self._asset_types.touch()


class AssetTypeCollection(BaseAssetTypeCollection):

    create_assets = flow.Child(CreateKitsuAssetsFromTypes)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                path_format='lib/{asset_type}/{asset_family}/{asset}/{task}/{file_mapped_name}/{revision}/{asset}_{file_base_name}'
            )


class AssetLibrary(BaseAssetLibrary):

    asset_types = flow.Child(AssetTypeCollection).ui(expanded=True)


class CreateKitsuAssetLibs(flow.Action):
    '''
    When `create_assets` is enabled, the action creates types and assets
    all at once.
    '''
    
    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_assets = flow.SessionParam(False).ui(editor='bool')

    _asset_libs = flow.Parent()

    def get_buttons(self):
        return ['Create libraries', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        episodes_data = self.root().project().kitsu_api().get_episodes_data()
        create_assets = self.create_assets.get()
        skip_existing = self.skip_existing.get()

        episodes_data.append({'name': 'MAIN_PACK'}) # add Kitsu default asset episode

        for data in episodes_data:
            name = data['name']

            if name == 'x':
                continue

            if not self._asset_libs.has_mapped_name(name):
                al = self._asset_libs.add(name)
                al.display_name.set(name)
                al.code.set(name)
            elif not skip_existing:
                al = self._asset_libs[name]
            else:
                continue
            
            print(f'Create asset type: {data["name"]}')

            if create_assets:
                al.asset_types.create_assets.skip_existing.set(skip_existing)
                al.asset_types.create_assets.run('Create assets')
        
        self._asset_libs.touch()


class AssetLibraryCollection(BaseAssetLibraryCollection):
    
    create_libs = flow.Child(CreateKitsuAssetLibs).ui(label='Create asset libraries')
