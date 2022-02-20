import requests
import json
import time
from teleNotice import *
import random

url = 'https://nft.knightwar.io/asset/1008979'


def basestatCalc(now, star, level):
    return now / (1 + (level - 1) * star / 100)


def duplicateCalc(level):
    return (2.5 * level * level + 2.5 * level + 20) / 100


def dpsCalc(id):
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 "
        "Safari/537.36 Edge/18.19577 "
        , "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 "
        "Safari/537.36 "
        ,
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 "
        "Safari/533.20.27 "
        ,
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) "
        "Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
        ,
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1"
        ,
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        ,
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
        ,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
        ,
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        ,
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    ]
    ua = random.choice(ua_list)
    headers1 = {'User-Agent': ua}

    # Get json
    url = 'https://nft.knightwar.io/asset/' + str(id)

    try:
        x = requests.get(url, headers=headers1, timeout=10)
    except:
        return [0, 0]
    x.close()
    if x.status_code != 200:
        return [0, 0]

    # Get attributes part
    attributes = x.json()['attributes']
    abilities = x.json()['abilities']
    is_duplicate = False
    levelduplicate = 0

    # Calculate
    star = attributes[0]['value']
    level = attributes[2]['value']
    type = attributes[1]['value']
    baseATK = basestatCalc(attributes[3]['value'], star, level)
    baseSPD = basestatCalc(attributes[4]['value'], star, level)

    info = type + ' ' + str(star) + ' Star ' + ' level ' + str(level)

    for ability in abilities:
        info += ' ' + ability['name']
        if ability['name'] == 'Duplicating':
            is_duplicate = True
            levelduplicate = ability['level']

    return [int(baseSPD * baseATK * (1 + is_duplicate * duplicateCalc(levelduplicate))) + 0.1 * is_duplicate, info]


url = 'https://api.knightwar.io/item/listItem/'
body = {
    'optionClass': {
        'sword': True,
        'bow': True,
        'staff': True
    },
    'optionEnchant': {
        'enchant': 0
    },
    'optionPrice': {
        'minPrice': 0,
        'highPrice': 6500
    },
    'optionStar': {
        'star1': False,
        'star2': True,
        'star3': True,
        'star4': True,
        'star5': False,
        'star6': False
    },
    'pageIndex': 1,
    'pageSize': 300,
    'sort_column': 'sellPrice',
    'sort_type': 1
}
response = requests.post(url, json=body)


def craw_idList():
    global response
    global oldId
    weapons = response.json()['data']['result']

    for weapon in weapons:
        oldId.append(weapon['id'])


oldId = []

print('Wanna sleep?')
isSleep = bool(int(input()))
if isSleep:
    print('How much minutes pls?')
    minutes = int(input())
    print('Sleep now')
    time.sleep(minutes * 60)
craw_idList()
i = 0

for id in oldId:
    try:
        i += 1
        dps = dpsCalc(id)
        print(str(id) + ' ' + str(dps))
        if dps[0] >= 500:
            response = requests.get('https://api.knightwar.io/item/getItemById/' + str(id))
            price = response.json()['data']['sellPrice'][:-18]

            send_test_message(
                str(dps) + ' ' + price + 'KWS\n' + 'https://marketplace.knightwar.io/marketplace/nft/' + str(id))

        if i % 15 == 0:
            time.sleep(120)
        else:
            time.sleep(5)

    except Exception as ex:
        print(id)
        send_test_message('error api')
        input()

send_test_message('Done idDiamond')
input()
# x.json()['attributes']
#   'value'
#     [0]star
#     [1]type
#     [2]level
#     [3]damage
#     [4]speed
#     [5]hp
#     [6]crit
#     [7]enchant
#     [8]owner
