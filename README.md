# smbspider

An urgent task was given to create a python script that could traverse multiple sambashares on multiple hosts.

Requirements for the code:
- Python 3
- Enumerate shares
- Enumerate files on shares or a single share based on filter options
- Download selected files, ex. based on bytesize and moddate
- Download files in directories, based on search filter
- Handle unicode characters, ex. cyrillic, mandarin
- Skip download if they are found on disk, ex. previous download

The script supports all requirements as given in the task as well as 1 scope creeped feature described below. 

Task asks to point out an area that was implemented particularly well.
For me that part could be the get_files() method in smb.py, as the code is pretty easy to extend with more filters.

A quick brainstorm for more filter ideas:
- MD5 checksums
- File extensions
- Reqular expressions (could be passed through to smbmap directly using -A PATTERN)

# Self-inflicted scope creep

I found it interesting to expand the script with:
- Ping function, to resolve avg. ms and make an OS guess based on ttl
