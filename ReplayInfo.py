import time
from enum import Enum
from datetime import datetime
from s2protocol import versions

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


    def getPlayerInfo(self, playerCount=2):
        playerInfo = []
        for i in range(0, playerCount):
            playerInfo.append(
                    {
                "name": 
                    self.protocolDetails['m_playerList'][i]['m_name'].decode('utf-8'),
                "race": 
                    self.protocolDetails['m_playerList'][i]['m_race'].decode('utf-8'),
                "result":
                    self.protocolDetails['m_playerList'][i]['m_result'],
                "mmr":
                    self.protocolInitData['m_syncLobbyState']
                        ['m_userInitialData'][i]['m_scaledRating'],
                "highestLeague":
                    self.highestLeague(self.protocolInitData['m_syncLobbyState']
                        ['m_userInitialData'][i]['m_highestLeague'])
                    }
                )
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


    def getPlayerCount(self):
        return len(self.protocolDetails['m_playerList'])


    def getMapName(self):
        return str(self.protocolDetails['m_title'])


    def getMatchup(self):
        return self.playerInfo[1]['race'][0] + 'v' + self.playerInfo[0]['race'][0]


    def getDateTime(self):
        date = str(datetime.fromtimestamp(round(
                self.protocolDetails['m_timeUTC'] / (10 * 1000 * 1000) - 11644473600 - 
                            ((self.protocolDetails['m_timeLocalOffset'] / 10000000)))))
        return date.split(' ')


    def getGameTime(self):
        # game time from sc2 client / game loops to time
        diff = (8*60+30)/(3*60+10.50)
        seconds = round(self.header['m_elapsedGameLoops'] * diff)
        # converting to time format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return f'{h:d}:{m:02d}:{s:02d}'


