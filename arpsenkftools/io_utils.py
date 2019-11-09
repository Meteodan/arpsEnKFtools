"""
Some utility functions
"""

import imp


def import_all_from(module_path):
    """
    Modified from
    http://grokbase.com/t/python/python-list/1172ahxp0s/from-module-import-using-import
    Loads python file at "module_path" as module and adds contents to global namespace.
    """
    mod = imp.load_source('mod', module_path)
    return mod
