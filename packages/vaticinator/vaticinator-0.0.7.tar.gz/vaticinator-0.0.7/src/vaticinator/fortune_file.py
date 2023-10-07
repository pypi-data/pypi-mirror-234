"""
provides an interface for fortune-style .dat files.

Contains:
    - FortuneFile
    - FortuneFileError
"""
from pathlib import Path
from logging import warn, debug, info
from random import randint
from functools import lru_cache
from collections import UserString
import struct
import os
import re


DEFAULT_FORTUNE_PATH = '/usr/share/games/fortunes'
MAX_TRIES = 1000


class Fortune(UserString):
    def __init__(self, init=None, source=None):
        super().__init__(init)
        self.source_file = source


class FortuneFileError(BaseException):
    pass


class FortuneObject:
    # @lru_cache
    @staticmethod
    def get_object(path, weight=None):
        path = path if isinstance(path, Path) else Path(path)
        obj = FortuneDirectory(path, weight) \
            if path.is_dir() else \
            FortuneFile(path, weight)
        debug(f'FortuneObject.get_object({path}, {weight}) => {obj}')
        return obj

    def __init__(self, path, weight=None):
        debug(f'FortuneObject({path}, {weight})')
        self._path = Path(path)
        self.weight = weight

    def __str__(self):
        cls = getattr(self, '__thisclass__', getattr(self, '__class__'))
        return f'{cls.__name__}({self._path}, {self.weight})'

    @property
    def length(self):
        return 0

    @property
    def path(self):
        return self._path

    @path.setter
    def set_path(self, path):
        raise NotImplementedError


class FortuneFile(FortuneObject):
    """Interface for fortune-style .dat files"""

    def __init__(self, path, weight=None):
        FortuneObject.__init__(self, path, weight)
        self._offsets = []
        (self._version, self._length,
         self._longest, self._shortest) = (0, 0, 0, 0)

    def __str__(self):
        return f'{super().__str__()}: {self.length} entries'

    @property
    def offsets(self):
        self.load_file(self.path)
        return self._offsets

    @property
    def data_path(self):
        return self.path.parent / self.path.stem

    @property
    def length(self):
        self.load_file(self.path)
        return self._length

    @property
    def version(self):
        self.load_file(self.path)
        return self._version

    @property
    def longest(self):
        self.load_file(self.path)
        return self._longest

    @property
    def shortest(self):
        self.load_file(self.path)
        return self._shortest

    @lru_cache
    def load_file(self, fn):
        debug(f'load_file({fn})')
        if self.path.exists() and self.data_path.exists():
            try:
                with self.path.open('rb') as dat:
                    header = struct.unpack('>IIIIIcxxx', dat.read(24))
                    (self._version, self._length,
                     self._longest, self._shortest) = header[0:4]
                    self._offsets = [
                        struct.unpack('>I', dat.read(4))[0]
                        for i in range(self._length + 1)
                        ]
            except Exception as e:     # noqa: E722
                warn(f'error reading fortune file "{fn}"!  {e}')
                raise FortuneFileError(e)
        else:
            warn(f'fortune file "{fn}" not found!')
            raise FortuneFileError

    def get_random_fortune(self, options):
        debug(f'FortuneFile.get_random_fortune({options})')
        fortune = None
        for i in range(1, MAX_TRIES):
            try:
                num = randint(1, self.length)
                fortunes_all = self.data_path.read_bytes()
                debug(f'fortunes length: {len(fortunes_all)}')
                debug(f'number of offsets: {self.length} ({len(self.offsets)})')
                debug(f'random number: {num}')
                debug(
                    f'offsets: {self.offsets[num - 1]} - {self.offsets[num] - 2}')
                debug(f'starts with {fortunes_all[self.offsets[num - 1]]}')
                fortune_bytes = fortunes_all[self.offsets[num - 1]:
                                             self.offsets[num] - 2]
                fortune = fortune_bytes.decode()
                debug(f'fortune: {fortune}')
                flags = re.I if options.ignore_case else re.NOFLAG
                if options.match:
                    debug(f'match: {options.match}')
                if ((options.match and not re.search(options.match, fortune, flags))
                        or (options.short and len(fortune) > options.short_max)
                        or (options.long and len(fortune) < options.short_max)):
                    continue
                return Fortune(fortune, self)
            except UnicodeDecodeError:
                warn('unicode decode error')
        else:
            return 'No fortune today!'


class FortuneCollection:
    def __init__(self):
        self.files = []

    def __str__(self):
        return 'FortuneCollection'

    def add_path(self, path, weight=None):
        info(f'{self}.add_path({path}, {weight})')
        obj = FortuneObject.get_object(path, weight)
        if obj.length:
            self.files.append(obj)
            debug(f'added {obj}')
        else:
            info(f'found no entries in {path}!')

    def clear(self):
        self.files.clear()

    @property
    def filenames(self):
        filenames = list([str(file) for file in self.files])
        debug(f'{self}.filenames files={filenames}')
        return filenames

    def walk_files(self, final=True):
        all_files = self.files
        for file in self.files:
            if isinstance(file, FortuneDirectory):
                all_files += file.walk_files(False)
        return sorted(all_files, key=lambda f: f.path) \
            if final \
            else all_files

    @property
    def length(self):
        return len(list(self.files))

    def get_random_fortune(self, options):
        ff = self.get_random_file(options)
        return ff.get_random_fortune(options) if ff else 'No fortune found'

    def get_random_file(self, options):
        debug(f'{self}.get_random_file({options}) files: {self.filenames}')
        total_weighted = sum(
            [f.weight for f in self.files if f.weight is not None])
        unweighted = filter(lambda f: f.weight is None, self.files)
        total_unweighted_lines = sum(
            [f.length for f in unweighted if not f.weight])
        remaining_pct = max(0, 100 - total_weighted)
        debug({
            'weighted': total_weighted,
            'unweighted': total_unweighted_lines
            })
        for f in unweighted:
            f.weight = (f.length / total_unweighted_lines) * \
                (remaining_pct / 100)
        sel_files = list(self.files).copy()
        c = sum(filter(None, [f.weight for f in sel_files]))
        r = randint(0, c)
        sel = None
        for file in sel_files:
            r -= file.length
            if r < 0:
                sel = file
        else:
            if len(sel_files):
                sel = sel_files[0]
            else:
                return None
        debug(f'{self}.get_random_file() => {sel}')
        return (sel
                if isinstance(sel, FortuneFile)
                else sel.get_random_file(options)
                if isinstance(sel, FortuneDirectory)
                else None)


class FortuneDirectory(FortuneObject, FortuneCollection):
    def __init__(self, path, weight=None):
        debug(f'FortuneDirectory({path}, {weight})')
        FortuneCollection.__init__(self)
        FortuneObject.__init__(self, path, weight)
        for path in [
                self.path / p for p
                in os.listdir(self.path)
                if p.endswith('.dat')
                ]:
            self.add_path(path, weight)

    def __str__(self):
        return FortuneObject.__str__(self)

    def get_random_fortune(self, options):
        return FortuneCollection.get_random_fortune(self, options)

    @property
    def length(self):
        return len(list(self.files))

    @property
    @lru_cache
    def _files(self):
        for path in [
                self.path / p for p
                in os.listdir(self.path)
                if p.endswith('.dat')
                ]:
            yield FortuneObject.get_object(path)

    def error(self):
        raise NotImplementedError
