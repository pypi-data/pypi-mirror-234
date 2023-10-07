#!/usr/bin/env python3
"""
USAGE:
    # cli
    vaticinator [options]
    
    # python
    from vaticinator import Vaticinator
    vat = Vaticinator()
    print(vat.fortune)
"""
import sys
import re
from argparse import ArgumentParser, Namespace
from logging import warn, debug, getLogger, INFO, DEBUG, WARN
# from random import randint
# import os
# from functools import cached_property, lru_cache
# from pathlib import Path

from vaticinator.fortune_file import (
    # FortuneFile, FortuneDirectory,
    FortuneCollection, DEFAULT_FORTUNE_PATH
    )


class Vaticinator:
    VALID_FLAGS = ('all', 'show_file', 'equal', 'list_files', 'long', 'off',
                   'short', 'ignore_case', 'wait', 'u', 'verbose', 'debug')
    VALID_ARGS = {'match': str, 'short_max': int, "params": list}

    def __init__(self, cmd_args=None, params=[], *args, **kwargs):
        self._args = cmd_args
        self._sources = FortuneCollection()
        self.set_default_options()
        if params or args or kwargs:
            self.process_options(params, *args, **kwargs)

    def __str__(self):
        return 'Vaticinator'

    def main(self, main_args=None):
        debug('main')
        args = main_args or self._args or sys.argv[1:]
        self.process_args(args)
        return self.run()

    @property
    def get_options(self):
        return self._options

    @get_options.setter
    def set_options(self, val):
        if val is None:
            return
        if not isinstance(val, Namespace):
            raise TypeError('Vaticinator.options must be of type '
                            + f'argparse.Namespace ({val} is of '
                            + f'type {type(val)})')
        self._options = val
        self.process_log_level()

    def set_default_options(self):
        kwargs = {'match': None, 'short_max': 160, 'params': []}
        for flag in self.VALID_FLAGS:
            kwargs.setdefault(flag, False)
        self.options = Namespace(**kwargs)

    def process_log_level(self):
        if self.options.debug:
            getLogger().setLevel(DEBUG)
        elif self.options.verbose:
            getLogger().setLevel(INFO)
        else:
            getLogger().setLevel(WARN)

    def process_args(self, args=None):
        parser = ArgumentParser()
        parser.add_argument('-a', '--all', action='store_true',
                            help='Choose from all lists of maxims, '
                            + 'both offensive and not.')
        parser.add_argument('-c', '--show-file', action='store_true',
                            help='Show the cookie file from which the '
                            + 'fortune came.')
        parser.add_argument('-e', '--equal', action='store_true',
                            help='Consider all fortune files to be of '
                            + 'equal size.')
        parser.add_argument('-f', '--list-files', action='store_true',
                            help='Print out the list of files which '
                            + 'would be searched; don’t print a fortune.')
        parser.add_argument('-l', '--long', action='store_true',
                            help='Long dictums only.')
        parser.add_argument('-m', '--match', type=str,
                            help='Print out all fortunes which match the '
                            + 'basic regular expression pattern.')
        parser.add_argument('-n', '--short-max', default=160, type=int,
                            help='Set the longest fortune length '
                            + 'considered short.')
        parser.add_argument('-o', '--off', action='store_true',
                            help='Choose only from potentially '
                            + 'offensive aphorisms.')
        parser.add_argument('-s', '--short', action='store_true',
                            help='Short apothegms only.')
        parser.add_argument('-i', '--ignore-case', action='store_true',
                            help='Ignore case for -m patterns.')
        parser.add_argument('-w', '--wait', action='store_true',
                            help='Wait before termination for an amount of '
                            + 'time calculated from the number of '
                            + 'characters in the message.')
        parser.add_argument('-u', action='store_true',
                            help="Don’t translate UTF-8 fortunes to the "
                            + 'locale when searching or translating.')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-d', '--debug', action='store_true')
        parser.add_argument('params', metavar='arg', nargs='*',
                            help='[#%%] file/directory/all')
        self.options = parser.parse_args(args)
        self.process_log_level()
        self.process_params()
        return self.options

    def process_options(self, *args, **kwargs):
        for arg in args:
            if arg in self.VALID_FLAGS and arg not in kwargs:
                kwargs[arg] = True
        for k, v in kwargs.items():
            if k not in (self.VALID_FLAGS + tuple(self.VALID_ARGS.keys())):
                warn(f'option "{k}" not recognized!')
                del kwargs[k]
            if (k in self.VALID_FLAGS and type(v) is not bool) or \
               (k in self.VALID_ARGS and type(v) is not self.VALID_ARGS[k]):
                warn(f'"{k}" is not valid for option {k}')
                del kwargs[k]
        for k, v in kwargs.items():
            setattr(self.options, k, v)
        self.process_log_level()
        self.process_params()
        return self.options

    def process_params(self, param_args=None):
        params = list(filter(None,
                             param_args
                             or self.options.params
                             or [DEFAULT_FORTUNE_PATH]))
        debug(f'{self}.process_file_params({params})')
        self._sources.clear()
        while len(params):
            next_weight = None
            next_sym = params.pop(0)
            if m := re.fullmatch(r'([0-9]+)%?', next_sym):
                next_weight = m.group(0)
                next_sym = params.pop(0)
            self._sources.add_path(next_sym, next_weight)

    def run(self, cmd=[], params=[], *args, **kwargs):
        debug('run')
        if cmd:
            self.process_args(cmd)
        if params or args or kwargs:
            self.process_options(params, *args, **kwargs)
        if self.options.list_files:
            print('\n'.join([
                str(f.path) for f
                in self._sources.walk_files()]))
            return 0
        fortune = self.fortune
        if self.options.show_file:
            print(fortune.source_file.path)
            return 0
        # elif self.options.version:
        #     pass
        else:
            print(fortune)
            return 0

    @property
    def fortune(self):
        return self._sources.get_random_fortune(self.options)
