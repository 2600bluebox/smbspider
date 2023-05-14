"""
Functions used for displaying the metadata in console
"""

import os

from enumeration import core

"""
Lists shares in a formatted table
"""
def shares(shares):
    for target in shares:
        core.message(f"Listing shares on \\\\{target} ({str(len(shares[target]))} found)", False)

        for share in shares[target]:
            core.message(f"{share['name']}", False, True, True)
    
    core.message("", False, True, False)

"""
Lists files in a formatted table
"""
def files(files):

    for target in files:
        for share in files[target]:
            
            core.message(f"Listing files on \\\\{target}\\{share} ", False)

            for file in files[target][share]:
                if file['type'] == 'DIR': continue

                core.message(f"[{file['type']}] {file['name']} ({file['size']} bytes, {file['date']})", False, True, True)
    
    core.message("", False, True, False)
