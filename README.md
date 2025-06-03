# ROM/Game importer tool
This tool is used to simplify importing ROMs onto the 4k Game Stick Lite.  
It both imports the game file itself and inserts the correct values into games.db.

Tested for "M8 V7.3 4k Game Stick Lite"

## Before using the tool
- Fully backup the SD Card before doing anything else
- Mount the partition /dev/sdX5 to /mnt/games (check for sdX with ```lsblk```)
  - Alternatively change the location of the games.db file set in the script
  - ```sudo mount /dev/sdX5 /mnt/games```

## Using the tool
```
git clone https://github.com/Th1nk7/game-stick-rom-importer.git
python3 game-stick-rom-importer/importTool.py
```


## After using the tool
Check for sdX with ```lsblk```
```
sync
sudo eject /dev/sdX
```
