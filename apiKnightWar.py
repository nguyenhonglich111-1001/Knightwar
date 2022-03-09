import time
import random
import requests
from assetapi import *
from teleNotice import *
import datetime

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
        'highPrice': 7000
    },
    'optionStar': {
        'star1': False,
        'star2': True,
        'star3': True,
        'star4': True,
        'star5': True,
        'star6': True
    },
    'pageIndex': 1,
    'pageSize': 300,
    'sort_column': 'sellPrice',
    'sort_type': 1
}

# Global Variable
idList = []
priceDict = {}


def toFile_owner():
    global response

    weapons = response.json()['data']['result']

    with open('F:/Python/Knightwar/owner.txt', 'w') as file1:
        for weapon in weapons:
            file1.write(str(weapon['id']) + ' ' + weapon['user']['walletId'] + '\n')


def toFile_price():
    global response

    weapons = response.json()['data']['result']

    with open('F:/Python/Knightwar/price.txt', 'w') as file1:
        for weapon in weapons:
            file1.write(str(weapon['id']) + ' ' + weapon['sellPrice'][:-18] + '\n')


def craw_priceDict():
    global response
    global priceDict
    weapons = response.json()['data']['result']

    for weapon in weapons:
        priceDict[str(weapon['id'])] = weapon['sellPrice'][:-18]

    return priceDict


def craw_idList():
    global response
    global idList
    idList.clear()
    weapons = response.json()['data']['result']

    for weapon in weapons:
        idList.append(weapon['id'])

    return idList


def toFilte_idList():
    global idList

    with open('F:/Python/Knightwar/id.txt', 'w') as file1:
        for id in idList:
            file1.write(str(id) + '\n')


def compare_OldOwner():
    global idList
    global priceDict
    global response
    weapons = response.json()['data']['result']

    # Old owner
    with open('F:/Python/Knightwar/owner.txt', 'r') as file1:
        oldOwnerList = file1.readlines()

    oldOwner = {}

    for waepon in oldOwnerList:
        oldOwner[waepon.split(' ')[0]] = waepon.split(' ')[1].split('\n')[0]

    # Old price

    with open('F:/Python/Knightwar/price.txt', 'r') as file1:
        oldPriceList = file1.readlines()

    oldPrice = {}

    for waepon in oldPriceList:
        oldPrice[waepon.split(' ')[0]] = waepon.split(' ')[1].split('\n')[0]

    # Old id
    with open('F:/Python/Knightwar/id.txt', 'r') as file1:
        oldIDList = file1.readlines()

    oldId = []

    for id in oldIDList:
        oldId.append(id.split('\n')[0])

    # # new Data and compare
    # url = 'https://nft.knightwar.io/asset/'
    marketplace_url = 'https://marketplace.knightwar.io/marketplace/nft/'

    # Check new weapon
    for id in idList:

        # if str(id) not in oldOwner:
        #     send_test_message(str(id) + ' new to de marketplace \nLink here: ' + marketplace_url+str(id))

        # compare time

        # dps[0] baseDPS
        # dps[1] type
        # dps[2] star
        # dps[3] level
        # dps[4] info
        # dps[5] baseHP

        #  New one, not int old id
        if str(id) not in oldId:
            dps = dpsCalc(str(id))
            time.sleep(6)
            print(str(id) + ' ' + dps[2][0])
            # if dps[2][0] == '1':
            #     if dps[0] >= 333:
            #         send_test_message('1 NEW ' + dps[2] + '\n'
            #                           + dps[1] + '\n'
            #                           + str(dps[7]) + 'dps -->' + str(dps[8]) + 'dps\n'
            #                           + dps[3] + ', ' + dps[4] + '\n'
            #                           + str(priceDict[str(id)]) + 'KWS\n'
            #                           + marketplace_url + str(id))
            #     if dps[5] >= 1600 and dps[1] == 'sword':
            #         send_test_message('1* Basehp ' + dps[2] + '\n'
            #                           + dps[1] + '\n'
            #                           + str(dps[7]) + 'dps -->' + str(dps[8]) + 'dps\n'
            #                           + dps[3] + ', ' + dps[4] + '\n'
            #                           + str(priceDict[str(id)]) + 'KWS\n'
            #                           + marketplace_url + str(id))



            if dps[8] >= 3900:
                send_test_message('NEW    ' + dps[2] + '\n'
                                  + dps[1] + '\n'
                                  + str(dps[7]) + ' dps      -->     ' + str(dps[8]) + ' dps\n'
                                  + dps[5] + '\n'
                                  + dps[6] + '\n'
                                  + dps[3] + ', ' + dps[4] + '\n'
                                  + str(priceDict[str(id)]) + 'KWS\n'
                                  + marketplace_url + str(id))

            if int(priceDict[str(id)]) <= 400:
                send_test_message('SUPERRRRRRR DEALLLLLL\n' + marketplace_url + str(id))
        else:

            try:
                if int(priceDict[str(id)]) != int(oldPrice[str(id)]):
                    dps = dpsCalc(str(id))
                    time.sleep(6)
                    if dps[8] >= 3900:
                        send_test_message('Change Price NEW ' + dps[2] + '\n'
                                          + dps[1] + '\n'
                                          + str(dps[7]) + 'dps -->' + str(dps[8]) + 'dps\n'
                                          + dps[5] + '\n'
                                          + dps[6] + '\n'
                                          + dps[3] + ', ' + dps[4] + '\n'
                                          + str(oldPrice[str(id)]) + 'KWS ->' + str(priceDict[str(id)]) + '\n'
                                          + marketplace_url + str(id))

            except:
                pass


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')
        time.sleep(1)
        t -= 1


def run():
    # # Lay ve idlist
    idList = craw_idList()
    priceDict = craw_priceDict()

    # # So Khop owner va thong bao
    compare_OldOwner()
    # #
    # #
    # #
    # # # Update id and owner and price
    toFilte_idList()
    toFile_owner()
    toFile_price()


preTotal = -1
curTotal = 0
i = 0
response = requests.post(url, json=body)
while 1:
    i += 1

    try:

        # curTotal = response.json()['data']['total']
        # if curTotal != preTotal:
        #     send_test_message('Total from ' + str(preTotal) + ' to ' + str(curTotal))
        #     preTotal = curTotal

        run()

        print('Done' + str(i) + ' ' + str(datetime.datetime.now().time()))

        if i == 1:
            send_test_message('Start!')


    except Exception as ex:
        print(ex)
        print('error in run')
        time.sleep(180)
        pass
    if i % 30 == 0:
        time.sleep(200)
    time.sleep(50)

    # Change user agent
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
    try:
        response = requests.post(url, json=body, headers=headers1, timeout=10)
        response.close()
        print(response.json()['statusCode'])
    except:
        time.sleep(180)
        pass

    if response.json()['statusCode'] != 201:
        send_test_message('Break dude to api')
        break

    time.sleep(50)
