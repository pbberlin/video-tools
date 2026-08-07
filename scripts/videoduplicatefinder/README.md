# Video Duplicate Finder 

## The software itself

github.com/0x90d/videoduplicatefinder

```bash

#  help
vdf-cli.exe  scan       -h
vdf-cli.exe  compare    -h


#  first step - scan
vdf-cli.exe scan ^
--db "C:\users\pbu\dropbox" ^
--include-images ^
--use-phash ^
--hardware-accel auto ^
--exclude  "C:\users\pbu\dropbox\software"   ^
--include  "C:\users\pbu\dropbox"    ^
--include  "C:\users\pbu\Videos"    


#  second step
vdf-cli.exe compare ^
--db "C:\users\pbu\dropbox" ^
--include-images ^
--use-phash ^
--hardware-accel auto ^
--partial-clip-detection  ^
--ai-matching   ^
--format json   --output "C:\users\pbu\dropbox\dupes.json" 


```
