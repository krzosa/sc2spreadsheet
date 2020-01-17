import re
import os
import mpyq
import spreadsheet_util
import configuration
from replay_info import ReplayInfo


def getListOfReplayNames(directory):
    
    # TODO: sort by date ALSO I SHOUKD USE A PYTHON LIBRARY TO DO THIS
    arr = os.listdir(directory)
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(directory + '/' + arr[i])

    return files


# TODO: check if this is game end date or not







def main():
    sheet = spreadsheet_util.getGoogleSheetObject()
    replays = getListOfReplayNames(configuration.replaysDirectory) # files contains all the sc2replay
    print(replays)
    for replay in replays:
        archive = mpyq.MPQArchive(replay)
        replayInfo = ReplayInfo(archive)
        playerIndex = replayInfo.getPlayerIndex()
        oppIndex = replayInfo.getOpponentIndex()

        
        name = replayInfo.getPlayerName(playerIndex)
        oppname = replayInfo.getPlayerName(oppIndex)
        # FIXME: 
        matchup = replayInfo.getMatchup(playerIndex, oppIndex)
        win = replayInfo.didPlayerWin(playerIndex)
        mmr = replayInfo.getPlayerMMR(playerIndex)
        oppmmr = replayInfo.getPlayerMMR(oppIndex)
        opphleague = replayInfo.getPlayerHighestLeague(oppIndex)
        date, time = replayInfo.getDateAndTime()
        
            
        print("INSERTING")
        sheet.append_row([
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
        
        



if __name__ == '__main__':
    main()
