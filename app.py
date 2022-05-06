from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import numpy as np
import time
import requests
import random
import aiohttp
import seaborn as sns
import re
import streamlit as st

tracklist = ['DS Delfino Square', 'DS Desert Hills', 'DS Peach Gardens', 'DS Yoshi Falls', 'GBA Bowser Castle 3', 'GBA Shy Guy Beach', 'GCN DK Mountain', 'GCN Mario Circuit', 'GCN Peach Beach', 'GCN Waluigi Stadium', "N64 Bowser's Castle", "N64 DK's Jungle Parkway", 'N64 Mario Raceway', 'N64 Sherbet Land', 'SNES Ghost Valley 2', 'SNES Mario Circuit 3', "Wii Bowser's Castle", 'Wii Coconut Mall', 'Wii DK Summit', 'Wii Daisy Circuit', 'Wii Dry Dry Ruins', 'Wii Grumble Volcano', 'Wii Koopa Cape', 'Wii Luigi Circuit', 'Wii Maple Treeway', 'Wii Mario Circuit', 'Wii Moo Moo Meadows', 'Wii Moonview Highway', 'Wii Mushroom Gorge', 'Wii Rainbow Road', "Wii Toad's Factory", "Wii Wario's Gold Mine"]

async def getJSONData(full_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as r:
                if r.status == 200:
                    js = await r.json()
                    return js
    except:
        return None

def getTrackData(player_id):
    url = 'https://mkwlounge.gg/ladder/player.php?player_id={}&ladder_id=3'.format(player_id)
    # print(url)
    playerpage = requests.get(url, timeout=3)
    playersoup = bs(playerpage.content)
    playertables = playersoup.find_all('table')
    dfs = pd.read_html(str(playertables))[3]
    return dfs


def formatTrackData(df, index):
    df.drop(['Std Dev Time', 'Average Points', 'Average Time', 'Slowest Time'], axis=1, inplace=True)
    df.rename(columns = {'Fastest Time':'Average Time'}, inplace = True)
    melted = df.pivot(index = 'Engine', columns='Track')
    melted = melted.drop('Mirror', axis=0, errors='ignore')
    melted = melted.drop('100cc', axis=0, errors='ignore')
    melted = melted.rename(index={'150cc': index})
    return melted

upperDict = {'Average Placement':'AP',
             'Average Time': 'AT',
             'Races': 'R',
             'player_id':'player_id'}
def renameCols(df):
    df.rename(columns=lambda x: upperDict[x], level=0, inplace=True)
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df.drop(['AT -','AP -', 'R -'], axis=1, inplace=True)
    df.rename(columns=lambda c: c.replace(' (Nintendo)',''), inplace=True)
    df.index.name = None
    return df

async def getPlayerData():
    metadata = await getJSONData('https://www.mkwlounge.gg/api/ladderplayer.php?ladder_type=rt&all=1')
    playerdata = pd.DataFrame(metadata['results'])
    playerdata = playerdata[['player_id','player_name','current_mmr','current_lr','current_class','win_percentage','win10_percentage','average_score','average10_score','total_events']]
    playerdata = playerdata.loc[playerdata["total_events"]!= 0]
    playerdata = playerdata.loc[playerdata["current_mmr"] >= 0]
    return playerdata

def getTime(time):
    min, sec = time.split(':')
    t = (int(min) * 60) + float(sec) 
    
    return t

def typeColumns(combodata):
    APcols = combodata.columns[10:42]
    ATcols = combodata.columns[42:74]
    Rcols = combodata.columns[74:106]
    for r in Rcols:
        combodata[r] = combodata[r].replace(np.nan, 0)
        combodata[r] = combodata[r].astype(int)
    for p in APcols:
        combodata[p] = combodata[p].replace(np.nan, '13th')
        combodata[p] = combodata[p].apply(lambda x: re.sub("[^0-9]", "", x)) 
        combodata[p] = combodata[p].astype(int)
    for T in ATcols:
        combodata[T] = combodata[T].apply(lambda x: getTime(x) if x != np.nan else x)
        combodata[T] = combodata[T].astype(float)
    avg = pd.DataFrame(combodata[ATcols])
    avg['current_class'] = combodata['current_class']
    groups = avg.groupby('current_class')
    means = groups.mean()
    # means.loc['Class A'][ATcols[0]]
    for T in ATcols:
        for i,c,m in combodata[['current_class',T]].itertuples():
            if np.isnan(m):
                combodata.at[i,T] = means.loc[c][T]

    
    return combodata


playerdata = await getPlayerData()
dfs = []
i =0
for index, row in playerdata.iterrows():
    trackdata = getTrackData(row['player_id'])
    formatData = formatTrackData(trackdata, index)
    formatData['player_id'] = row['player_id']
    dfs.append(formatData)
    # if i %100 == 0:
    #     print('working: ' + str(i))
    # i = i + 1

trackdata = pd.DataFrame().append(dfs)
trackdata = renameCols(trackdata)
combodata = pd.merge(playerdata,trackdata, left_on='player_id', right_on='player_id')

combodata = typeColumns(combodata)

st.write(combodata.iloc[0:1])