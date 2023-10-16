# refind

A find clone in Python with both CLI and library interfaces

## Shameless Promotion

Check out my other Python clone tools:
- [greplica](https://pypi.org/project/greplica/)
- [sedeuce](https://pypi.org/project/sedeuce/)

## Known Differences with find

- The Python module `re` is internally used for all regular expressions. The inputted regular
    expression is modified only when `sed` is selected as the regextype (default) in order to
    reverse meaning of escaped characters `+?|{}()`
- Parenthesis around expressions are not supported
- printf action differences
    - Birth time (B) is just treated the same as creation time (C)
    - %b, %k, %S, and %Y are not supported
    - Some formatting specifier inconsistencies may be encountered
- Not all options, tests, and actions are available (see help)
- pyprint actions are provided which uses Python string formatting

## Contribution

Feel free to open a bug report or make a merge request on [github](https://github.com/Tails86/refind/issues).

## Installation

This project is uploaded to PyPI at https://pypi.org/project/refind/

To install, ensure you are connected to the internet and execute: `python3 -m pip install refind --upgrade`

Once installed, there will be a script called `refind` under Python's script directory. Ensure Python's
scripts directory is under the environment variable `PATH` in order to be able to execute the script
properly from command line.

## CLI Help
```
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
    -delete  Deletes every matching path
```

## Library Help

refind can be used as a library from another module. The following is a simple example.
```py
    import refind
    from io import StringIO

    finder = refind.Finder()
    finder.set_min_depth(1)
    finder.add_root('.')
    finder.append_matcher(refind.TypeMatcher(FindType.FILE, FindType.DIRECTORY))
    output_stream = StringIO()
    finder.add_action(refind.PyPrintAction('{perm} {name}', file=output_stream))
    matches = finder.execute()

    # Prints the string that contains the result of all actions performed
    print(output_stream.getvalue(), end='')

    # Prints the contents of matches
    for match in matches:
        print(f'{match.find_root}, {match.root}, {match.rel_dir}, {match.name}, {match.full_path}')
```

The following Finder functions may be used to setup Finder.
```py
def add_root(self, *root_dirs:Union[str,List[str]]) -> None:
    '''
    Adds one or more roots. Each root will be treated as a glob when executing under Windows.
    '''

def set_min_depth(self, min_depth:int) -> None:
    '''
    Sets the global minimum depth limit
    '''

def set_max_depth(self, max_depth:int) -> None:
    '''
    Sets the global maximum depth limit
    '''

def add_action(self, action:Action) -> None:
    '''
    Adds an action that will be executed on matched paths.
    '''

def append_matcher(self, matcher:refind.Matcher, set_logic:refind.LogicOperation=None) -> None:
    '''
    Appends a matcher using a logic gate (AND or OR).
    Inputs: matcher - The matcher to append
            set_logic - The logic gate to use when appending this matcher
    '''

def set_matcher(self, matcher:refind.Matcher):
    '''
    Clears out the current matcher and sets the given matcher.
    '''
```

The following Actions are provided by refind.
```py
# Simply prints the full path of the item
PrintAction(end:str=None, file:io.IOBase=None, flush:bool=False)

# Prints the item using python format string
PyPrintAction(format:str, end:str=None, file:io.IOBase=None, flush:bool=False)

# Prints the item using printf format string
PrintfAction(format:str, end:str=None, file:io.IOBase=None, flush:bool=False)

# Executes custom command where {} is the full path to the item
ExecuteAction(command:List[str])

# Executes custom command where each element in the command is a format string
PyExecuteAction(command:List[str])

# Deletes the matched item
DeleteAction()
```

The following Matchers are provided by refind. Use set_invert() function after creating the
matcher if inverting the result is desired.
```py
# Statically return True or False for every item
StaticMatcher(value:bool)

# The default matcher when none specified (same as StaticMatcher(True))
DefaultMatcher()

# Matches against the name of the item
NameMatcher(pattern:str)

# Matches against the full path of the item
FullPathMatcher(pattern:str)

# Matches against the full path of the item using regex
RegexMatcher(pattern:str, regex_type:refind.RegexType)

# Matches against the item's type
TypeMatcher(*types:Union[refind.FindType,str,List[refind.FindType],List[str]])

# Matches against os.stat time relative to current time
StatTimeIncrementMatcher(
    value_comparison:refind.ValueComparison,
    rel_s:float,
    increment_s:float,
    current_time_s:float,
    stat_name:str
)

# Matches against os.stat time to an absolute time
StatTimeMatcher(
    value_comparison:refind.ValueComparison,
    stat_or_time:Union[os.stat_result,float],
    stat_name:str,
    r_stat_name:str=None
)

# Matches when directory empty or file size is 0 bytes
EmptyMatcher()

# Matches against access type for current user (read, write, execute)
AccessMatcher(access_type:int)

# Matches against group name or ID
GroupMatcher(gid_or_name:Union[int,str])

# Matches against user name or ID
UserMatcher(uid_or_name:Union[int,str])

# Matches against octal perm value
PermMatcher(perm:int, logic_operation:refind.LogicOperation=None)

# Gates two matchers together using logical AND or OR
GatedMatcher(
    left_matcher:refind.Matcher,
    right_matcher:refind.Matcher,
    operation:refind.LogicOperation=LogicOperation.AND
)
```

The Finder.execute() function should then be called once all options, actions, and matchers are
set on the Finder object.
```py
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
```