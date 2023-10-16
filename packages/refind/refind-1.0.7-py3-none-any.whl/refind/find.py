# MIT License
#
# Copyright (c) 2023 James Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import threading
from enum import Enum
import enum
import fnmatch
import re
import subprocess
import time
import math
from datetime import datetime, timedelta
import glob
import stat
import io
import textwrap
from typing import Any, Union, List

__version__ = '1.0.7'
PACKAGE_NAME = 'refind'

try:
    import grp
except ModuleNotFoundError:
    GID_ENABLED = False

    def _group_id_to_name(id:int) -> str:
        return 'N/A'

    def _group_name_to_id(name:str) -> int:
        return -1
else:
    GID_ENABLED = True

    def _group_id_to_name(id:int) -> str:
        return grp.getgrgid(id).gr_name

    def _group_name_to_id(name:str) ->int:
        return grp.getgrnam(name).gr_gid

try:
    import pwd
except ModuleNotFoundError:
    UID_ENABLED = False

    def _user_id_to_name(id:int) -> str:
        return 'N/A'

    def _user_name_to_id(name:str) -> int:
        return -1
else:
    UID_ENABLED = True

    def _user_id_to_name(id:int) -> str:
        return pwd.getpwuid(id).pw_name

    def _user_name_to_id(name:str) -> int:
        return pwd.getpwnam(name).pw_uid

def _is_windows():
    return sys.platform.lower().startswith('win')

class SharedFileWriter:
    ''' Simple file writer used when multiple objects need to write to the same file '''
    files = {}
    files_mutex = threading.Semaphore(1)

    def __init__(self, file_path, binary=True, append=False):
        file_path = os.path.abspath(file_path)
        self._file_path = file_path
        with __class__.files_mutex:
            if file_path not in __class__.files:
                if append:
                    mode = 'a'
                else:
                    mode = 'w'

                if binary:
                    mode += 'b'

                __class__.files[file_path] = {
                    'file': open(file_path, mode),
                    'count': 0
                }
            self._file_entry = __class__.files[file_path]
            self._file_entry['count'] += 1
            self._file = self._file_entry['file']
        # Copy over write and flush methods
        self.write = self._file.write
        self.flush = self._file.flush

    def __del__(self):
        with __class__.files_mutex:
            __class__.files[self._file_path]['count'] -= 1
            if __class__.files[self._file_path]['count'] <= 0:
                # File is no longer used
                del __class__.files[self._file_path]
                self._file.close()

class FindType(Enum):
    BLOCK = 'b'
    CHARACTER = 'c'
    DIRECTORY = 'd'
    NAMED_PIPE = 'p'
    FILE = 'f'
    SYMBOLIC_LINK = 'l'
    SOCKET = 's'

class RegexType(Enum):
    PY = enum.auto()
    SED = enum.auto()
    EGREP = enum.auto()

class ValueComparison(Enum):
    EQUAL_TO = enum.auto()
    GREATER_THAN = enum.auto()
    LESS_THAN = enum.auto()

class LogicOperation(Enum):
    OR = enum.auto()
    AND = enum.auto()

class PathParser:
    ''' This class helps to parse each element that needs to be matched/executed in find '''
    def __init__(self, find_root, path_split=None):
        '''
        Initialize the PathParser object for use with Finder.
        Inputs: find_root - The root that we are interrogating
                path_split - When set, A 2-item tuple or list containing the head and tail of the
                             path; the head must begin with find_root and must be a directory
                             When not set, find_root is the path being interrogated
        '''
        self._find_root = find_root
        if path_split:
            if len(path_split) != 2:
                raise ValueError('path_split is not length of 2: {}'.format(path_split))
            elif not path_split[0].startswith(find_root):
                raise ValueError(
                    'Expected root "{}" to begin with find_root "{}"'.format(path_split[0], find_root)
                )
            self._root = path_split[0]
            self._name = path_split[1]
            self._rel_dir = self._root[len(find_root):]
            if self._rel_dir:
                self._rel_dir = os.path.normpath(self._rel_dir)
                if self._rel_dir.startswith(os.sep):
                    self._rel_dir = self._rel_dir[1:]
            self._full_path = os.path.join(self._root, self._name)
        else:
            self._root = ''
            self._rel_dir = ''
            self._name = find_root
            self._full_path = find_root
        # Saves value of previous call to os.stat()
        self._stat = None

    @property
    def find_root(self):
        ''' Returns the find root currently being interrogated '''
        return self._find_root

    @property
    def root(self):
        ''' Returns the directory path of the current item '''
        if self._root:
            return self._root
        else:
            return self._find_root

    @property
    def rel_dir(self):
        ''' Returns the directory relative to the find root for the current item '''
        return self._rel_dir

    @property
    def name(self):
        ''' Returns the base name of the item '''
        return self._name

    @property
    def full_path(self):
        ''' Returns the full path to the item '''
        return self._full_path

    def __str__(self) -> str:
        return self._full_path

    def _set_stat(self):
        if self._stat is None:
            try:
                self._stat = os.stat(self.full_path)
            except OSError:
                pass

    @property
    def stat(self):
        self._set_stat()
        return self._stat

    def get_type(self):
        ''' Returns the FindType of the item or None if it cannot be determined '''
        self._set_stat()
        if self._stat is None:
            return None
        mode = self._stat.st_mode
        if stat.S_ISLNK(mode):
            return FindType.SYMBOLIC_LINK
        elif stat.S_ISDIR(mode):
            return FindType.DIRECTORY
        elif stat.S_ISBLK(mode):
            return FindType.BLOCK
        elif stat.S_ISCHR(mode):
            return FindType.CHARACTER
        elif stat.S_ISFIFO(mode):
            return FindType.NAMED_PIPE
        elif stat.S_ISSOCK(mode):
            return FindType.SOCKET
        elif stat.S_ISREG(mode):
            return FindType.FILE
        else:
            return None

    def get_rel_depth(self):
        '''
        Returns the depth of the item where 0 is the find_root itself, 1 is an item directly under
        find_root, etc.
        '''
        if not self._root:
            return 0
        elif self._root == self._find_root:
            return 1
        depth = len(self._rel_dir.split(os.sep)) + 1
        return depth

    def to_pydict(self):
        ''' Returns the dictionary used in -py* actions '''
        t = self.get_type()
        d = {
            "full_path": self.full_path,
            "root": self.root,
            "rel_dir": self.rel_dir,
            "name": self.name,
            "find_root": self.find_root,
            "type": t.value if t else '-',
            "depth": self.get_rel_depth()
        }
        self._set_stat()
        if self._stat is not None:
            d.update({k: getattr(self._stat, k) for k in dir(self._stat) if k.startswith('st_')})
            d['atime'] = datetime.fromtimestamp(self._stat.st_atime)
            d['ctime'] = datetime.fromtimestamp(self._stat.st_ctime)
            d['mtime'] = datetime.fromtimestamp(self._stat.st_mtime)
            d['mode_oct'] = oct(self._stat.st_mode)[2:]
            d['perm_oct'] = oct(self._stat.st_mode & 0o777)[2:]
            d['perm'] = stat.filemode(self._stat.st_mode)
            d['group'] = _group_id_to_name(self._stat.st_gid)
            try:
                d['link'] = os.readlink(self.full_path)
            except OSError:
                d['link'] = ''
            d['user'] = _user_id_to_name(self._stat.st_uid)
        else:
            d['st_atime'] = 0.0
            d['st_atime_ns'] = 0
            d['st_blksize'] = 0
            d['st_blocks'] = 0
            d['st_ctime'] = 0.0
            d['st_ctime_ns'] = 0
            d['st_dev'] = 0
            d['st_gid'] = 0
            d['st_ino'] = 0
            d['st_mode'] = 0
            d['st_mtime'] = 0.0
            d['st_mtime_ns'] = 0
            d['st_nlink'] = 0
            d['st_rdev'] = 0
            d['st_size'] = 0
            d['atime'] = d['ctime'] = d['mtime'] = datetime.fromtimestamp(0)
            d['mode_oct'] = '00000'
            d['perm_oct'] = '000'
            d['perm'] = '----------'
            d['group'] = ''
            d['link'] = ''
            d['user'] = ''
        return d

