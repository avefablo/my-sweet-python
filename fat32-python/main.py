import re
from os import mkdir
from os.path import isfile
from sys import argv

import readline

from abstract_app import AbstractApplication
from completer import PathCompleter
from fat_fs_lib.entries import FileEntry
from misc import KindOfEntries
from misc import unescape_spaces


class ConsoleApplication(AbstractApplication):
    """Console utility"""

    def __init__(self, filename):
        super().__init__(open(filename, 'rb'))
        completer_types = {'ls': None, 'cat': KindOfEntries.files,
                           'cd': KindOfEntries.dirs,
                           'save': KindOfEntries.files}
        self.string_pwd = '/'
        self.completer = PathCompleter(completer_types,
                                       self.pwd_entry.files_entries,
                                       self.pwd_entry.dirs_entries)
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind('tab: complete')
        self.input_loop()

    def input_loop(self):
        """Main loop of utility"""
        argument_regex = re.compile(r'(?<!\\) ')
        commands = {"cd": self.console_cd, "save": self.console_save,
                    "ls": self.console_ls, "cat": self.console_cat}
        while True:
            raw_args = input("%s -> " % self.string_pwd)
            arguments = argument_regex.split(raw_args)
            cmd = arguments[0]
            files = arguments[1:]
            if len(arguments) == 0:
                print('help')
            if cmd == 'exit':
                self.raw.close()
                exit(0)
            elif cmd in commands:
                commands[cmd](files)
            else:
                print('Unrecognized command')

    def console_cd(self, paths):
        """Function that change dir
        and change pwd_string"""
        if len(paths) != 1:
            print('cd: chande directory. Usage: cd dir_name')
            return
        else:
            path = unescape_spaces(paths[0])
            if path == '.':
                return
            entry = self.get_entry(path)
            if entry and entry.is_dir():
                self.cd(entry)
                self.generate_new_pwd(path)
                self.completer.files = self.pwd_entry.files_entries
                self.completer.dirs = self.pwd_entry.dirs_entries
            else:
                print('No such directory')

    def console_save(self, files):
        """
        Function that saves files to dir "saved"
        """
        if not files:
            print('save: saving files to subdir "saved". '
                  'Usage: save file_name')
            return
        files_with_unpacked_wildcards = self.open_wildcards(files)
        if not files_with_unpacked_wildcards:
            print('Files not found')
            return
        try:
            mkdir('saved')
        except FileExistsError:
            pass
        for file_name in files_with_unpacked_wildcards:
            entry = self.get_entry(file_name)
            if entry and type(entry) is FileEntry:
                for percentage in self.save(entry):
                    print("\r{}%".format(percentage), end='')
                print('\nSaved to saved/%s' % entry.get_name())
            elif entry and type(entry) is not FileEntry:
                print('You try to save not file entry')
            else:
                print('No such file %s' % file_name)
        pass

    def get_percentage(self, saved, total):
        """Return percentage of already copied data"""
        return '\r{}%'.format(int(saved / total * 100))

    def console_cat(self, files):
        """Function that show data in prompt"""
        if not files:
            print('cat: show content of files. Usage: cat file_name')
            return
        files_with_unpacked_wildcards = self.open_wildcards(files)
        if not files_with_unpacked_wildcards:
            print('Files not found')
            return
        for file_name in files_with_unpacked_wildcards:
            entry = self.get_entry(file_name)
            if entry and type(entry) is FileEntry:
                print(entry.get_name())
                for fragment in self.cat(entry):
                    print(fragment, end='')
                print('\n')
            elif entry and type(entry) is not FileEntry:
                pass
            else:
                print('No such file %s' % file_name)

    def console_ls(self, files):
        """List directory or files that apply for mask"""
        if not files:
            entries = self.pwd_entry.entries
        else:
            entries = [self.get_entry(i) for i in self.open_wildcards(files)]
        for entry in self.ls(entries):
            print(self.get_ls_string(entry))

    def get_ls_string(self, entry):
        """
        Return fancy string for ls
        """
        attributes = ['-'] * 5
        if entry.is_dir():
            attributes[0] = 'd'
        if not entry.is_readonly():
            attributes[1] = 'w'
        if entry.is_archive():
            attributes[2] = 'a'
        if entry.is_long_file_name():
            attributes[3] = 'l'
        if entry.is_system():
            attributes[4] = 's'
        return ''.join(attributes) + ' ' + entry.get_name()

    def generate_new_pwd(self, new_entry):
        """
        Change pwd_string
        """
        if new_entry == '..':
            self.string_pwd = self.string_pwd[:self.string_pwd.rfind('/')]
            if self.string_pwd == '':
                self.string_pwd = '/'
        else:
            if self.string_pwd == '/':
                self.string_pwd += new_entry
            else:
                self.string_pwd += '/' + new_entry

    def get_entry(self, name):
        """Return entry that apply for name"""
        entry = [f for f in self.pwd_entry.entries if f.get_name() == name]
        if entry:
            return entry[0]
        else:
            return None

    def open_wildcards(self, arguments):
        """Open filename wildcards '*' & '?'"""
        entries_names = []
        for arg in arguments:
            arg = unescape_spaces(arg)
            arg = re.escape(arg)
            arg = arg.replace('\\*', '.*')
            arg = arg.replace('\\?', '.')
            pattern = re.compile(arg + '$')
            for entry in self.pwd_entry.entries:
                name = entry.get_name()
                if re.match(pattern, name):
                    if name not in entries_names and name not in {'.', '..'}:
                        entries_names.append(name)
        return entries_names


if __name__ == '__main__':
    if len(argv) > 1:
        if isfile(argv[1]) or argv[1].startswith('/dev'):
            ConsoleApplication(argv[1])
        else:
            print('No such file')
            exit(0)
    else:
        print("Launch py main.py fat32_image")
        exit(0)