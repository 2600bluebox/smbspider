"""
Functions used for various network stuff
"""

import os

from enumeration import core 
from subprocess import PIPE, run

"""
Allows for ping of targets
Display and avg. ms response time as well as a qualified os guess based on ttl
"""
def ping(targets):
    
    for target in targets:

        # params
        counts = 5

        core.message(f"Pinging {target} ", True)
        
        # run the ping cmd
        command = f"ping -c {str(counts)} {target}"
        result = run(command.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        # result parsing
        if '100% packet loss' in result.stdout:
            core.message(f"(Host seems down!)", False, True)
        else:
            ms = float(0)
            ttl = 0

            for line in result.stdout.split("\n"):
                if 'bytes from' not in line:
                    continue
                
                # time 
                time = float(line.split("time=")[1].split(" ")[0])

                # ttl
                ttl = line.split("ttl=")[1].split(" ")[0]

                ms = ms + time

            os = os_from_ttl(ttl)
            core.message(f"(Ping avg: {ms:.3f}ms, ttl={ttl}, os: {os})", False, True)

"""
Allows for resolvement of operating system based on a ttl value
Wikis online are flooded with details on ttl values

For the sake of simplicity in this script we stick to Linux, Windows, Unix

Ref: https://subinsb.com/default-device-ttl-values/
"""
def os_from_ttl(ttl):

    os = ''
    match ttl:
        case '32':
            os = 'Windows (95 => NT 4.0)'
        case '64':
            os = '*nix (Linux/Unix)'
        case '128':
            os = 'Windows'
        case '254':
            os = 'Solaris/AIX'
        case _:
            os = 'Unknown!'
        
    return os 
    