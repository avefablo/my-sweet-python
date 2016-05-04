#!/usr/bin/python3.5

from os.path import isfile
from sys import argv

import drawer
from bmp_opener import BMPOpener


class Launcher:
    def __init__(self):
        no_draw_options = Option('no draw', ['-d', '--nodraw'],
                                 'prevent drawing picture')
        quiet_options = Option('quiet', ['-q', '--quiet'],
                               'prevent showing info in tty')
        no_check_options = Option('no check', ['-c', '--nocheck'],
                                  'prevent checking fields in bmp')
        help_options = Option('help', ['-h', '--help'],
                              'show help')
        all_pseudonyms = []
        for option in [no_draw_options, quiet_options,
                       no_check_options, help_options]:
            all_pseudonyms += option.pseudonyms
        self.available_options = [no_check_options, no_draw_options,
                                  help_options, quiet_options]
        options = [arg for arg in argv[1:] if not isfile(arg)]
        files_to_open = [arg for arg in argv[1:] if isfile(arg)]
        if any(x in argv for x in help_options.pseudonyms):
            self.show_usage()
            self.show_available_options()
            exit()
        if any(x not in all_pseudonyms for x in options):
            print("There is a mistake in some option")
            print("Use py launcher.py -h to see help")
            exit()
        if not files_to_open:
            self.show_usage()
            exit()
        for file in files_to_open:
            self.bmp = BMPOpener(file).bmp_file
            if all(x not in argv for x in no_check_options.pseudonyms):
                self.bmp.validate()
            if all(x not in argv for x in quiet_options.pseudonyms):
                self.bmp.print_info()
            if all(x not in argv for x in no_draw_options.pseudonyms):
                self.bmp.parse_pixels()
                drawer.main(self.bmp)

    def show_usage(self):
        print("""Launch py launcher.py {path_to_bmp}""")

    def show_available_options(self):
        for option in self.available_options:
            print(option)


class Option:
    def __init__(self, name, pseudonyms, description):
        self.description = description
        self.pseudonyms = pseudonyms
        self.name = name

    def __str__(self):
        return "{}: can be called by {} and {}".format(self.name,
                                                       self.pseudonyms,
                                                       self.description)


if __name__ == "__main__":
    Launcher()
