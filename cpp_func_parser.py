import os, sys
from modules.function_tracker import FunctionTracker
from modules.helpers import *

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

def main():

    options = get_args(sys.argv)
    ft = FunctionTracker()
    
    # parse functions from files
    for filepath in get_file_list(options):

        filename = filepath.split(os.path.sep)[-1]

        # open file and get functions
        with open(filepath) as f:
            funcs = getFuncsList(f) 
            ft.add_file(funcs, filename)

        # print progress information if specified
        if options['terminalOutput'] is True:

            print

            print 'Reading function signatures from: ' + filename

            if not len(funcs):
                # message if none found
                print '    ' + 'no function definitions found'
            else:
                # print functions
                for item in funcs:
                    print '    ' + item


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
            if options['details'] is True:
                # if enabled, write the filenames that contain this function
                for filename in ft.get_files(func):
                    resFile.write('    - ' + filename + '\n')
                resFile.write('\n')


if __name__ == '__main__':
    main()

