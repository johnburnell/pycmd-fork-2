#
# Basic mechanism for customizing PyCmd
#
import os, traceback, pycmd_public

class Settings(object):
    """
    Generic settings class; extend this to create a "group" of options
    (accessible as instance members in the settings.py files)
    """
    def sanitize(self):
        """Make sure the settings have sane values"""
        pass

    
class Appearance(Settings):
    """Appearance settings"""

    def __init__(self):
        # Prompt function (should return a string)
        self.prompt = pycmd_public.abbrev_path_prompt

    def sanitize(self):
        if not callable(self.prompt):
            print 'Prompt function doesn\'t look like a callable; reverting to PyCmd\'s default prompt'
            self.prompt = pycmd_public.abbrev_path_prompt


class Behavior(Settings):
    """Behavior settings"""
    def __init__(self):
        # Skip splash message (welcome and bye).
        # This can be also overriden with the '-Q' command line argument'
        self.quiet_mode = False
        
        # Select the completion mode; currently supported: 'bash'
        self.completion_mode = 'bash'

    def sanitize(self):
        if not self.completion_mode in ['bash']:
            print 'Invalid setting "' + self.completion_mode + '" for "completion_mode" -- using default "bash"'
            self.completion_mode = 'bash'


def apply_settings(settings_file):
    """
    Execute a configuration file (if it exists), overriding values from the
    global configuration objects (created when this module is loaded)
    """
    if os.path.exists(settings_file):
        try:
            # We initialize the dictionary to readily contain the settings
            # structures; anything else needs to be explicitly imported
            execfile(settings_file, {'appearance': appearance,
                                     'behavior': behavior})
        except Exception, e:
            print 'Error encountered when loading ' + settings_file
            print 'Subsequent settings will NOT be applied!'
            traceback.print_exc()

def sanitize():
    """Sanitize all the configuration instances"""
    appearance.sanitize()
    behavior.sanitize()

# Initialize global configuration instances with default values
#
# These objects are directly manipulated by the settings.py files, executed via
# apply_settings(). Then, they are directly used by PyCmd.py to get the current
# configuration settings
appearance = Appearance()
behavior = Behavior()