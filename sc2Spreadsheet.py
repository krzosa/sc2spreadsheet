import re
import os
import mpyq
import spreadsheet_util
import configuration
from replay_info import ReplayInfo


def getListOfReplayNames(directory):
    
    # TODO: sort by date ALSO I SHOUKD USE A PYTHON LIBRARY TO DO THIS
    arr = os.listdir(directory)
    if 'analyzed' not in arr:
        os.mkdir(directory + '/analyzed')
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(directory + '/' + arr[i])

    return files


# TODO: check if this is game end date or not

def main():
    sheet = spreadsheet_util.getGoogleSheetObject()
    for directory in configuration.replaysDirectories:
        replays = getListOfReplayNames(directory) # files contains all the sc2replay
    
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
                    date,
                    time,
                    gameDuration,
                    name,
                    mmr,
                    win,
                    matchup,
                    mapName,
                    oppname,
                    oppmmr,
                    opphleague,
                ]) 
            date = date.replace(':', '-')
            time = time.replace(':', '-')
            gameDuration = gameDuration.replace(':', '-')
            # os.rename(replay, directory + '\\analyzed\\' + date + ' ' + time + matchup +  str(mmr) + '.SC2Replay')
            os.rename(replay, ("%s\\analyzed\\%s %s %s %s %s %s.SC2Replay" 
                        %(directory, matchup, oppmmr, mapName, gameDuration, date, time)))
        
        



if __name__ == '__main__':
    main()
