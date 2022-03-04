import requests
import json
import random




def basestatCalc(now, star, level):
    return now / (1 + (level - 1) * star / 100)


def maxLevelByStar(star):
    switcher={
        1: 50,
        2: 70,
        3: 90,
        4: 110,
        5: 130
    }

    return switcher[star]
def lvMaxstatCalc(now, star, level):
    maxLevel = maxLevelByStar(star)

    return now * (1 + (maxLevel - 1) * star / 100)

# Duplicating':0, 'Enhanced':0, 'Enraged':0, 'Explosive':0}
def duplicating(level):
    switcher = {
        0: 0,
        1: 0.25,
        2: 0.35,
        3: 0.5
    }

    return switcher[level]


def enhanced(level):
    switcher = {
        0: 0,
        1: 0.1,
        2: 0.17,
        3: 0.25
    }

    return switcher[level]


def enraged(level):
    switcher = {
        0: 0,
        1: 0.9,
        2: 1.6,
        3: 2.5
    }

    return switcher[level]


def explosive(level):
    switcher = {
        0: 0,
        1: 0.2,
        2: 0.33,
        3: 0.49
    }

    return switcher[level]
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
    baseATK = round(basestatCalc(attributes[3]['value'], star, level),2)
    baseSPD = round(basestatCalc(attributes[4]['value'], star, level),2)
    baseHP = round(basestatCalc(attributes[5]['value'], star, level),2)
    baseCRIT = round(basestatCalc(attributes[6]['value'], star, level),2)
    lvMaxATK = round(lvMaxstatCalc(baseATK, star, level),2)
    lvMaxSPD = round(lvMaxstatCalc(baseSPD, star, level),2)
    lvMaxHP = round(lvMaxstatCalc(baseHP, star, level),2)
    lvMaxCRIT = round(lvMaxstatCalc(baseCRIT, star, level),2)
    if(lvMaxCRIT > 100):
        lvMaxCRIT = 100
    skill = {'Duplicating': 0, 'Enhanced': 0, 'Enraged': 0, 'Explosive': 0}


    baseInfo = str(baseATK) + ' ' + str(baseSPD) + ' ' + str(baseHP) + ' ' + str(baseCRIT)
    lvMaxInfo = str(lvMaxATK) + ' ' + str(lvMaxSPD) + ' ' + str(lvMaxHP) + ' ' + str(lvMaxCRIT)
    skills = ' '
    for ability in abilities:
        skills += ' ' + ability['name']
        if ability['name'] in skill:
            skill[ability['name']] = ability['level']

    baseDPS = int(baseSPD*baseATK);
    lvMaxDPS = int(lvMaxSPD*lvMaxATK);
    withSkill_baseDPS = baseDPS*(1 + baseCRIT/100*(1 + enraged(skill['Enraged']) ) + duplicating(skill['Duplicating'])
                             + enhanced(skill['Enhanced']) + explosive(skill['Explosive']))
    withSkill_baseDPS = int(withSkill_baseDPS)

    withSkill_lvMaxDPS = lvMaxDPS*(1 + lvMaxCRIT/100*(1 + enraged(skill['Enraged'])) + duplicating(skill['Duplicating'])
                             + enhanced(skill['Enhanced']) + explosive(skill['Explosive']))
    withSkill_lvMaxDPS = int(withSkill_lvMaxDPS)



    return [int(baseSPD * baseATK),
            type, str(star) + ' Star(s)', str(level) + ' levels', skills, baseInfo, lvMaxInfo,
            withSkill_baseDPS, withSkill_lvMaxDPS]

print((dpsCalc(1005987)))

# dpsCalc()
# dps = dpsCalc(str(1010981))
# print('1* NEW ' + str(dps[0]) + 'dps\n' + dps[1] +
#                                       + ', ' + dps[2] + '\n' + dps[3] +
#                                        ', ' + dps[4] + '\n'
#                                    )
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
