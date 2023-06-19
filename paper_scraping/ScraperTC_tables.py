# %% ####################################################################################
# To scrape html table directly with pandas.reda_html() and save as CSV files

import os
import pandas as pd
import numpy as np
import requests


# %% ####################################################################################
#
# read the fig/tbl records
figtblDataFile = '.\\TobaccoControl\\figtblData.csv'
figtbl_data = pd.read_csv(figtblDataFile)
    # full_data = main_data.iloc[:, 1:] # if need to drop the first column
figtbl_data.head(5)


# %% 
# iterate and grab all tables -- direct from the website

tblPath = '.\\TobaccoControl\\tableData\\tables\\'

# get authorization -- seems no need here
# proxy_headers, proxy_cookies = getAuthorizedSession()

for index, row in figtbl_data.iterrows():
    # print(index, row['vis_type'])
    # if index>20: # problem tables: 107 (figure)
    if row['filename'] != 'TC.2015.62.144905': # search for specific table
        continue
    if row['vis_type'] == 16:
        url = row['url']
        print(index, url)
        tableName = row['filename'] + '.csv'
        df = pd.read_html(url, encoding='UTF-8')[0]
        # df.to_csv(tblPath + tableName) # 'ISO-8859-1' or 'latin'

if False: # this is those require authtnetication
    for index, row in figtbl_data.iterrows():
        if index > 5:        # problematic tables: 
            break
        if row['vis_type'] == 16:
            url = row['url'] # use osu-redirected url, not the original
            print(index, url)
            r = requests.get(url, headers=proxy_headers, cookies=proxy_cookies)
            # r = requests.get(url)
            tableName = row['filename'] + '.csv'
            # print(len(pd.read_html(r.text)))
            df = pd.read_html(r.text)[0]
            df.to_csv(tblPath + tableName)

print('Scraping tables done!')


# %%
def getAuthorizedSession():
    # Have to manually initiate this session for the first time
    # Access any paper with OSU proxy and get the following from Chrome Developer tool

    proxy = os.getenv('_sn:4$_se:12$_ss:0$_st:1613546220971$vapi_domain:ohio-state.edu$ses_id:1613543674475%3Bexp-session$_pn:6%3Bexp-session')

    cookies = {
        'optimizelyEndUserId': 'oeu1604631622962r0.8979699495381592',
        '_rollupGA': 'GA1.2.459547342.1604631302',
        's_fid': '3434826249D15B39-16C9B064FD45D3D8',
        '_ga_0BJESHLY6P': 'GS1.1.1611337050.1.0.1611337051.0',
        '_ga_EXTSVLH45V': 'GS1.1.1611617628.11.1.1611617864.0',
        '__utmzz': 'utmccn=(not set)',
        'tc_ptidexpiry': '1676615644596',
        'tc_ptid': '6fFzz8YyDxV6TJpESiSfB5',
        'com.silverpop.iMAWebCookie': '74707954-0466-34db-e7d6-d45710bdb17d',
        'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1687686476%7CMCIDTS%7C18577%7CMCMID%7C39474372145734594052015963545670039167%7CMCAAMLH-1614148476%7C7%7CMCAAMB-1614148476%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1613550876s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0',
        'utag_main': f"v_id:0175b31cb65800017fef5cbed61c03073004e06b00bd0{proxy}",
        'fs_uid': 'rs.fullstory.com#ATGDR#4781211299594240:6353100159303680/1645079643',
        'amplitude_id_9f6c0bb8b82021496164c672a7dc98d6_edmohio-state.edu': 'eyJkZXZpY2VJZCI6ImY3NzZiNWY3LTYxMTItNGYxOS1hOWJiLTY0NTU2NzE1YzQwZlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYxNDYwOTgwMTMyNSwibGFzdEV2ZW50VGltZSI6MTYxNDYxMzc3NjY0MSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MjQsInNlcXVlbmNlTnVtYmVyIjoyNH0=',
        'amplitude_id_408774472b1245a7df5814f20e7484d0ohio-state.edu': 'eyJkZXZpY2VJZCI6IjZmMTNiNTIyLWQzMDUtNDMwNi04MzU2LTQ4ZGI5ZDQxZmQyNCIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjE0NjA5NTg3MDMyLCJsYXN0RXZlbnRUaW1lIjoxNjE0NjEzODA0NjYzLCJldmVudElkIjoxNTgsImlkZW50aWZ5SWQiOjc1LCJzZXF1ZW5jZU51bWJlciI6MjMzfQ==',
        '_gid': 'GA1.2.1738345297.1621961879',
        'SaneID': 'XsgrElMp7Pr-cibgufj',
        'ezproxy': 'sysFP3m5P3xhXHm',
        'ezproxyl': 'sysFP3m5P3xhXHm',
        'ezproxyn': 'sysFP3m5P3xhXHm',
        'JSESSIONID': '647756E6B2B8E992A1BAF53DED89408A',
        '__atuvc': '10%7C21',
        '__atuvs': '60ad5608836978e6000',
        '_gat_UA-78288099-3': '1',
        '_ga_GLF90ZEMKF': 'GS1.1.1621972474.3.1.1621972676.0',
        '_ga': 'GA1.2.459547342.1604631302',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://academic-oup-com.proxy.lib.ohio-state.edu/ntr/issue/17/1',
        'Accept-Language': 'en',
    }

    response = requests.get('https://academic-oup-com.proxy.lib.ohio-state.edu/ntr/article/17/1/74/2857986', headers=headers, cookies=cookies)

    return headers, cookies

    
# %%
df.head()
# %%
