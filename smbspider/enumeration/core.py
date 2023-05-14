"""
Functions used for running smbspider
"""

import os

indent_marker = '\033[94m[\033[0m+\033[94m]\033[0m '
indent_marker_value = '  \033[92m[\033[0m=\033[92m]\033[0m '
directory = ''

"""
Resolves targets to a string list
input here can be both a file and a single host string
"""
def targets(host):
    targets = []

    if os.path.exists(host):
        with open(host, 'r') as file:
            targets = file.read().splitlines()
    else:
        targets.append(host)

    return targets

"""
Function used for having a unified way of displaying console output
This allows for some color formatting and setting up output in a somewhat neat structure
"""
def message(message, skip_newline=False, skip_indent=False, value_indent=False):

    indent = indent_marker 
    if skip_indent == True:
        indent = ''

    if value_indent == True:
        indent = indent_marker_value

    if skip_newline == True:
        print(f"{indent}{message}", end="")
    else:
        print(f"{indent}{message}")
