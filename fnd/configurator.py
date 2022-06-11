import configparser
import os


class Configurator:
    def __init__(self, folder='./settings', file_name='preferences.ini'):
        self.config = configparser.ConfigParser()

        # subject of rewrite to accept one path whole
        self._file_path = folder + '/' + file_name

        if not os.path.exists(folder):
            os.makedirs(folder)
            self.config.add_section('Preferences')
            self.config['Preferences']['theme'] = 'arc'
            self.config['Preferences']['mode'] = 'simple'
            self.update_pref()

        self.config.read(self._file_path)

    def update_pref(self, **kwargs):  # can be replaced with read_dict
        for key, value in kwargs.items():
            self.config['Preferences'][key] = value
        with open(self._file_path, 'w') as configfile:
            self.config.write(configfile)

    def get_prefs(self):
        return dict(self.config.items('Preferences'))


if __name__ == '__main__':
    test = Configurator()
    test.get_prefs()


#theme = config['Preferences']['theme']
#mode = config['Preferences']['mode']
