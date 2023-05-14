# Installation

## Step 1
git clone https://github.com/2600bluebox/smbspider.git

## Step 2
cd smbspider

## Step 3
docker build -t smbspider-image .

## Step 4
docker run -ti --rm smbspider-image /bin/bash

## Step 5 
service smbd restart

## Step 6
su user

cd ~/smbspider && python smbspider.py --help

## Step 7 - ready
Run the following command to try and display all shares and all files.

python smbspider.py --host 127.0.0.1 --list-shares --list-files

## Notes about the image
A copy of smbspider is dropped into /home/user/smbspider. 
A samba daemon is also started on localhost which holds 2 anonymous shares on launch:

- /home/user/shares/ctf
- /home/user/shares/secret_files

The file How-to-use.md contains quite a few examples how smbspider can be used.
Alternatively the script can also be launched with the --help flag, which will show all available options.

Have fun!
