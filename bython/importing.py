import sys
import os

import bython.parser
import bython.logger


"""
Module for handling imports of Bython files in Python code.
"""


def bython_import(module_name, globals, logger=None):
    """
    Import Bython files in Python code. Example:
    
    ``` python
    from bython.importing import bython_import
    bython_import("test_module", globals())

    # Now, 'test_module' is available like any other module:
    test_module.func()
    ```
    
    Args:
        module_name (str):              Name of module to import.
        globals (dict):                 Global namespace (use globals() to get 
                                        this).
        logger (bython.logger.Logger)   Optional. Logger object. Mainly used for
                                        debugging.

    Raises:
        ImportError: If no bython file for module is found, or bython file could
        not be parsed. 
    """
    if logger is None:
        logger = bython.logger.Logger()

    logger.log_info("Looking for %s.by" % module_name)
    path = _locate_module(module_name, logger)

    logger.log_info("Parsing %s" % path)
    try:
        bython.parser.parse_file_recursively(path, False, os.path.join(sys.path[0], "python_"))

        error_during_parsing = None

    except Exception as e:
        error_during_parsing = e

    if error_during_parsing is not None:
        raise ImportError("Error while parsing '%s': %s" % (path, str(e)))

    python_file_path = os.path.join(
        sys.path[0], 
        "python_" + bython.parser._change_file_name(module_name, None)
    )

    logger.log_info("Importing %s" % python_file_path)

    # Hacky way of doing global imports of general modules inside a function
    exec("global %s" % module_name, globals)
    exec("import python_%s as %s" % (module_name, module_name), globals)

    # Cleanup
    logger.log_info("Removing %s" % python_file_path)
    os.remove(python_file_path)


def _locate_module(module_name, logger):
    """
    Locate the bython file for a given module name.

    Args:
        module_name (str):              Module to look for.
        logger (bython.logger.Logger)   Optional. Logger object. Mainly used for
                                        debugging.

    Returns:
        str: Full path of bython file associated with module. 
    
    Raises:
        ImportError: If module is not found.
    """
    for path in sys.path:
        logger.log_info("Searching in %s" % path)

        module_path = _traverse_and_find(module_name, path) 

        if module_path is not None:
            logger.log_info("Module found at %s" % module_path)
            break

    if module_path is None:
        raise ImportError("Could not find any bython file for %s" % module_name)

    return module_path


def _traverse_and_find(module_name, directory):
    """
    Traverse a directory (recursively), and look for a file named 
    'module_name'.by.

    Args:
        module_name (str):              Module to look for.
        directory (str):                Path to directory to traverse.

    Returns:
        str: Full path of bython file associated with module, None if no such
        file is found.
    """
    for rootpath, subdirs, files in os.walk(directory):
        for file in files:
            if file == (module_name+".by"):
                return os.path.join(rootpath, file)

    return None

