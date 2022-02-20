from bs4 import BeautifulSoup
import requests
import pandas as pd


name = ['kappachin', 'rived11011', 'rivedkws17', 'rivedkws18', 'rivedkws19', 'rivedkws20', 'rivedkws21', 'rivedkws22']
print('What season you wanna take in?')
season = input()

bossReward_URL = 'https://play.knightwar.io/top_boss_event' + season + '.htm'

response = requests.get(bossReward_URL).text

soup = BeautifulSoup(response, 'html.parser')

alltr_tags = soup.find_all(name='tr')


# tag[0] top
# tag[1] eventid
# tag[2] wallet
# tag[3] userName
# tag[4] point
# tag[5] kwsReward

# bossReward_Data = pd.read_excel()
seasonCol = []
usernameCol = []
rankCol = []
rewardCol = []
for tr_tag in alltr_tags[1:]:
    td_tags = tr_tag.find_all(name='td', class_='normal')
    if td_tags[3].string in name:
         seasonCol.append(int(td_tags[1].string))
         usernameCol.append(td_tags[3].string)
         rankCol.append(int(td_tags[0].string))
         rewardCol.append(int(td_tags[5].string))

rewardCol.append(sum(rewardCol))
rankCol.append('Total:')
seasonCol.append('')
usernameCol.append('')

oldDf = pd.read_excel('F:/Python/Knightwar/bossReward.xlsx', sheet_name='bossReward')
df = pd.DataFrame({
    'Season': seasonCol,
    'Username': usernameCol,
    'Rank': rankCol,
    'Reward': rewardCol
})

middleDf = [oldDf,df]
NewDf = pd.concat(middleDf)
# NewDf.style.set_properties(subset=['Username'], **{'width': '100px'})
NewDf.to_excel('F:/Python/Knightwar/bossReward.xlsx', sheet_name='bossReward', index=False)

