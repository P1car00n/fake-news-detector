import configparser
import os

class Configurator:
    def __init__(self, folder=''): #
        self.config = configparser.ConfigParser()
        if not os.path.exists(path_to_check := './settings'): #
            os.makedirs(path_to_check)
            self.config.add_section('Preferences')
            self.config['Preferences']['theme'] = 'clam'
            self.config['Preferences']['mode'] = 'advanced'
            self.update_pref()
        
        self.config.read('./settings/preferences.ini') #

    def update_pref(self, **kwargs): # can be replaced with read_dict
        for key, value in kwargs:
            self.config['Preferences'][key] = value
        with open('settings/preferences.ini', 'w') as configfile: #
            self.config.write(configfile)
    
    def get_prefs(self):
        return dict(self.config.items('Preferences'))

if __name__ == '__main__':
    test = Configurator()
    test.get_prefs()


#theme = config['Preferences']['theme']
#mode = config['Preferences']['mode']

