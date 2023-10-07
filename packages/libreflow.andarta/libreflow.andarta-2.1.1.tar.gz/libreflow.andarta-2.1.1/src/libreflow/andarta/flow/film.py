import re
from kabaret import flow
from libreflow.baseflow.film import Film as BaseFilm
from libreflow.baseflow.film import FilmCollection as BaseFilmCollection


class CreateKitsuSequences(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_shots = flow.SessionParam(False).ui(editor='bool')
    create_task_default_files = flow.SessionParam(True).ui(editor='bool')
    name_regex = flow.SessionParam('SQ\d+').ui(hidden=True)
    shot_name_regex = flow.SessionParam('SH\d+').ui(hidden=True)

    _film = flow.Parent()

    def get_buttons(self):
        return ['Create sequences', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        name_regex = self.name_regex.get()
        sequences_data = self.root().project().kitsu_api().get_sequences_data(
            episode_name=self._film.display_name.get()
        )
        for data in sequences_data:
            match_regex = re.search(name_regex, data['name'])
            if match_regex is None:
                print((f'Create Kitsu sequences :: sequence \'{data["name"]}\' skipped '
                    '(name does not match provided filter)'))
                continue

            display_name = data['name']
            object_name = match_regex.group(0)

            if not self._film.sequences.has_mapped_name(object_name):
                s = self._film.sequences.add(object_name)
                s.display_name.set(display_name)
                s.code.set(object_name)
            elif not self.skip_existing.get():
                s = self._film.sequences[object_name]
            else:
                continue
            
            print(f'Create sequence {data["name"]}')

            if self.create_shots.get():
                s.create_shots.skip_existing.set(self.skip_existing.get())
                s.create_shots.create_task_default_files.set(self.create_task_default_files.get())
                s.create_shots.name_regex.set(self.shot_name_regex.get())
                s.create_shots.run('Create shots')
        
        self._film.sequences.touch()


class Film(BaseFilm):

    create_sequences = flow.Child(CreateKitsuSequences)


class CreateKitsuFilms(flow.Action):

    '''
    Create Films based on Kitsu episodes
    '''

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_sequences = flow.SessionParam(False).ui(editor='bool')
    create_shots = flow.SessionParam(False).ui(editor='bool')
    create_task_default_files = flow.SessionParam(True).ui(editor='bool')
    name_regex = flow.SessionParam('E\d+|TEST_PIPE').ui(hidden=True)
    seq_name_regex = flow.SessionParam('SQ\d+').ui(hidden=True)
    shot_name_regex = flow.SessionParam('SH\d+').ui(hidden=True)

    _films = flow.Parent()

    def get_buttons(self):
        return ['Create films', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return

        episodes_data = self.root().project().kitsu_api().get_episodes_data()
        name_regex = self.name_regex.get()

        for data in episodes_data:
            match_regex = re.search(name_regex, data['name'])
            if match_regex is None:
                print((f'Create Kitsu episodes :: episode \'{data["name"]}\' skipped '
                    '(name does not match provided filter)'))
                continue
            
            display_name = data['name']
            object_name = match_regex.group(0)

            if not self._films.has_mapped_name(object_name):
                f = self._films.add(object_name)
                f.display_name.set(display_name)
                f.code.set(object_name)
            elif not self.skip_existing.get():
                f = self._films[object_name]
            else:
                continue
            
            print(f'Create film {data["name"]}')

            if self.create_sequences.get():
                f.create_sequences.skip_existing.set(self.skip_existing.get())
                f.create_sequences.create_shots.set(self.create_shots.get())
                f.create_sequences.create_task_default_files.set(self.create_task_default_files.get())
                f.create_sequences.name_regex.set(self.seq_name_regex.get())
                f.create_sequences.shot_name_regex.set(self.shot_name_regex.get())
                f.create_sequences.run('Create sequences')
        
        self._films.touch()


class FilmCollection(BaseFilmCollection):

    create_films = flow.Child(CreateKitsuFilms)
