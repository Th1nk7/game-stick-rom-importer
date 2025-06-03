# ROM/Game importer tool
This tool is used to simplify importing ROMs onto the 4k Game Stick Lite.  
It both imports the game file itself and inserts the correct values into games.db.

Tested for "M8 V7.3 4k Game Stick Lite"

## Before using the tool
- Fully backup the SD Card before doing anything else
- Mount the large (most likely 5th) partition /mnt/games
  - Alternatively change the location of the games.db file set in the script

## Using the tool


## After using the tool
Check for sdX with ```lsblk```
```
sync
sudo eject /dev/sdX
```
