import platform  # to check users operating system
import re
import subprocess  # to invoke ls or dir which lists files in a folder
import mpyq
import spreadsheet_util
from replay_info import ReplayInfo

# TODO: 
#   loading settings from file
#   loading files from directory outputing stats
#   send to spreadsheet
#   making project modular
#   make it compatible with different systems


##TODO: directory
def getListOfReplayNames(directory):
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
    replays = getListOfReplayNames('replays') # files contains all the sc2replay
    for replay in replays:
        archive = mpyq.MPQArchive(replay)
        replayInfo = ReplayInfo(archive)

        playerInfo = replayInfo.getPlayerInfo()
        
        win = playerInfo[1]['result']
        if win == '2':
            win = 0
        mapName = replayInfo.getMapName()
        matchup = replayInfo.getMatchup()
        mymmr = playerInfo[1]['mmr']
        oppmmr = playerInfo[0]['mmr']
        date, time = replayInfo.getDateAndTime()
        gameTime = replayInfo.getDuration()
        
        print(mapName)
        print(mymmr, oppmmr)

        print(playerInfo[1]['name'], matchup)
        
        #TODO: calculate id
        # sheet.append_row(['', gameDate, gameTime, matchup, 
        #     win, mapName, playerInfo[0]['name'], oppmmr, mymmr] )



if __name__ == '__main__':
    main()
