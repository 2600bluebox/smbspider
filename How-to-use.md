# Usage

## Help
$ python smbspider.py --help

## List shares 
$ python smbspider.py --host 127.0.0.1 --list-shares --quiet

## List shares and files
$ python smbspider.py --host 127.0.0.1 --list-shares --list-files --quiet

## List files on explicit share
$ python smbspider.py --host 127.0.0.1 --list-files --share 'ctf' --quiet

## Download filtered files
$ mkdir download
$ python smbspider.py --host 127.0.0.1 --list-files --share 'ctf' --directory ./download --quiet

## List files and narrow down to minimum and maximum bytesize
$ python smbspider.py --host 127.0.0.1 --list-files --filter-size-min 1000 --filter-size-max 3000 --quiet

## List files and filter by filename
$ python smbspider.py --host 127.0.0.1 --list-files --filter-filename 'id_rsa' --quiet

## List files and filter by folder with a containing name
$ python smbspider.py --host 127.0.0.1 --list-files --filter-dir '.ssh' --filter-size-min 1000 --quiet

## List files and filter by modified datetime intervals
$ python smbspider.py --host 127.0.0.1 --list-files --filter-mod-min '2023-05-13 11:58:00' --filter-mod-max '2023-05-15 00:30:00' --quiet

## Ping the host and return avg. ms and os guess based on ttl
$ cd ~/smbspider && python smbspider.py --host 127.0.0.1 --ping --quiet

## Running on multiple hosts, ping
$ for host in $(cat hosts); do python smbspider.py --host $host --ping --quiet; done

## Running on multiple hosts
$ for host in $(cat hosts); do python smbspider.py --host $host --list-shares --quiet; done

