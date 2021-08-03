#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests ,json
import pandas as pd
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62', 'x-requested-with': 'XMLHttpRequest'}

def SearchData(start, end, period):
    data={
        'curr_id': '6408',
        'smlID': '1159963',
        'header': 'AAPL历史数据',
        'st_date': str(start)[:4]+'/'+str(start)[4:6]+'/'+str(start)[6:8],
        'end_date': str(end)[:4]+'/'+str(end)[4:6]+'/'+str(end)[6:8],
        'interval_sec': period,
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data'}
    res = requests.post('https://cn.investing.com/instruments/HistoricalDataAjax', data=data, headers=headers)
    dfs = pd.read_html(res.text, encoding='utf-8')
    df=dfs[0]
    Jdict={}
    for i in range(len(df)):
        date=ChiDateToNum(df.loc[i]['日期'])
        Jdict[date]={}
        for index in df.columns:
            Jdict[date][index]=df.loc[i][index]
    with open(f'{start}-{end}股價.json', 'w', encoding='utf-8') as f:
        json.dump(Jdict, f, ensure_ascii=False, indent=4)
    return()

def ChiDateToNum(date):
    year=date[:date.index('年')]
    mon=date[date.index('年')+1:date.index('月')]
    day=date[date.index('月')+1:date.index('日')]
    if len(mon)==1:mon='0'+mon
    if len(day)==1:day='0'+day
    return(year+mon+day)

SearchData('20200901','20200910','Daily')

