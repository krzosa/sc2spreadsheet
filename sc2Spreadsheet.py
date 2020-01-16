import mpyq
import time
import re
import subprocess # to invoke ls or dir which lists files in a folder 
import platform # to check users operating system
from datetime import datetime
from s2protocol import versions

# TODO: 
#   loading settings from file
#   loading files from directory outputing stats
#   send to spreadsheet
#   making project modular
#   make it compatible with different systems


def getGameTime(header):
    # game time from sc2 client / game loops to time
    diff = (8*60+30)/(3*60+10.50)
    seconds = round(header['m_elapsedGameLoops'] * diff)
    # converting to time format
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f'{h:d}:{m:02d}:{s:02d}'


# returns the time and date when the game was played
# TODO: check if this is game end date or not
def getGameDate(protocolDetails):
    return datetime.fromtimestamp(round(
            protocolDetails['m_timeUTC'] / (10 * 1000 * 1000) - 11644473600 - 
                        ((protocolDetails['m_timeLocalOffset'] / 10000000))))


def getPlayerInfo(protocolDetails, protocolInitData, playerCount=2):
    playerInfo = []
    for i in range(0, playerCount):
        playerInfo.append(
                {
            "name": 
                str(protocolDetails['m_playerList'][i]['m_name']),
            "race": 
                str(protocolDetails['m_playerList'][i]['m_race']),
            "result":
                str(protocolDetails['m_playerList'][i]['m_result']),
            "mmr":
                str(protocolInitData['m_syncLobbyState']
                    ['m_userInitialData'][i]['m_scaledRating']),
            "highestLeague":
                str(protocolInitData['m_syncLobbyState']
                    ['m_userInitialData'][i]['m_highestLeague'])
                }
            )
    return playerInfo


def getPlayerCount(protocolDetails):
    return len(protocolDetails['m_playerList'])


def getMapName(protocolDetails):
    return protocolDetails['m_title']


def getProtocolDetails(protocol, archive):
    return protocol.decode_replay_details(
                archive.read_file('replay.details'))


def getProtocolInitData(protocol, archive):
    return protocol.decode_replay_initdata(
                archive.read_file('replay.initData'))


def getHeaderAndProtocol(archive):
    contents = archive.header['user_data_header']['content']
    header = versions.latest().decode_replay_header(contents)
    protocol = versions.build(header['m_version']['m_baseBuild'])
    return [header, protocol]


##TODO: directory
def getListOfReplayNames(directory):
    if platform.system()=='Windows': 
        ls = subprocess.run(['cmd.exe','/c', 'dir /b /a-d'], capture_output = True,
            text = True)
    else:
        ls = subprocess.run('ls', capture_output = True,
        text = True)

    arr = re.split("\n", ls.stdout)
    files = []
    for i in range(0,len(arr)):
        if ".SC2Replay" in arr[i]:
            files.append(arr[i])

    return files

# ls D:/apps

def main():

    

    replays = getListOfReplayNames('aa') # files contains all the sc2replay
    for replay in replays:
        archive = mpyq.MPQArchive(replay)
        # archive = mpyq.MPQArchive('Efemeryda ER.sc2replay')
        header, protocol = getHeaderAndProtocol(archive)

        protocolDetails = getProtocolDetails(protocol, archive)
        protocolInitData = getProtocolInitData(protocol, archive)

        print(getPlayerInfo(protocolDetails, protocolInitData))
        print(getMapName(protocolDetails))
        print(getGameDate(protocolDetails))
        print(getGameTime(header))







if __name__ == '__main__':
    main()




