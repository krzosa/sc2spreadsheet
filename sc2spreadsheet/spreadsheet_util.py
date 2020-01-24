import re
import os
import mpyq
import gspread
import configuration as config
from replay_info import ReplayInfo
from oauth2client.service_account import ServiceAccountCredentials


# return: gspread object that represents your google sheet
# it allows you to edit it however you like and also
# take information from it
def getGoogleSheetObject():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            config.googleSpreadsheetCredentials, scope)
        client = gspread.authorize(creds)
        return client.open(config.sheetName).sheet1
    except:
        # TODO: make exception class MEME
        print("""
client_secret.json was not found. Make sure that it's in sc2spreadsheet folder.
if you are having trouble refer to the second part of the github guide.
        """)
        exit()
     


# this function iterates through all the replays in the specified
# directories appends them into your google spreadsheet
# and lastly renames those replays > moves them into analyzed folder
def insertIntoGoogleSheet():
    sheet = getGoogleSheetObject()
    # iterating through all the directories specified in config
    for directory in config.replaysDirectories:
        replays = getListOfReplayNames(directory)
        # iterating through all the replays in specified directories
        for replay in replays:
            archive = mpyq.MPQArchive(replay)
            replayInfo = ReplayInfo(archive)
            playerIndex = replayInfo.getPlayerIndex()
            oppIndex = replayInfo.getOpponentIndex()
            
            date, time = replayInfo.getDateAndTime()
            archive = ''

            if(replayInfo.getPlayerCount() == 2 and replayInfo.getPlayerHighestLeague(oppIndex) != "VSAI"):    
                print("INSERTING " + replay)
                sheet.append_row([
                        resultAsString(replayInfo.didPlayerWin(playerIndex)),
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


# return: names of all the files in the {directory}
def getListOfReplayNames(directory):
    arr = os.listdir(directory)
    if 'analyzed' not in arr:
        os.mkdir(directory + '/analyzed')
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(directory + '/' + arr[i])
    return files


# takes match result -> 1, 2, 3 etc.
# return: WIN or LOSS
def resultAsString(result):
    if result == 1:
        return "WIN"
    return "LOSS"