class Action:
    ''' Action base class - executes something based on the matched path '''
    def handle(self, path_parser):
        pass

class PrintAction(Action):
    ''' Simply prints the full path of the item '''
    def __init__(self, end:str=None, file:io.IOBase=None, flush:bool=False):
        super().__init__()
        self._end = end
        self._file = file
        self._flush = flush

    def handle(self, path_parser):
        print(path_parser.full_path, end=self._end, file=self._file, flush=self._flush)

class PyPrintAction(Action):
    ''' Prints the item using python format string '''
    def __init__(self, format:str, end:str=None, file:io.IOBase=None, flush:bool=False):
        super().__init__()
        self._format = bytes(format, "utf-8").decode("unicode_escape")
        self._end = end
        self._file = file
        self._flush = flush

    def handle(self, path_parser):
        print_out = self._format.format(**path_parser.to_pydict())
        print(print_out, end=self._end, file=self._file, flush=self._flush)

class PrintfAction(Action):
    ''' Prints the item using printf format string '''

    # Group 1 is format specifier
    # Group 2 is printf type (0 to 2 characters in length)
    printf_search_pattern = re.compile(r'%([^a-zA-Z%{[(]*)(([A-CT].)|([a-zD-SU-Z%{[(])|($))')

    def __init__(self, format:str, end:str=None, file:io.IOBase=None, flush:bool=False):
        super().__init__()
        self._format_base = bytes(format, "utf-8").decode("unicode_escape")
        self._end = end
        self._file = file
        self._flush = flush

    @staticmethod
    def _replace_fn(item_dict, matchobj):
        format_specifier:str = matchobj.group(1)
        printf_type:str = matchobj.group(2)
        original_input = '%' + format_specifier + printf_type
        value = None
        if printf_type == '%' or printf_type == '\n' or printf_type == '':
            return original_input
        elif printf_type == 'a':
            value = '{atime:%a %b %d %H:%M:%S.%f %Y}'.format(**item_dict)
        elif printf_type == 'c':
            value = '{ctime:%a %b %d %H:%M:%S.%f %Y}'.format(**item_dict)
        elif printf_type == 't':
            value = '{mtime:%a %b %d %H:%M:%S.%f %Y}'.format(**item_dict)
        elif printf_type[0] in 'ABCT':
            t = printf_type[0]
            if t == 'A':
                time_str = 'atime'
            elif t == 'B':
                # Probably not right, but that's ok
                time_str = 'ctime'
            elif t == 'C':
                time_str = 'ctime'
            else:
                time_str = 'mtime'

            f = printf_type[1]
            if f == '@':
                value = item_dict['st_' + time_str]
            elif f == '+':
                value = f'{{{time_str}:%Y-%m-%d+%H:%M:%S.%f}}'.format(**item_dict)
            else:
                value = f'{{{time_str}:%{f}}}'.format(**item_dict)
        elif printf_type == 'd':
            value = item_dict['depth']
        elif printf_type == 'D':
            value = item_dict['st_dev']
        elif printf_type == 'f':
            value = item_dict['name']
        elif printf_type == 'g':
            value = item_dict['group']
        elif printf_type == 'G':
            value = item_dict['st_gid']
        elif printf_type == 'h':
            value = item_dict['root']
        elif printf_type == 'H':
            value = item_dict['find_root']
        elif printf_type == 'i':
            value = item_dict['st_ino']
        elif printf_type == 'l':
            value = item_dict['link']
        elif printf_type == 'm':
            value = item_dict['perm_oct']
        elif printf_type == 'M':
            value = item_dict['perm']
        elif printf_type == 'p':
            value = item_dict['full_path']
        elif printf_type == 'P':
            value = os.path.join(item_dict['rel_dir'], item_dict['name'])
            if value == item_dict['find_root']:
                value = ''
        elif printf_type == 's':
            value = item_dict['st_size']
        elif printf_type == 'u':
            value = item_dict['user']
        elif printf_type == 'U':
            value = item_dict['st_uid']
        elif printf_type == 'y':
            value = item_dict['type']

        if not value:
            # Not handled
            return original_input
        elif format_specifier:
            if isinstance(value, int):
                # Integer decimal format
                t = 'd'
            elif isinstance(value, str):
                # String format
                t = 's'
            elif isinstance(value, float):
                # Floating-point decimal format
                t = 'f'
            else:
                # Shouldn't reach here, but handle it as string
                value = str(value)
                t = 's'

            try:
                # As long as Python supports it, it's better to use the modulo operator here
                # since this conforms more closely to printf formatting
                return f'%{format_specifier}{t}' % value
            except ValueError:
                # Invalid format specifier
                return original_input
        else:
            return str(value)

    def handle(self, path_parser):
        item_dict = path_parser.to_pydict()
        replace_lambda = lambda matchobj : __class__._replace_fn(item_dict, matchobj)
        print_out = self.printf_search_pattern.sub(replace_lambda, self._format_base)
        print(print_out, end=self._end, file=self._file, flush=self._flush)

