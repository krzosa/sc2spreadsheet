import gspread
import configuration
from oauth2client.service_account import ServiceAccountCredentials
import re
import os
import mpyq
import configuration
from replay_info import ReplayInfo

def getGoogleSheetObject():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
    client = gspread.authorize(creds)
    return client.open("Starcraft2Spreadsheet").sheet1

def insertIntoGoogleSheet():
    sheet = getGoogleSheetObject()
    # iterating through all the directories specified in config
    for directory in configuration.replaysDirectories:
        replays = getListOfReplayNames(directory)
        # iterating through all the replays in specified directories
        for replay in replays:
            archive = mpyq.MPQArchive(replay)
            replayInfo = ReplayInfo(archive)
            playerIndex = replayInfo.getPlayerIndex()
            oppIndex = replayInfo.getOpponentIndex()
            
            date, time = replayInfo.getDateAndTime()
            archive = ''
                
            print("INSERTING")
            sheet.append_row([
                    replayInfo.didPlayerWin(playerIndex),
                    replayInfo.getMatchup(),
                    replayInfo.getMapName(),
                    replayInfo.getDuration(),
                    replayInfo.getPlayerMMR(playerIndex),
                    str(replayInfo.getPlayerMMR(oppIndex)),
                    replayInfo.getPlayerName(playerIndex),
                    replayInfo.getPlayerName(oppIndex),
                    replayInfo.getPlayerHighestLeague(oppIndex),
                    date,
                    time,
                ]) 
                
            renameAndMoveReplays(directory, 
                                replay, 
                                replayInfo.didPlayerWin(playerIndex), 
                                replayInfo.getMatchup(),
                                str(replayInfo.getPlayerMMR(oppIndex)), 
                                replayInfo.getMapName(), 
                                date, 
                                time, 
                                replayInfo.getDuration())


def renameAndMoveReplays(directory, replay, win, matchup, 
                         oppmmr, mapName, date, time, gameDuration):
    time = time.replace(':', '-')
    gameDuration = gameDuration.replace(':', '-')
    win = resultAsString(win)
    os.rename(replay, ("%s\\analyzed\\%s %s %s %s %s %s %s.SC2Replay" 
        %(directory, matchup, win, oppmmr, mapName, gameDuration, date, time)))


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