import platform  # to check users operating system
import re
import subprocess  # to invoke ls or dir which lists files in a folder
import mpyq
import spreadsheet_util
import configuration
from replay_info import ReplayInfo

# TODO: 
#   loading settings from file
#   loading files from directory outputing stats
#   send to spreadsheet
#   making project modular
#   make it compatible with different systems


def getListOfReplayNames(directory):
    
    # TODO: sort by date ALSO I SHOUKD USE A PYTHON LIBRARY TO DO THIS
    # pathing problems when pointing at sc2 replay repo
    if platform.system()=='Windows': 
        ls = subprocess.run(['cmd.exe','/c', 'dir ' + directory + ' /b /a-d'], capture_output = True,
            text = True)
    else:
        ls = subprocess.run('ls ' + directory, capture_output = True,
            text = True)

    arr = re.split("\n", ls.stdout)
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(directory + '/' + arr[i])

    return files


# TODO: check if this is game end date or not







def main():
    sheet = spreadsheet_util.getGoogleSheetObject()
    replays = getListOfReplayNames(configuration.replaysDirectory) # files contains all the sc2replay
    for replay in replays:
        archive = mpyq.MPQArchive(replay)
        replayInfo = ReplayInfo(archive)

        if replayInfo.getPlayerName(0) in configuration.usernames:
            name = replayInfo.getPlayerName(0)
            oppname = replayInfo.getPlayerName(1)
            # FIXME: 
            matchup = replayInfo.getMatchupReverse()
            win = replayInfo.didPlayerWin(0)
            mmr = replayInfo.getPlayerMMR(0)
            oppmmr = replayInfo.getPlayerMMR(1)
            opphleague = replayInfo.getPlayerHighestLeague(1)
        else:
            name = replayInfo.getPlayerName(1)
            oppname = replayInfo.getPlayerName(0)
            # FIXME: 
            matchup = replayInfo.getMatchup()
            win = replayInfo.didPlayerWin(1)
            mmr = replayInfo.getPlayerMMR(1)
            oppmmr = replayInfo.getPlayerMMR(0)
            opphleague = replayInfo.getPlayerHighestLeague(0)
            
        date, time = replayInfo.getDateAndTime()
        print("INSERTING")
        sheet.append_row([
                '',
               date,
               time,
               replayInfo.getDuration(),
               name,
               mmr,
               win,
               matchup,
               replayInfo.getMapName(),
               oppname,
               oppmmr,
               opphleague,
           ]) 
        



        #TODO: calculate id
        
        



if __name__ == '__main__':
    main()
