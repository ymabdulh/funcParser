'''
    contians helper functions for the main script
'''
import os, re


'''
    Given a file object 'file', this function reads each line
    parsing out each function definition and storing it in a list
    'funcs' that's returned by the function
'''
def getFuncsList(file):
    funcs = []
    keywords = '(and|if|while)'

    for line in file:
        # make sure we don't match if statements
        match = re.match('\\s*'+keywords+'\\s*\\(', line)
        if match:
            continue

        '''
            search for the function signature

            REGEX                       DESCRIPTION                         EXAMPLE
            ------------------------------------------------------------------------
            \s*                         any number of spaces
            [a-zA-Z0-9_:]+              return type                         int
            \*?                         optional (non spaced) pointer          *
            \s+                         one or more spaces
            [a-zA-Z0-9_*:\s]*           function name                            hello
            \(                          opening parenthesis                            (
            (                           start of group
                [a-zA-Z0-9_,.*\s]           function arguments                          int i
                (=(?!=))?                   default arguments (but not ==)                    =
                (-(?=>))?                   dereference ->                                      num->val
            )*                          one or more of group
            \)(?!\s*;)                  close parenthesis not followed by ;                             )
        '''
        match = re.match('\\s*[a-zA-Z0-9_:]+\\*?\\s+[a-zA-Z0-9_*:\\s]*\\(([a-zA-Z0-9_,.*:\\s](=(?!=))?(-(?=>))?)*\\)(?!\\s*;)', line)
        if match:
            funcs.append(match.group().strip())

    return funcs


'''
    function to parse the config file if one is provided
    otherwise returns default config settings
'''
def get_config(options):
    # find path and levels
    if options['configFile'] is True:
        with open('config.txt', 'r') as config_file:
            path = config_file.readline().strip() # contains directory path
            depth = config_file.readline() # contains depth to read into

            if not depth.isdigit() or depth == '\n' or depth == '':
                depth = 0
            else:
                depth = int(depth)
    else:
        path = os.getcwd() + '/cppfiles'
        depth = 0

    path = os.path.normpath(path)

    return {
        'path' : path,
        'depth' : depth
    }


'''
    function to get the list of file paths to scan through
'''
def get_file_list(path, depth):

    # get file list
    res = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        res += [os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.cpp') or filename.endswith('.cc')]

        current_depth = dirpath[len(path) + len(os.path.sep):].count(os.path.sep)
        if current_depth >= depth:
            dirnames[:] = [] # Don't recurse any deeper

    return res
    

'''
    function to get the command line arguments
'''
def get_args(argv):
    allowed_opts = {
        'c' : 'configFile',
        'd' : 'details',
        't' : 'terminalOutput'
    }
    options = {
        'configFile' : False,
        'details' : False,
        'terminalOutput' : False
    }

    if len(argv) > 1:
        for c in argv[1]:
            if c in allowed_opts:
                key = allowed_opts[c]
                options[key] = True
            else:
                print 'unrecognized argument', c

    return options
