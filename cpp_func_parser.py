import os, re

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
    prototypes = []
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
            [a-zA-Z0-9_*]+              return type                         int
            \s+                         one or more spaces
            [a-zA-Z0-9_*:\s]*           function name                           * hello
            \(                          opening parenthesis                            (
            (                           start of group
                [a-zA-Z0-9_,.*\s]           function arguments                          int i
                (=(?!=))?                   default arguments (but not ==)                    =
                (-(?=>))?                   dereference ->                                      num->val
            )*                          one or more of group
            \)                          close parenthesis                                               )
        '''
        match = re.match('\\s*[a-zA-Z0-9_*]+\\s+[a-zA-Z0-9_*:\\s]*\\(([a-zA-Z0-9_,.*:\\s](=(?!=))?(-(?=>))?)*\\)', line)
        if match:
            prototypes.append(match.group())

    return prototypes

def main():

    path = os.getcwd()+'/'

    print
    
    for filename in os.listdir(path):
        # only check cpp and cc files
        if not filename.endswith('.cpp') and not filename.endswith('.cc'):
            continue

        print 'Reading function signatures from: ' + filename

        # open file and get functions
        with open(path+filename) as file:
            funcs = getFuncsList(file)

        # print functions
        for item in funcs:
            print '    ' + item

        # message if none found
        if not len(funcs):
            print '    ' + 'no function prototypes found'

        print

if __name__ == '__main__':
    main()

