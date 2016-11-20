import os, sys, re
from function_tracker import FunctionTracker

'''
    Script to detect function signatures from a *.cpp or *.cc file.
    
    Usage:
    - To use, place files in the same directory as the script and run.
    - A function's entire signature (return type, name, parameters, and open/close parenthesis)
      must be on the same line for this script to detect it.

    Behavior:
    - This script works on member functions (className::funcName) as well as global functions.
    - It does not, however, detect constructors or destructors (because they don't have a return type).
    - Extracts all lines that look like a function, but doesn't check them for correctness.
      For example, "ad afaf(iia.da,adda)" will be detected even if none are known types.
    - Extracts functions from comments
    - Ignores keywords even if they look like functions.
      For example: "else if(true)" won't be included as function because of the presence of "if".
      Currently ignored keywords are: if, else, while.

    The script is not guaranteed to catch all function definitions,
    and may mistakenly include non-functions. Read over the output to be sure.
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
            [a-zA-Z0-9_*:]+             return type                         int
            \s+                         one or more spaces
            [a-zA-Z0-9_*:\s]*           function name                           * hello
            \(                          opening parenthesis                            (
            (                           start of group
                [a-zA-Z0-9_,.*\s]           function arguments                          int i
                (=(?!=))?                   default arguments (but not ==)                    =
                (-(?=>))?                   dereference ->                                      num->val
            )*                          one or more of group
            \)(?!\s*;)                  close parenthesis not followed by ;                             )
        '''
        match = re.match('\\s*[a-zA-Z0-9_*:]+\\s+[a-zA-Z0-9_*:\\s]*\\(([a-zA-Z0-9_,.*:\\s](=(?!=))?(-(?=>))?)*\\)(?!\\s*;)', line)
        if match:
            funcs.append(match.group().strip())

    return funcs

def get_file_list():
    # find path and levels
    if len(sys.argv) > 1 and sys.argv[1] == 'c':
        with open('config.txt', 'r') as config_file:
            path = config_file.readline().strip() # contains directory path
            depth = config_file.readline() # contains depth to read into

            if not depth.isdigit() or depth == '\n' or depth == '':
                depth = 0
            else:
                depth = int(depth)
    else:
        path = os.getcwd()
        depth = 0

    path = os.path.normpath(path)

    # get file list
    res = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        res += [os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.cpp') or filename.endswith('.cc')]

        current_depth = dirpath[len(path) + len(os.path.sep):].count(os.path.sep)
        if current_depth >= depth:
            dirnames[:] = [] # Don't recurse any deeper

    return res
    

def main():

    ft = FunctionTracker()

    print
    
    # parse functions from files
    for filepath in get_file_list():
        filename = filepath.split(os.path.sep)[-1]

        print 'Reading function signatures from: ' + filename

        # open file and get functions
        with open(filepath) as f:
            funcs = getFuncsList(f) 
            ft.add_file(funcs, filename)

        # print functions
        for item in funcs:
            print '    ' + item

        # message if none found
        if not len(funcs):
            print '    ' + 'no function definitions found'

        print


    # write results to file
    dup_funcs = ft.get_duplicate_funcs() # sorted by most duplicate first
    
    with open('results.txt', 'w') as resFile:
        resFile.write('Total number of files read: ' + str(len(ft.get_files())) + '\n')
        resFile.write('Total number of function definitions found: ' + str(len(ft.get_funcs())) + '\n')
        resFile.write('Number of functions defined multiple times: ' + str(len(dup_funcs)) + '\n')
        resFile.write('\n')
        resFile.write('Below is a sorted list of functions defined multiple times.\n')
        resFile.write('The ones with most duplicates appear first.\n')
        resFile.write('\n')

        for func in dup_funcs:
            resFile.write(func + '\t' + str(ft.get_num_duplicated(func)) + '\n')


if __name__ == '__main__':
    main()

