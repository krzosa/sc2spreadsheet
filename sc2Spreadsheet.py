import mpyq
import pprint #pretty print
import time
from datetime import datetime
from s2protocol import versions

archive = mpyq.MPQArchive('a.sc2replay')
# archive = mpyq.MPQArchive('Efemeryda ER.sc2replay')
contents = archive.header['user_data_header']['content']
header = versions.latest().decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
protocol = versions.build(baseBuild)

contents = archive.read_file('replay.details')
protocolDetails = protocol.decode_replay_details(contents)
contents = archive.read_file('replay.initData')
protocolInitData = protocol.decode_replay_initdata(contents)

gameDetails = []
playerInfo = []
gameDetails.append(len(protocolDetails['m_playerList']))

for i in range(0, gameDetails[0]):
    playerInfo.append([protocolDetails['m_playerList'][i]['m_name'],
    protocolDetails['m_playerList'][i]['m_race'],
    protocolDetails['m_playerList'][i]['m_result'],
    protocolInitData['m_syncLobbyState']['m_userInitialData'][i]['m_scaledRating'],
    protocolInitData['m_syncLobbyState']['m_userInitialData'][i]['m_highestLeague']])

gameDetails.append(protocolDetails['m_title'])

print(playerInfo, ' ', gameDetails)
gameDetails.append(protocolDetails['m_timeUTC'] / 
                  (10 * 1000 * 1000) - 11644473600 - 
                  ((protocolDetails['m_timeLocalOffset'] / 10000000)))
print(datetime.fromtimestamp(gameDetails[2]))
# print(protocolDetails['m_playerList'][0]['m_name'])
# print(protocolDetails['m_playerList'][0]['m_result'])
# print(protocolDetails['m_playerList'][0]['m_race'])
# print(protocolDetails['m_playerList'][1]['m_name'])
# print(protocolDetails['m_playerList'][1]['m_result'])
# print(protocolDetails['m_playerList'][1]['m_race'])
# print(protocolDetails['m_title'])
# print(protocolDetails['m_timeUTC'])
# print(protocolDetails['m_timeLocalOffset'])

# pprint.pprint(protocolInitData['m_syncLobbyState']['m_userInitialData'][1]['m_scaledRating'])


# contents = archive.read_file('replay.load.info')
# protocolLoadInfo = protocol.decode_replay_load_info(contents)

##game time from sc2 client / game loops to time
diff = (8*60+30)/(3*60+10.50)
seconds=round(header['m_elapsedGameLoops']*diff)

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)

gameTime = f'{h:d}:{m:02d}:{s:02d}'

print(gameTime)