class ExecuteAction(Action):
    ''' Executes custom command where {} is the full path to the item '''
    def __init__(self, command:List[str]):
        super().__init__()
        self._command = command

    def handle(self, path_parser):
        command = list(self._command)
        for i in range(len(command)):
            command[i] = command[i].replace('{}', path_parser.full_path)
        process = subprocess.Popen(command)
        process.communicate()

class PyExecuteAction(Action):
    ''' Executes custom command where each element in the command is a format string '''
    def __init__(self, command:List[str]):
        super().__init__()
        self._command = command

    def handle(self, path_parser):
        command = list(self._command)
        d = path_parser.to_pydict()
        for i in range(len(command)):
            command[i] = command[i].format(**d)
        process = subprocess.Popen(command)
        process.communicate()

class DeleteAction(Action):
    ''' Deletes the matched item '''
    def __init__(self):
        super().__init__()

    def handle(self, path_parser):
        # Handle all except "."
        if path_parser.full_path != '.':
            if os.path.isdir(path_parser.full_path):
                try:
                    os.rmdir(path_parser.full_path)
                except OSError as err:
                    print(str(err), file=sys.stderr)
            else:
                try:
                    os.remove(path_parser.full_path)
                except OSError as err:
                    print(str(err), file=sys.stderr)

class Matcher:
    ''' Base matcher class which determines if an item is a match or not '''
    def __init__(self):
        self._invert = False

    def is_match(self, path_parser):
        result = self._is_match(path_parser)
        if result is None:
            # Error result - always false, regardless of self._invert
            result = False
        elif self._invert:
            result = not result
        return result

    def _is_match(self, path_parser):
        return False

    def set_invert(self, invert):
        self._invert = invert

class StaticMatcher(Matcher):
    ''' Statically return True or False for every item '''
    def __init__(self, value:bool):
        super().__init__()
        self._value = value

    def _is_match(self, path_parser):
        return self._value

class DefaultMatcher(StaticMatcher):
    ''' The default matcher when none specified '''
    def __init__(self):
        super().__init__(True)

class NameMatcher(Matcher):
    ''' Matches against the name of the item '''
    def __init__(self, pattern:str):
        super().__init__()
        self._pattern = pattern

    def _is_match(self, path_parser):
        return fnmatch.fnmatch(path_parser.name, self._pattern)

class FullPathMatcher(Matcher):
    ''' Matches against the full path of the item '''
    def __init__(self, pattern:str):
        super().__init__()
        self._pattern = pattern

    def _is_match(self, path_parser):
        return fnmatch.fnmatch(path_parser.full_path, self._pattern)

class RegexMatcher(Matcher):
    ''' Matches against the full path of the item using regex '''
    def __init__(self, pattern:str, regex_type:RegexType):
        super().__init__()
        self._regex_type = regex_type

        # Convert given regex type to Python re type
        if self._regex_type == RegexType.SED:
            # Main difference between sed and re is escaping is inverted in meaning for some chars
            pattern = self._pattern_escape_invert(pattern, '+?|{}()')
        # else: just use pattern as-is for re

        self._pattern = pattern

    @staticmethod
    def _pattern_escape_invert(pattern, chars):
        for char in chars:
            escaped_char = '\\' + char
            pattern_split = pattern.split(escaped_char)
            new_pattern_split = []
            for piece in pattern_split:
                new_pattern_split.append(piece.replace(char, escaped_char))
            pattern = char.join(new_pattern_split)
        return pattern

    def _is_match(self, path_parser):
        try:
            m = re.search(self._pattern, path_parser.full_path)
            return (m is not None)
        except:
            return False

class TypeMatcher(Matcher):
    ''' Matches against the item's type '''
    def __init__(self, *types:Union[FindType,str,List[FindType],List[str]]):
        super().__init__()
        self._type_list = []

        flattened_types_list = []
        for t in types:
            if isinstance(t, list):
                flattened_types_list.extend(t)
            else:
                flattened_types_list.append(t)

        for t in flattened_types_list:
            if isinstance(t, str):
                # Try to convert string to types
                for c in t:
                    # Don't require comma like find command, but also don't error out if they are included
                    if c != ',':
                        try:
                            self._type_list.append(FindType(c))
                        except ValueError:
                            raise ValueError('Unsupported or unknown type {} in types string: {}'.format(c, t))
            elif isinstance(t, FindType):
                self._type_list.append(t)
            else:
                raise TypeError(f'Invalid type: {type(t)} in given args {types}')

    @property
    def type_list(self):
        return self._type_list

    def _is_match(self, path_parser):
        return (path_parser.get_type() in self._type_list)

class StatTimeIncrementMatcher(Matcher):
    ''' Matches against os.stat time relative to current time '''
    def __init__(
            self,
            value_comparison:ValueComparison,
            rel_s:float,
            increment_s:float,
            current_time_s:float,
            stat_name:str
    ):
        super().__init__()
        self._value_comparison = value_comparison
        self._rel_s = rel_s
        self._rel_inc = math.floor(rel_s / increment_s)
        self._increment_s = increment_s
        self._current_time_s = current_time_s
        self._stat_name = stat_name

    def _is_match(self, path_parser):
        stat = path_parser.stat
        if stat is None:
            # Couldn't get stat
            return None

        # t should be positive
        t = self._current_time_s - self._get_stat_time(stat)
        t_inc = math.floor(t / self._increment_s)

        if self._value_comparison == ValueComparison.GREATER_THAN:
            return (t_inc > self._rel_inc)
        elif self._value_comparison == ValueComparison.LESS_THAN:
            return (t_inc < self._rel_inc)
        else:
            return (t_inc == self._rel_inc)

    def _get_stat_time(self, stat):
        return getattr(stat, self._stat_name)

