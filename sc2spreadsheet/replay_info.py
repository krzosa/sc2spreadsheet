import time
import configuration
from enum import Enum
from datetime import datetime
from s2protocol import versions



# input: MPQArchive(replay) object. Which is used to unpack
# sc2replay which is basically an archive
# init: decoding files from the archive
# protocolInitData contains stuff like mmr, map, game time etc.
# protocolDetails contains info about players and some other things
# header contains information about the game itself
class ReplayInfo:
    def __init__(self, archive):
        self.contents = archive.header['user_data_header']['content']
        self.header = versions.latest().decode_replay_header(self.contents)
        self.protocol = versions.build(self.header['m_version']['m_baseBuild'])

        self.protocolDetails = self.protocol.decode_replay_details(
                                archive.read_file('replay.details'))
        self.protocolInitData = self.protocol.decode_replay_initdata(
                                archive.read_file('replay.initData'))

        self.playerInfo = self.getPlayerInfo()
        self.playerIndex = self.getPlayerIndex()
        self.oppIndex = self.getOpponentIndex()


    def getPlayerInfo(self, playerCount=2):
        playerInfo = []
        for i in range(0, playerCount):
            playerInfo.append({
                "name": self.protocolDetails['m_playerList']
                                            [i]['m_name'].decode('utf-8'),
                "race": self.protocolDetails['m_playerList']
                                            [i]['m_race'].decode('utf-8'),
                "result": self.protocolDetails['m_playerList']
                                              [i]['m_result'],
                "mmr": self.protocolInitData['m_syncLobbyState']['m_userInitialData']
                                            [i]['m_scaledRating'],
                "highestLeague": self.highestLeague(self.protocolInitData['m_syncLobbyState']
                                                                         ['m_userInitialData']
                                                                         [i]['m_highestLeague'])
            })
        return playerInfo


    class highestLeague(Enum):
        UNRANKED = 8
        GM = 7
        MASTER = 6
        DIAMOND = 5
        PLATINUM = 4
        GOLD = 3
        SILVER = 2
        BRONZE = 1
        VSAI = 0


    # return: number of players in the lobby
    def getPlayerCount(self):
        return len(self.protocolDetails['m_playerList'])


    def getMapName(self):
        return self.protocolDetails['m_title'].decode('utf-8')


    # return: ex. TvZ - first letters of players races
    def getMatchup(self):
        return self.playerInfo[self.playerIndex]['race'][0] + 'v' + self.playerInfo[self.oppIndex]['race'][0]


    # input: index of the player(in 1v1 => 0 or 1)
    # return: username
    def getPlayerName(self, playerIndex):
        return self.playerInfo[playerIndex]['name']


    # input: index of the player(in 1v1 => 0 or 1)
    # return: players race
    def getPlayerRace(self, playerIndex):
        return self.playerInfo[playerIndex]['race']


    # input: index of the player(in 1v1 => 0 or 1)
    # return: result translates to placing
    # 1 - first place , 2 - second place etc. 
    def getPlayerMatchResult(self, playerIndex):
        return self.playerInfo[playerIndex]['result']


    # input: index of the player(in 1v1 => 0 or 1)
    # return: players current ladder rating
    def getPlayerMMR(self, playerIndex):
        return self.playerInfo[playerIndex]['mmr']


    # input: index of the player(in 1v1 => 0 or 1)
    # return: highest rank that player got ex. MASTER
    # in s2protocol they don't specify if its highest
    # rank in season or ever achieved or in gamemode 
    def getPlayerHighestLeague(self, playerIndex):
        return self.playerInfo[playerIndex]['highestLeague'].name


    # return: date and time when the game happened 
    # TODO: check if its when the game ended begun
    def getDateAndTime(self):
        date = str(datetime.fromtimestamp(round(
            self.protocolDetails['m_timeUTC'] / (10 * 1000 * 1000) - 11644473600 - 
                ((self.protocolDetails['m_timeLocalOffset'] / 10000000)))))
        return date.split(' ')


    # return: how long the game lasted
    # i calculated it by taking time displayed in sc2 client
    # and divided it by game loops which at the time I translated
    # to regular time. It has +-1s error so no reason to change
    def getDuration(self):
        diff = (8*60+30)/(3*60+10.50)
        seconds = round(self.header['m_elapsedGameLoops'] * diff)
        # converting from game loops to time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return f'{h:d}:{m:02d}:{s:02d}'

    
    # input: index of the player(in 1v1 => 0 or 1)
    # return: 1 if player won, 0 if player lost 
    def didPlayerWin(self, playerIndex):
        if(self.playerInfo[playerIndex]['result'] == 1):
            return 1
        return 0

    
    # 1v1
    # return: index of player who's username you gave in config file
    def getPlayerIndex(self):
        if self.getPlayerName(0) in configuration.usernames:
            return 0
        return 1

    # 1v1
    # return: index of player who's username is not in the config file
    def getOpponentIndex(self):
        if self.getPlayerName(0) in configuration.usernames:
            return 1
        return 0


