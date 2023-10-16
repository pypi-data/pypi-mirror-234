<h1>inspect-dense by <a href="https://aimodels.org">AI Models</a></h1>

inspect-dense is a Python package for recursively describing all python files in a directory. 
Provides a simple way to get a high-level overview of a project's codebase in a conscise format to minimize tokens used when developing code with AI systems.


Installation
------------

You can install inspect-dense using pip:

Copy code

`pip install inspect-dense`

Usage
-----

To use inspect-dense, simply import the `describe_directory` function from the package and pass it the directory path you want to describe:

python code
```python
from inspect-dense import describe_directory  

directory = "/path/to/directory" 
output = describe_directory(directory)
```

The `describe_directory` function returns a dictionary with the following structure:

```json
{     "/path/to/file.py": {         "functions": {             "function_name(args)": "Function docstring"         },         "classes": {             "Class1": {                 "methods": {                     "method1(args)": "Method docstring",                     "method2(args)": "Method docstring"                 }             },             "Class2": {                 "methods": {                     "method3(args)": "Method docstring",                     "method4(args)": "Method docstring"                 }             }         }     } }
```
Command Line Interface
----------------------

inspect-dense also comes with a command line interface. You can use it to describe a directory and output the results to a file:

`inspect-dense <directory> [--no-gitignore]`

For example:

`inspect-dense /path/to/directory --no-gitignore`

This will output the results.

License
-------

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.