class StatTimeMatcher(Matcher):
    ''' Matches against os.stat time to an absolute time '''
    def __init__(
            self,
            value_comparison:ValueComparison,
            stat_or_time:Union[os.stat_result,float],
            stat_name:str,
            r_stat_name:str=None
    ):
        super().__init__()
        self._value_comparison = value_comparison
        self._stat_name = stat_name
        if isinstance(stat_or_time, os.stat_result):
            if r_stat_name is None:
                r_stat_name = stat_name
            self._time_point = getattr(stat_or_time, r_stat_name)
        else:
            self._time_point = stat_or_time

    def _is_match(self, path_parser):
        stat = path_parser.stat
        if stat is None:
            # Couldn't get stat
            return None
        t = self._get_stat_time(stat)
        if self._value_comparison == ValueComparison.GREATER_THAN:
            return (t > self._time_point)
        elif self._value_comparison == ValueComparison.LESS_THAN:
            return (t < self._time_point)
        else:
            return (t == self._time_point)

    def _get_stat_time(self, stat):
        return getattr(stat, self._stat_name)

class EmptyMatcher(Matcher):
    ''' Matches when directory empty or file size is 0 bytes '''
    def __init__(self):
        super().__init__()

    def _is_match(self, path_parser):
        if os.path.isfile(path_parser.full_path):
            stat = path_parser.stat
            if stat is None:
                # Couldn't get stat
                return None
            return (stat.st_size == 0)
        elif os.path.isdir(path_parser.full_path):
            return not bool(os.listdir(path_parser.full_path))
        else:
            return False

class AccessMatcher(Matcher):
    ''' Matches against access type for current user (read, write, execute) '''
    def __init__(self, access_type:int):
        super().__init__()
        self._access_type = access_type

    def _is_match(self, path_parser):
        return os.access(path_parser.full_path, self._access_type)

class GroupMatcher(Matcher):
    ''' Matches against group name or ID '''
    def __init__(self, gid_or_name:Union[int,str]):
        super().__init__()
        # Windows will not support this module
        if not GID_ENABLED:
            raise ModuleNotFoundError('No module named \'grp\' - this OS may not support group matching')
        self._gid = None
        try:
            self._gid = int(gid_or_name)
        except ValueError:
            try:
                self._gid = _group_name_to_id(gid_or_name)
            except KeyError:
                raise ValueError('Could not locate group \'{}\' on system'.format(gid_or_name))

    def _is_match(self, path_parser):
        stat = path_parser.stat
        if stat is None:
            # Couldn't get stat
            return None
        return (stat.st_gid == self._gid)

class UserMatcher(Matcher):
    ''' Matches against user name or ID '''
    def __init__(self, uid_or_name:Union[int,str]):
        super().__init__()
        # Windows will not support this module
        if not UID_ENABLED:
            raise ModuleNotFoundError('No module named \'pwd\' - this OS may not support user matching')
        self._uid = None
        try:
            self._uid = int(uid_or_name)
        except ValueError:
            try:
                self._uid = _user_name_to_id(uid_or_name)
            except KeyError:
                raise ValueError('Could not locate user \'{}\' on system'.format(uid_or_name))

    def _is_match(self, path_parser):
        stat = path_parser.stat
        if stat is None:
            # Couldn't get stat
            return None
        return (stat.st_uid == self._uid)

class PermMatcher(Matcher):
    ''' Matches against octal perm value '''
    def __init__(self, perm:int, logic_operation:LogicOperation=None):
        super().__init__()
        self._perm = perm
        self._logic_operation = logic_operation

    def _is_match(self, path_parser):
        stat = path_parser.stat
        if stat is None:
            # Couldn't get stat
            return None
        perm = (stat.st_mode & 0o777)
        if self._logic_operation is None:
            return (perm == self._perm)
        elif self._logic_operation == LogicOperation.AND:
            # All of perm bits set
            return ((perm & self._perm) == self._perm)
        else:
            # Any of perm bits set
            return ((perm | self._perm) != 0)

class GatedMatcher(Matcher):
    ''' Gates two matchers together using logical AND or OR '''
    def __init__(self, left_matcher:Matcher, right_matcher:Matcher, operation:LogicOperation=LogicOperation.AND):
        super().__init__()
        self.operation = operation
        self.left_matcher = left_matcher
        self.right_matcher = right_matcher

    def _is_match(self, path_parser):
        if self.operation == LogicOperation.AND:
            return (
                self.left_matcher.is_match(path_parser)
                and self.right_matcher.is_match(path_parser)
            )
        else:
            return (
                self.left_matcher.is_match(path_parser)
                or self.right_matcher.is_match(path_parser)
            )

