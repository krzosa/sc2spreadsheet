import re
import os
import mpyq
import spreadsheet_util
import configuration
from replay_info import ReplayInfo

# TODO: EXCEL Integration

def getListOfReplayNames(directory):
    arr = os.listdir(directory)
    if 'analyzed' not in arr:
        os.mkdir(directory + '/analyzed')
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(directory + '/' + arr[i])
    return files


def resultAsString(result):
    if result == 1:
        return "WIN"
    return "LOSS"


def main():
    sheet = spreadsheet_util.getGoogleSheetObject()
    for directory in configuration.replaysDirectories:
        replays = getListOfReplayNames(directory)
    
        print(replays)
        for replay in replays:
            archive = mpyq.MPQArchive(replay)
            replayInfo = ReplayInfo(archive)
            playerIndex = replayInfo.getPlayerIndex()
            oppIndex = replayInfo.getOpponentIndex()
            
            name = replayInfo.getPlayerName(playerIndex)
            oppname = replayInfo.getPlayerName(oppIndex)
            # FIXME: check matchup
            matchup = replayInfo.getMatchup(playerIndex, oppIndex)
            win = replayInfo.didPlayerWin(playerIndex)
            mmr = replayInfo.getPlayerMMR(playerIndex)
            oppmmr = str(replayInfo.getPlayerMMR(oppIndex))
            opphleague = replayInfo.getPlayerHighestLeague(oppIndex)
            date, time = replayInfo.getDateAndTime()
            mapName = replayInfo.getMapName()
            gameDuration = replayInfo.getDuration()
            archive = ''
                
            print("INSERTING")
            sheet.append_row([
                    win,
                    matchup,
                    mapName,
                    gameDuration,
                    mmr,
                    oppmmr,
                    name,
                    oppname,
                    opphleague,
                    date,
                    time,
                ]) 


            # Renaming and moving replays
            time = time.replace(':', '-')
            gameDuration = gameDuration.replace(':', '-')
            win = resultAsString(win)
            os.rename(replay, ("%s\\analyzed\\%s %s %s %s %s %s %s.SC2Replay" 
                        %(directory, matchup, win, oppmmr, mapName, gameDuration, date, time)))
        
        



if __name__ == '__main__':
    main()
