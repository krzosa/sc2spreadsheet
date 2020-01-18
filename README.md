# SC2Spreadsheet
Small Python package for personal use that decodes 
starcraft 2 replays using s2protocol, logs relevant 
information(mmr, matchup etc. ) to the google spreadsheet
and lastly renames them to something alot more informative.

## Requirements
    Python 3.8 definitely should work
    Python 3.4+ should work

## How to use (for non programmers)(windows 10)
1. download [python 3.8.1](https://www.python.org/downloads/)
    * important! during installation check that you want to add it to PATH!
1. download this repository by clicking the green button 
thats located on the top-right side of the file list
1. unzip the archive to wherever you like
1. run setup.py(it downloads external modules that I used to make this work)
1. run sc2spreadsheet.py - it should flash you a big error and by the end
it should be saying that "client_secret.json" is missing
    * if thats true then you are doing great !!
## Google spreadsheet integration (hard)
1. [follow this tutorial. Start reading at "Ok, let's begin"](https://medium.com/@denisluiz/python-with-google-sheets-service-account-step-by-step-8f74c26ed28e)
    * Stop following after you share your spreadsheet.
1. you should at this point have your client_secret.json file
in the sc2spreadsheet folder
1. now step into sc2spreadsheet folder, open configuration file and fill it out!
1. you are ready to run sc2spreadsheet! Just double-click
sc2spreadsheet.bat
    * For convenience you can make a shortcut out of
it -> send it to desktop
1. thats all ! gg wp

## Google sheet tricks
*  [I suggest sorting your replays by date and then by time](https://support.google.com/docs/answer/3540681?co=GENIE.Platform%3DDesktop&hl=en)

## Example of usage:
(spreadsheet)[https://github.com/krzosa/sc2spreadsheet/blob/master/img.png]
(files)[https://github.com/krzosa/sc2spreadsheet/blob/master/imgfiles.png]