class Finder:
    ''' Finder is capable of walking through paths and execute actions on matching paths '''
    def __init__(self) -> None:
        self._root_dirs = []
        self._min_depth = 0
        self._max_depth = None
        self._matcher = DefaultMatcher()
        self._current_logic = LogicOperation.AND
        self._invert = None
        self._actions = []
        self._verbose = False

    def add_root(self, *root_dirs:Union[str,List[str]]) -> None:
        '''
        Adds one or more roots. Each root will be treated as a glob when executing under Windows.
        '''
        flattened_roots = []
        for root_dir in root_dirs:
            if isinstance(root_dir, list):
                flattened_roots.extend(root_dir)
            else:
                flattened_roots.append(root_dir)

        for root_dir in flattened_roots:
            if _is_windows():
                # Need to manually expand this out
                expanded_dirs = [f for f in glob.glob(root_dir)]
                if not expanded_dirs:
                    print('No match for: {}'.format(root_dir), file=sys.stderr)
                    # Add None as a placeholder to ensure _root_dirs is not empty
                    # (so default is not used in execute())
                    self._root_dirs.append(None)
                else:
                    self._root_dirs.extend(expanded_dirs)
            else:
                # *nix and *nix based systems do this from command line
                self._root_dirs.append(root_dir)

    def set_min_depth(self, min_depth:int) -> None:
        '''
        Sets the global minimum depth limit
        '''
        self._min_depth = min_depth

    def set_max_depth(self, max_depth:int) -> None:
        '''
        Sets the global maximum depth limit
        '''
        self._max_depth = max_depth

    def set_logic(self, logic:LogicOperation) -> bool:
        '''
        Sets the logic gate to be used on subsequent calls to self.append_matcher(). This should
        only be called internal to refind - use set_logic argument to self.append_matcher() instead.
        '''
        self._current_logic = logic
        if isinstance(self._matcher, DefaultMatcher):
            # Nothing is going to be gated on next call
            return False
        return True

    def set_invert(self, invert:bool) -> None:
        '''
        Sets the invert state to be used on subsequent calls to self.append_matcher(). This should
        only be called internal to refind - use Matcher.set_invert() on the matcher object instead.
        '''
        self._invert = invert

    def add_action(self, action:Action) -> None:
        '''
        Adds an action that will be executed on matched paths.
        '''
        self._actions.append(action)

    def set_verbose(self, verbose:bool) -> None:
        '''
        Set verbose output state.
        '''
        # Not yet used locally
        self._verbose = verbose

    def append_matcher(self, matcher:Matcher, set_logic:LogicOperation=None) -> None:
        '''
        Appends a matcher using a logic gate (AND or OR).
        Inputs: matcher - The matcher to append
                set_logic - The logic gate to use when appending this matcher
        '''
        if set_logic is not None:
            self.set_logic(set_logic)

        if self._invert is not None:
            matcher.set_invert(self._invert)

        if isinstance(self._matcher, DefaultMatcher):
            # Only default matcher set - replace with this matcher
            self._matcher = matcher
        elif isinstance(self._matcher, GatedMatcher):
            # Gated matcher already in place
            # Just append it - find command doesn't take precedence into account, even though it may say it does
            self._matcher = GatedMatcher(self._matcher, matcher, self._current_logic)
        else:
            self._matcher = GatedMatcher(self._matcher, matcher, self._current_logic)

        # Reset these settings back to defaults
        self._current_logic = LogicOperation.AND
        self._invert = False

    def set_matcher(self, matcher:Matcher):
        '''
        Clears out the current matcher and sets the given matcher.
        '''
        self._matcher = matcher

    def _handle_path(self, path_parser, actions, match_list):
        if self._matcher.is_match(path_parser):
            for action in actions:
                action.handle(path_parser)
            if match_list is not None:
                match_list.append(path_parser)

    def _is_depth_ok(self, depth):
        return (
            depth >= self._min_depth
            and (self._max_depth is None or depth <= self._max_depth)
        )

    def _is_path_depth_ok(self, root_dir, dir_path):
        path_parser = PathParser(root_dir, (dir_path, ''))
        depth = path_parser.get_rel_depth()
        return self._is_depth_ok(depth)

    def execute(
            self,
            default_root:str=None,
            default_action:Action=None,
            return_list:bool=True
    ) -> Union[List[PathParser],None]:
        '''
        Inputs: default_root:  The default root to use when no root was previously added
                default_action:  The default action to use when no action was previously added.
                return_list:  set to False in order to save on memory when return not needed
        Returns: a list of PathParser when return_list is True or None when return_list is False
        '''
        root_dirs = self._root_dirs
        if not root_dirs and default_root is not None:
            # Default to "."
            root_dirs = [default_root]
        else:
            # Remove None placeholders
            root_dirs = [r for r in root_dirs if r is not None]
        actions = self._actions
        if not actions and default_action is not None:
            # Default to print
            actions = [default_action()]

        # If return_list is set to true, set match_list so it can be filled
        # Otherwise, it will remain None and None will be returned
        match_list = None
        if return_list:
            match_list = []

        for root_dir in root_dirs:
            # Check just the root first
            if self._is_depth_ok(0):
                self._handle_path(PathParser(root_dir), actions, match_list)

            if os.path.isdir(root_dir):
                # Walk through each
                for root, dirs, files in os.walk(root_dir, followlinks=False):
                    dirs.sort()
                    files.sort()
                    if self._is_path_depth_ok(root_dir, root):
                        for entity in dirs + files:
                            self._handle_path(PathParser(root_dir, (root, entity)), actions, match_list)

        return match_list

class Options(Enum):
    ''' Contains all command line option types '''
    DOUBLEDASH = enum.auto()
    HELP = enum.auto()
    NOT = enum.auto()
    AND = enum.auto()
    OR = enum.auto()
    TYPE = enum.auto()
    MAX_DEPTH = enum.auto()
    MIN_DEPTH = enum.auto()
    REGEX_TYPE = enum.auto()
    NAME = enum.auto()
    FULL_PATH = enum.auto()
    REGEX = enum.auto()
    AMIN = enum.auto()
    ANEWER = enum.auto()
    ATIME = enum.auto()
    CMIN = enum.auto()
    CNEWER = enum.auto()
    CTIME = enum.auto()
    EMPTY = enum.auto()
    EXECUTABLE = enum.auto()
    FALSE = enum.auto()
    GID = enum.auto()
    GROUP = enum.auto()
    MMIN = enum.auto()
    NEWER = enum.auto()
    NEWERXY = enum.auto()
    MTIME = enum.auto()
    NOGROUP = enum.auto()
    NOUSER = enum.auto()
    PERM = enum.auto()
    READABLE = enum.auto()
    TRUE = enum.auto()
    UID = enum.auto()
    USER = enum.auto()
    WRITABLE = enum.auto()
    EXEC = enum.auto()
    PYEXEC = enum.auto()
    PRINT = enum.auto()
    FPRINT = enum.auto()
    PRINT0 = enum.auto()
    FPRINT0 = enum.auto()
    PRINTF = enum.auto()
    FPRINTF = enum.auto()
    PYPRINT = enum.auto()
    FPYPRINT = enum.auto()
    PYPRINT0 = enum.auto()
    FPYPRINT0 = enum.auto()
    DELETE = enum.auto()
    VERBOSE = enum.auto()

