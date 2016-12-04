# funcParser
Script to detect function signatures from a C++ projects with files ending in `.cpp` or `.cc`.
    
## Usage:
- To use, place files in the cppfile directory and run `python cpp_func_parser.py`
- Command line arguments:
  `python cpp_func_parser.py [arguments]`

  Arguments can be any of:
	- `c`: use a config file `config.txt`. Use to specify a path containing your cpp project and the depth (number of directory levels to include) in the scan. Check `config_template.txt` to get started.
	- `d`: show details in the output file `results.txt` specifying the files each duplicated function was found in.
	- `t`: show each function as its found in the terminal (doesn't affect `results.txt` output).

  An example that runs with all arguments: `python cpp_func_parser.py cdt`


## Behavior:
- This script works on member functions (className::funcName) as well as global functions.
- It does not, however, detect constructors or destructors (because they don't have a return type).
- A function's entire signature (return type, name, parameters, and open/close parenthesis)
  must be on the same line for this script to detect it.
- Extracts all lines that look like a function, but doesn't check them for correctness.
  For example, "ad afaf(iia.da,adda)" will be detected even if none are known types.
- Extracts functions from comments
- Ignores keywords even if they look like functions.
  For example: "else if(true)" won't be included as function because of the presence of "if".
  Currently ignored keywords are: if, else, while.


###### Keep in mind that this script is not guaranteed to catch all function definitions, and may mistakenly include non-functions. Read over the output to be sure.
