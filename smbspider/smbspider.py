# smbspider.py
# crawl a single or multiple hosts for smb shares, files and directories
# blueb0x

import click
import os
import sys
import time

assert (sys.version_info[0] == 3), "Python version must be 3"

from enumeration import core 
from enumeration import display
from enumeration import network
from enumeration import smb

@click.command()
@click.option('--host', '-h', help='Target host or file containing multiple', prompt='IP/Hostname', required=True)
@click.option('--list-shares', '-l', help='Lists shares', is_flag=True, default=False, required=False, show_default=True)
@click.option('--list-files', '-f', help='Lists files on shares. --share to narrow down', is_flag=True, default=False, required=False, show_default=True)
@click.option('--filter-size-min', '-smin', help='Filter by minimum size in bytes', required=False, type=int)
@click.option('--filter-size-max', '-smax', help='Filter by maximum size in bytes', required=False, type=int)
@click.option('--filter-mod-min', '-mmin', help='Filter by minimum date (yyyy-mm-dd hh:ii:ss)', required=False)
@click.option('--filter-mod-max', '-mmax', help='Filter by maximum date (yyyy-mm-dd hh:ii:ss)', required=False)
@click.option('--filter-filename', '-name', help='Filter by filename, ex. id_rsa', required=False)
@click.option('--filter-dir', '-fdir', help='Filter by holding directory name, ex. .ssh', required=False)
@click.option('--share', '-s', help='The Samba share, optional', required=False)
@click.option('--directory', '-d', help='Downloads listed content to this directory', required=False)
@click.option('--ping', '-p', help='ICMP Ping and retrieve ttl and avg. ms.', is_flag=True, default=False, required=False, show_default=True)
@click.option('--quiet', '-q', help='Hide the banner', is_flag=True, default=False, required=False, show_default=True)
def main(host, list_shares, list_files, filter_size_min, filter_size_max, filter_mod_min, filter_mod_max, filter_filename, filter_dir, share, directory, ping, quiet):
    
    try:
        
        # show the ascii banner
        banner() if quiet == False else None
        
        # resolve targets
        targets = core.targets(host)
        
        # verify output directory if supplied
        if directory:
            if os.path.exists(directory) != True:
                raise Exception("Download directory was supplied, but does not exist.")
        
        # ping target
        if ping == True:
            network.ping(targets)

        # fetch shares and files using smbclient and smbmap in conjunction
        shares = smb.get_shares(targets)

        filter = { 
            'min': filter_size_min, # bytesize minimum
            'max': filter_size_max, # bytesize maximum
            'mod_min': filter_mod_min, # modtime minimum
            'mod_max': filter_mod_max, # modtime maximum
            'name': filter_filename, # filename filter
            'dir': filter_dir # directory filter
        }

        files = smb.get_files(shares, share, filter)

        # list shares in a table for the user
        if list_shares == True:
            display.shares(shares)
        
        # list files 
        if list_files == True:
            display.files(files) 

        # download files if flag is set for it
        # the target file/folder structure will remain the same as on the share
        # [download_dir]/[target]/[share]/file/path/on/the/share.jpg
        if directory and os.path.exists(directory):
            smb.download(directory, files)

    except Exception as e:
        print(f"Error: {str(e)}")

def banner():
    print("               _               _     _           ")
    print(" ___ _ __ ___ | |__  ___ _ __ (_) __| | ___ _ __ ")
    print("/ __| '_ ` _ \| '_ \/ __| '_ \| |/ _` |/ _ \ '__|")
    print("\__ \ | | | | | |_) \__ \ |_) | | (_| |  __/ |   ")
    print("|___/_| |_| |_|_.__/|___/ .__/|_|\__,_|\___|_|   ")
    print("                        |_|                      ")
    print()

if __name__ == '__main__':
    main()