class FinderArgParser:
    ''' This class parses find arguments into a Finder object '''

    # Converts option string to option type
    OPTION_DICT = {
        '--': Options.DOUBLEDASH,
        '-h': Options.HELP,
        '-help': Options.HELP,
        '--help': Options.HELP,
        '!': Options.NOT,
        '-not': Options.NOT,
        '-a': Options.AND,
        '-and': Options.AND,
        '-o': Options.OR,
        '-or': Options.OR,
        '-type': Options.TYPE,
        '-maxdepth': Options.MAX_DEPTH,
        '-mindepth': Options.MIN_DEPTH,
        '-regextype': Options.REGEX_TYPE,
        '-name': Options.NAME,
        '-wholename': Options.FULL_PATH,
        '-path': Options.FULL_PATH,
        '-regex': Options.REGEX,
        '-amin': Options.AMIN,
        '-anewer': Options.ANEWER,
        '-atime': Options.ATIME,
        '-cmin': Options.CMIN,
        '-cnewer': Options.CNEWER,
        '-ctime': Options.CTIME,
        '-empty': Options.EMPTY,
        '-executable': Options.EXECUTABLE,
        '-false': Options.FALSE,
        '-gid': Options.GID,
        '-group': Options.GROUP,
        '-mmin': Options.MMIN,
        '-newer': Options.NEWER,
        '-neweraa': Options.NEWERXY,
        '-newerac': Options.NEWERXY,
        '-neweram': Options.NEWERXY,
        '-newerat': Options.NEWERXY,
        '-newerca': Options.NEWERXY,
        '-newercB': Options.NEWERXY,
        '-newercm': Options.NEWERXY,
        '-newerct': Options.NEWERXY,
        '-newerma': Options.NEWERXY,
        '-newermB': Options.NEWERXY,
        '-newermm': Options.NEWERXY,
        '-newermt': Options.NEWERXY,
        '-mtime': Options.MTIME,
        '-nogroup': Options.NOGROUP,
        '-nouser': Options.NOGROUP,
        '-perm': Options.PERM,
        '-readable': Options.READABLE,
        '-true': Options.TRUE,
        '-uid': Options.UID,
        '-user': Options.USER,
        '-writable': Options.WRITABLE,
        '-exec': Options.EXEC,
        '-pyexec': Options.PYEXEC,
        '-print': Options.PRINT,
        '-fprint': Options.FPRINT,
        '-print0': Options.PRINT0,
        '-fprint0': Options.FPRINT0,
        '-printf': Options.PRINTF,
        '-fprintf': Options.FPRINTF,
        '-pyprint': Options.PYPRINT,
        '-fpyprint': Options.FPYPRINT,
        '-pyprint0': Options.PYPRINT0,
        '-fpyprint0': Options.FPYPRINT0,
        '-delete': Options.DELETE,
        '-verbose': Options.VERBOSE
    }

    # Converts newerXY character to os.stat attribute name
    XY_CHAR_TO_STAT_NAME = {
        'a': 'st_atime',
        'c': 'st_ctime',
        'm': 'st_mtime'
    }

    def __init__(self):
        self._now = time.time()
        self._arg_idx = 0
        self._opt_idx = 0
        self._current_regex_type = RegexType.SED
        self._current_option_arguments = []
        self._current_option = None
        self._current_option_name = None
        self._current_argument = None

    @staticmethod
    def _print_help():
        print(textwrap.dedent('''
    Partially implements find command entirely in Python.

    Usage: refind [path...] [expression...]

    default path is the current directory (.); default action is -print

    operators
        ! EXPR
        -not EXPR  Inverts the resulting value of the expression
        EXPR EXPR
        EXPR -a EXPR
        EXPR -and EXPR  Logically AND the left and right expressions' result
        EXPR -o EXPR
        EXPR -or EXPR   Logically OR the left and right expressions' result

    normal options
        -help  Shows help and exit
        -maxdepth LEVELS  Sets the maximum directory depth of find (default: inf)
        -mindepth LEVELS  Sets the minimum directory depth of find (default: 0)
        -regextype TYPE  Set the regex type to py, sed, egrep (default: sed)
        --version  Shows version number and exits

    tests
        -name PATTERN  Tests against the name of item using fnmatch
        -regex PATTERN  Tests against the path to the item using re
        -type [dfl]  Tests against item type directory, file, or link
        -path PATTERN
        -wholename PATTERN  Tests against the path to the item using fnmatch
        -amin [+-]N  Last accessed N, greater than +N, or less than -N minutes ago
        -anewer FILE  Last accessed time is more recent than given file
        -atime [+-]N  Last accessed N, greater than +N, or less than -N days ago
        -cmin [+-]N  Change N, greater than +N, or less than -N minutes ago
        -cnewer FILE  Change time is more recent than given file
        -ctime [+-]N  Change N, greater than +N, or less than -N days ago
        -empty  File is 0 bytes or directory empty
        -executable  Matches items which are executable by current user
        -false  Always false
        -gid GID  Matches with group ID
        -group GNAME  Matches with group name or ID
        -mmin [+-]N  Modified N, greater than +N, or less than -N minutes ago
        -newer FILE  Modified time is more recent than given file
        -mtime [+-]N  Modified N, greater than +N, or less than -N days ago
        -newerXY REF  Matches REF X < item Y where X and Y can be:
                      a: Accessed time of item or REF
                      c: Change time of item or REF
                      m: Modified time of item or REF
                      t: REF is timestamp (only valid for X)
        -nogroup  Matches items which aren't assigned to a group
        -nouser  Matches items which aren't assigned to a user
        -perm [-/]PERM  Matches exactly bits in PERM, all in -PERM, any in /PERM
        -readable  Matches items which are readable by current user
        -true  Always true
        -uid UID  Matches with user ID
        -user UNAME  Matches with user name or ID
        -writable  Matches items which are writable by current user

    actions
        -print  Print the matching path
        -fprint FILE  Same as above but write to given FILE instead of stdout
        -print0  Print the matching path without newline
        -fprint0 FILE  Same as above but write to given FILE instead of stdout
        -printf FORMAT  Print using find printf formatting
        -fprintf FILE FORMAT  Same as above but write to given FILE instead of stdout
        -pyprint PYFORMAT  Print using python print() using named args:
                           find_root: the root given to refind
                           root: the directory name this item is in
                           rel_dir: the relative directory name from find_root
                           name: the name of the item
                           full_path: the full path of the item
                           mode_oct: st_mode as octal string
                           perm_oct: only the permissions part of mode_oct
                           perm: the permission in symbolic form
                           type: the type character
                           depth: the directory depth integer of this item
                           group: group name
                           user: user name
                           link: the file that this links to, if any
                           atime: access time as datetime
                           ctime: created time as datetime
                           mtime: modified time as datetime
                           any st args from os.stat()
        -fpyprint FILE PYFORMAT  Same as above but write to given FILE instead of stdout
        -pyprint0 PYFORMAT  Same as pyprint except end is set to empty string
        -fpyprint0 FILE PYFORMAT  Same as above but write to given FILE instead of stdout
        -exec COMMAND ;  Execute the COMMAND where {} in the command is the matching path
        -pyexec PYFORMAT ;  Execute the COMMAND as a pyformat (see pyprint)
        -delete  Deletes every matching path''').strip('\r\n'))

    def _handle_option(self, finder):
        ''' Called when option parsed, returns True iff arg is expected '''
        if self._current_option == Options.HELP:
            self._print_help()
            sys.exit(0)
        elif self._current_option == Options.NOT:
            finder.set_invert(True)
        elif self._current_option == Options.AND:
            if not finder.set_logic(LogicOperation.AND):
                raise ValueError(
                    'invalid expression; you have used a binary operator \'{}\' with nothing before it.'.format(self._current_argument))
        elif self._current_option == Options.OR:
            if not finder.set_logic(LogicOperation.OR):
                raise ValueError(
                    'invalid expression; you have used a binary operator \'{}\' with nothing before it.'.format(self._current_argument))
        elif self._current_option == Options.PRINT:
            finder.add_action(PrintAction())
        elif self._current_option == Options.PRINT0:
            finder.add_action(PrintAction(''))
        elif self._current_option == Options.DELETE:
            finder.add_action(DeleteAction())
        elif self._current_option == Options.EMPTY:
            finder.append_matcher(EmptyMatcher())
        elif self._current_option == Options.EXECUTABLE:
            finder.append_matcher(AccessMatcher(os.X_OK))
        elif self._current_option == Options.READABLE:
            finder.append_matcher(AccessMatcher(os.R_OK))
        elif self._current_option == Options.WRITABLE:
            finder.append_matcher(AccessMatcher(os.W_OK))
        elif self._current_option == Options.FALSE:
            finder.append_matcher(StaticMatcher(False))
        elif self._current_option == Options.TRUE:
            finder.append_matcher(StaticMatcher(True))
        elif self._current_option == Options.NOGROUP:
            finder.append_matcher(GroupMatcher('nogroup'))
        elif self._current_option == Options.NOUSER:
            finder.append_matcher(GroupMatcher('nouser'))
        elif self._current_option == Options.VERBOSE:
            finder.set_verbose(True)
        else:
            # All other options require an argument
            return True
        return False

    @staticmethod
    def _parse_n(n):
        ''' Parses an N argument value '''
        if n.startswith('+'):
            value_comparison = ValueComparison.GREATER_THAN
            n = n[1:]
        elif n.startswith('-'):
            value_comparison = ValueComparison.LESS_THAN
            n = n[1:]
        else:
            value_comparison = ValueComparison.EQUAL_TO
        try:
            value = float(n)
        except ValueError:
            value = None
        return [value_comparison, value]

    @staticmethod
    def _time_to_epoc(t):
        ''' Parses a time string to epoc '''
        epoc = None

        try:
            epoc = float(t)
        except ValueError:
            if t.endswith('Z'):
                is_utc = True
                t = t[:-1]
            else:
                is_utc = False

            time_formats = [
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%dT%H:%M',
                '%Y-%m-%d'
            ]

            date_time = None
            for format in time_formats:
                try:
                    date_time = datetime.strptime(t, format)
                    break
                except ValueError:
                    # continue looping
                    pass

            if date_time is not None:
                if not is_utc:
                    # Adjust for current system time
                    date_time += timedelta(hours=-time.daylight, seconds=time.timezone)
                epoc = (date_time - datetime(1970, 1, 1)).total_seconds()

        return epoc

    def _handle_arg(self, finder:Finder):
        ''' Handle argument, returns True iff parsing is complete for this option '''
        complete = True
        if self._current_option is None or self._current_option == Options.DOUBLEDASH:
            if self._current_argument.startswith('-') and not os.path.isdir(self._current_argument):
                raise ValueError('Unknown predicate: {}'.format(self._current_argument))
            elif self._opt_idx != 0 and self._current_option != Options.DOUBLEDASH:
                raise ValueError('paths must precede expression: {}'.format(self._current_argument))
            else:
                finder.add_root(self._current_argument)
        elif self._current_option == Options.TYPE:
            type_matcher = TypeMatcher(self._current_argument)
            if not type_matcher.type_list:
                raise ValueError('No value given for type option')
            finder.append_matcher(type_matcher)
        elif self._current_option == Options.MAX_DEPTH:
            try:
                max_depth = int(self._current_argument)
            except:
                raise ValueError('Invalid value given to max depth: {}'.format(self._current_argument))
            finder.set_max_depth(max_depth)
        elif self._current_option == Options.MIN_DEPTH:
            try:
                min_depth = int(self._current_argument)
            except:
                raise ValueError('Invalid value given to min depth: {}'.format(self._current_argument))
            finder.set_min_depth(min_depth)
        elif self._current_option == Options.REGEX_TYPE:
            if self._current_argument == 'py':
                self._current_regex_type = RegexType.PY
            elif self._current_argument == 'sed':
                self._current_regex_type = RegexType.SED
            elif self._current_argument == 'egrep':
                self._current_regex_type = RegexType.EGREP
            else:
                raise ValueError(
                    'Unknown regular expression type {}; valid types are py, sed, egrep.'.format(self._current_argument))
        elif self._current_option == Options.NAME:
            finder.append_matcher(NameMatcher(self._current_argument))
        elif self._current_option == Options.FULL_PATH:
            finder.append_matcher(FullPathMatcher(self._current_argument))
        elif self._current_option == Options.REGEX:
            finder.append_matcher(RegexMatcher(self._current_argument, self._current_regex_type))
        elif self._current_option == Options.AMIN or self._current_option == Options.CMIN or self._current_option == Options.MMIN:
            value_comparison, value = __class__._parse_n(self._current_argument)
            if value is None:
                raise ValueError('Invalid argument for -amin ({}); expected numeric'.format(self._current_argument))
            increment = 60.0
            matcher_args = [value_comparison, value * increment, increment, self._now]
            if self._current_option == Options.AMIN:
                matcher_args += ['st_atime']
            elif self._current_option == Options.CMIN:
                matcher_args += ['st_ctime']
            else:
                matcher_args += ['st_mtime']
            finder.append_matcher(StatTimeIncrementMatcher(*matcher_args))
        elif self._current_option == Options.ANEWER or self._current_option == Options.CNEWER or self._current_option == Options.NEWER:
            if os.path.exists(self._current_argument):
                s = os.stat(self._current_argument)
                matcher_args = [ValueComparison.GREATER_THAN, s]
                if self._current_option == Options.ANEWER:
                    matcher_args += ['st_atime']
                elif self._current_option == Options.CNEWER:
                    matcher_args += ['st_ctime']
                else:
                    matcher_args += ['st_mtime']
                finder.append_matcher(StatTimeMatcher(*matcher_args))
            else:
                raise FileNotFoundError('Cannot find path at \'{}\' for -anewer'.format(self._current_argument))
        elif self._current_option == Options.NEWERXY:
            r_stat_name = __class__.XY_CHAR_TO_STAT_NAME.get(self._current_option_name[-1], None)
            if r_stat_name is None:
                # Argument is absolute time
                stat_or_time = __class__._time_to_epoc(self._current_argument)
            elif os.path.exists(self._current_argument):
                stat_or_time = os.stat(self._current_argument)
            else:
                raise FileNotFoundError('Cannot find path at \'{}\' for {}'
                                        .format(self._current_argument, self._current_option_name))
            stat_name = __class__.XY_CHAR_TO_STAT_NAME.get(self._current_option_name[-2], 'st_mtime')
            finder.append_matcher(StatTimeMatcher(ValueComparison.GREATER_THAN, stat_or_time, stat_name, r_stat_name))
        elif self._current_option == Options.ATIME or self._current_option == Options.CTIME or self._current_option == Options.MTIME:
            value_comparison, value = __class__._parse_n(self._current_argument)
            if value is None:
                raise ValueError('Invalid argument for -time ({}); expected numeric'.format(self._current_argument))
            increment = 24.0 * 60.0 * 60.0
            matcher_args = [value_comparison, value * increment, increment, self._now]
            if self._current_option == Options.ATIME:
                matcher_args += ['st_atime']
            elif self._current_option == Options.CTIME:
                matcher_args += ['st_ctime']
            else:
                matcher_args += ['st_mtime']
            finder.append_matcher(StatTimeIncrementMatcher(*matcher_args))
        elif self._current_option == Options.GID:
            try:
                gid = int(self._current_argument)
            except ValueError:
                raise ValueError('Invalid argument for -gid ({}); expected numeric'.format(self._current_argument))
            finder.append_matcher(GroupMatcher(gid))
        elif self._current_option == Options.GROUP:
            finder.append_matcher(GroupMatcher(self._current_argument))
        elif self._current_option == Options.UID:
            try:
                uid = int(self._current_argument)
            except ValueError:
                raise ValueError('Invalid argument for -uid ({}); expected numeric'.format(self._current_argument))
            finder.append_matcher(UserMatcher(uid))
        elif self._current_option == Options.USER:
            finder.append_matcher(UserMatcher(self._current_argument))
        elif self._current_option == Options.PERM:
            logic = None
            perm = self._current_argument
            if perm.startswith('-'):
                logic = LogicOperation.AND
                perm = perm[1:]
            elif perm.startswith('/'):
                logic = LogicOperation.OR
                perm = perm[1:]
            try:
                perm = int(perm, base=8)
            except ValueError:
                raise ValueError('Invalid argument for -perm ({}); expected numeric'.format(self._current_argument))
            finder.append_matcher(PermMatcher(perm, logic))
        elif self._current_option == Options.EXEC or self._current_option == Options.PYEXEC:
            if self._current_argument != ';':
                complete = False # Continue parsing until ;
            else:
                if self._current_option == Options.EXEC:
                    finder.add_action(ExecuteAction(self._current_option_arguments[:-1]))
                else:
                    finder.add_action(PyExecuteAction(self._current_option_arguments[:-1]))
        elif self._current_option == Options.FPRINT:
            fp = SharedFileWriter(self._current_argument, binary=False)
            finder.add_action(PrintAction(file=fp))
        elif self._current_option == Options.FPRINT0:
            fp = SharedFileWriter(self._current_argument, binary=False)
            finder.add_action(PrintAction(end='', file=fp))
        elif self._current_option == Options.PRINTF:
            finder.add_action(PrintfAction(self._current_argument, ''))
        elif self._current_option == Options.FPRINTF:
            if len(self._current_option_arguments) >= 2:
                fp = SharedFileWriter(self._current_option_arguments[0], binary=False)
                finder.add_action(PrintfAction(self._current_argument, end='', file=fp))
            else:
                # Keep waiting for more arguments
                complete = False
        elif self._current_option == Options.PYPRINT:
            finder.add_action(PyPrintAction(self._current_argument))
        elif self._current_option == Options.FPYPRINT:
            if len(self._current_option_arguments) >= 2:
                fp = SharedFileWriter(self._current_option_arguments[0], binary=False)
                finder.add_action(PyPrintAction(self._current_argument, file=fp))
            else:
                # Keep waiting for more arguments
                complete = False
        elif self._current_option == Options.PYPRINT0:
            finder.add_action(PyPrintAction(self._current_argument, ''))
        elif self._current_option == Options.FPYPRINT0:
            if len(self._current_option_arguments) >= 2:
                fp = SharedFileWriter(self._current_option_arguments[0], binary=False)
                finder.add_action(PyPrintAction(self._current_argument, end='', file=fp))
            else:
                # Keep waiting for more arguments
                complete = False
        return complete

    def parse(self, cliargs, finder):
        ''' Parse the cliargs list into the finder '''
        if '--version' in cliargs:
            print('{} {}'.format(PACKAGE_NAME, __version__))
            sys.exit(0)
        # argparse is too complex to handle simple commands that find processes
        for arg in cliargs:
            self._current_argument = arg
            opt = __class__.OPTION_DICT.get(arg, None)
            if opt is None or self._current_option is not None:
                # This is an argument to an option
                self._current_option_arguments += [self._current_argument]
                if self._handle_arg(finder):
                    self._current_option = None
                    self._current_option_name = None
                    self._current_option_arguments = []
            else:
                self._opt_idx += 1
                self._current_option = opt
                self._current_option_name = arg
                if not self._handle_option(finder):
                    self._current_option = None
                    self._current_option_name = None
            self._arg_idx += 1

        if self._current_option is not None:
            if self._current_option == Options.EXEC or self._current_option == Options.PYEXEC:
                raise ValueError('arguments to option -exec and -pyexec must end with ;')
            else:
                raise ValueError(f'missing arguments to option {self._current_option_name}')
        return True

def main(cliargs):
    arg_parser = FinderArgParser()
    finder = Finder()
    if arg_parser.parse(cliargs, finder):
        finder.execute(default_root='.', default_action=PrintAction, return_list=False)
        return 0
    else:
        print('Failed to parse arguments', file=sys.stderr)
        return 1
