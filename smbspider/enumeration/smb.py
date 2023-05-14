"""
Functions used for fetching meta and content from samba servers.
External binaries used in conjunction here is smbclient and smbmap
"""

import datetime
import time
import os
import subprocess 

from enumeration import core

"""
Fetch shares from samba server using smbclient
Only anonymous logins work in a null session at this point 
"""
def get_shares(targets):

    shares = {}
    for target in targets:

        # run the smbclient cmd and traverse the greppable output
        command = f"smbclient -N -L \\\\{target} -g"
        
        result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        shares[target] = []
        
        if '|' in result.stdout: # | is the greppable value marker 
            for line in result.stdout.split("\n"):
                if '|' not in line: 
                    continue

                share_type, share_name, share_description = line.split('|')

                shares[target].append({ "type": share_type, "name": share_name, "description": share_description })

    return shares

"""
Fetch meta on files from sambashares
Can be narrowed down to files on a single share and filters can also be applied for bytesize, moddate and more
"""
def get_files(all_shares, filter_by_share=None, filter=None):
    files = {}

    for target in all_shares:

        files[target] = {}
        for share in all_shares[target]:

            if filter_by_share != None and share['name'] != filter_by_share:
                continue
            
            files[target][share['name']] = []
            
            command = f"/usr/bin/smbmap -g -H {target} -R '{share['name']}'"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            # smbmap v2 has a way of deprecating the \r loader "Working on it", but 1.8 does not which we are basing this script on.
            # therefore some manual code to remove the smbmap loading msg
            # see "--no-update" flag in latest release here https://github.com/ShawnDEvans/smbmap
            for line in result.stdout.split("\n"):
                if "Working on it" in line:
                    continue 

                if line.strip() == '':
                    continue 

                filehost, fileprivs, filetype, filename, filesize, date = line.split(', ')

                # interpret the smbmap filetype
                filetype = filetype.split(":")[1].upper()
                if filetype == 'D':
                    filetype = 'DIR'
                else:
                    filetype = 'FILE'

                # convert the smbmap file modified time format to unixtime
                # ex. Thu May 11 23:02:23 2023
                date = date.replace("date:", "") # remove smbmap formatting :

                date_complex = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S %Y") # shoutouts to chatgpt

                timestamp = int(date_complex.timestamp())
                
                file = {
                    'host': filehost.split(":")[1],
                    'priv': fileprivs.split(":")[1],
                    'type': filetype,
                    'name': filename.split(":")[1],
                    'size': int(filesize.split(":")[1]),
                    'time': timestamp,
                    'date': str(date_complex)
                }

                # apply search filters here
                # todo: expand filename and dir search with regex options if time allows it
                if filter:
                    
                    # minimum byte filter
                    if filter['min']: 
                        if file['size'] < filter['min']:
                            continue
                    
                    # maximum byte filter
                    if filter['max']:
                        if file['size'] > filter['max']:
                            continue

                    # minimum mod time filter
                    if filter['mod_min']:
                        mod_min_complex = datetime.datetime.strptime(filter['mod_min'], "%Y-%m-%d %H:%M:%S")
                        filter_timestamp = int(time.mktime(mod_min_complex.timetuple()))

                        if file['time'] < filter_timestamp:
                            continue
                
                    # maximum mod time filter
                    if filter['mod_max']:
                        mod_max_complex = datetime.datetime.strptime(filter['mod_max'], "%Y-%m-%d %H:%M:%S")
                        filter_timestamp = int(time.mktime(mod_max_complex.timetuple()))

                        if file['time'] > filter_timestamp:
                            continue

                    # filename filter, containing search
                    if filter['name']:
                        if filter['name'] not in file['name']:
                            continue 

                    # directory filter, containing search throughout the samba share path
                    if filter['dir']:
                        if file['type'] == 'FILE':
                            
                            # split the filename into parts, removing first entry (sharename) and last entry (filename)
                            # leaving us with only the directory path structure to search in
                            path = file['name'].split('\\')
                            path.pop() # last
                            path.pop(0) # first

                            match = False

                            if len(path) > 0:
                                for directory in path:
                                    if filter['dir'] in directory:
                                        match = True 
                            
                            if match != True:
                                continue

                files[target][share['name']].append(file)
    
    return files

"""
Downloads content from a sambashare to a local folder structure matching the share
Target structure is: [output_dir]/[target]/[share]/path/to/file/on/share.ext

Having a folder structure we can rely on here gives us an easy way of avoiding double downloads.
"""
def download(basedir, files):
    for target in files:
        for share in files[target]:

            core.message(f"Downloading files from \\\\{target}\\{share}", False)

            for file in files[target][share]:
                if file['type'] == 'DIR': continue
                
                # flip smb/nix path separator from \ to /
                file_to_download = file['name'].replace('\\', '/')

                # split path and pop the file basename
                path_struct = file_to_download.split('/')
                basename = path_struct.pop()
                
                target_dir = basedir + '/' + target + '/'
                target_dir = target_dir + '/'.join(path_struct)

                target_file = target_dir + '/' + basename 

                # mkdir -p equiv.
                os.makedirs(target_dir, exist_ok=True)

                # download file from anon smb
                # todo: consider login? out of scope for this deadline sunday though
                #print(target_file)
                if os.path.exists(target_file):
                    core.message(f"Skipping file, already exists: {file_to_download}", False, True, True)
                else:
                    command = f"echo '' | smbget -U '' 'smb://{target}/{file_to_download}' -o '{target_file}'"
                    result = subprocess.run(command, capture_output=True, text=True, shell=True)

                    # todo: we really need some error checking here
                    # stuff could go wrong with smb perms
                    # deadline.. out of scope for now.

                    core.message(f"Downloading {file_to_download} ({file['size']} bytes, {file['date']})", False, True, True)
