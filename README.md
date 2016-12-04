# funcParser
Script to detect function signatures from a *.cpp or *.cc file.
    
##Usage:
- To use, place files in the same directory as the script and run.
- A function's entire signature (return type, name, parameters, and open/close parenthesis)
  must be on the same line for this script to detect it.

##Behavior:
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