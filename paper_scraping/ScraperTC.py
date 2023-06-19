# %%
from bs4 import BeautifulSoup
import urllib.request
import os
import requests
import urllib.error
import re
import csv
import os.path
import time
import random
import argparse


# %%
def getArticleURLs(url):

    links = []

    print ("Working on: " + url)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    website = response.read()

    soup = BeautifulSoup(website,"lxml")
    articleLinks = soup.find_all(attrs={"class":re.compile("highwire-cite highwire-cite-highwire-article highwire-citation-bmjj-toc clearfix")})
    
    prefix = 'https://tobaccocontrol.bmj.com'
    for paperTag in articleLinks:
        articleLink=paperTag.find('a', attrs={'href' : True})
        # if paperTag.string is None:
        if not 'Thank' in paperTag:
            paperhtml = prefix + str(articleLink['href'])
            # print(paperhtml)
            links.append(paperhtml)

    return links


# %%
def getSingleArticleData(url, writer, file, articleID):

    url_proxy = url.replace('tobaccocontrol.bmj.com', 'tobaccocontrol-bmj-com.proxy.lib.ohio-state.edu')
    print(url_proxy)
    response = requests.get(url_proxy, headers=proxy_headers, cookies=proxy_cookies)
    soup = BeautifulSoup(response.text,'html.parser')
    
    csvline = []

    #
    # obtain all the pieces
    #

    journalName = 'Tobacco Control'
    csvline.append(journalName)

    title = soup.find("meta", attrs = {'property':'og:title'})['content']
    csvline.append(title)

    articleType = soup.find("meta", attrs = {'name':'citation_article_type'})['content']
    csvline.append(articleType)

    authorTags = soup.find_all("meta", attrs = {'name':'citation_author'})
    authornames = ''
    if not (authorTags is None):
        for author in authorTags:
            authornames += author['content'] + '; '
    csvline.append(authornames)

    affiliationTags = soup.find_all("meta", attrs = {'name':'citation_author_institution'})
    authoraffiliations = ''
    if not (affiliationTags is None):
        for affiliation in affiliationTags:
            authoraffiliations += affiliation['content'] + '; '
    csvline.append(authoraffiliations)

    firstpage = soup.find("meta", attrs = {'name':'citation_firstpage'})['content']
    csvline.append(firstpage)

    lastpage = soup.find("meta", attrs = {'name':'citation_lastpage'})['content']
    csvline.append(lastpage)

    paperYear = soup.find("meta", attrs = {'name':'citation_publication_date'})['content'].split('/')[0]
    csvline.append(paperYear)

    paperID = soup.find("meta", attrs = {'name':'citation_id'})['content']
    csvline.append(paperID)

    doiTag = soup.find("meta", attrs = {'name':'citation_doi'})
    doi = ''
    if not (doiTag is None):
        doi = 'http://dx.doi.org/'+doiTag['content']
    csvline.append(doi)

    abstractTag = soup.find_all('div', class_='section abstract') # soup.find("meta", attrs={'name':'citation_abstract'})
    abstract = '' 
    if not (abstractTag is None):
        for elem in abstractTag:
            paragraphs=elem.find_all('p')
            for paragraph in paragraphs:
                abstract += paragraph.text + ' '
    csvline.append(abstract)

    whatsNewTag = soup.find_all(attrs={"class": re.compile("boxed-text")})
    whatsNew = ""
    if not (whatsNewTag is None):
        for elem in whatsNewTag:
            paragraphs=elem.find_all('p')
            for paragraph in paragraphs:
                whatsNew += paragraph.text + ' '
    csvline.append(whatsNew)

    figureCaptionTags = soup.find_all(attrs={"class": re.compile("fig-caption")})
    figCaptions = ""
    if not (figureCaptionTags is None):
        for elem in figureCaptionTags:
            figlabel = elem.find(attrs = {'class':'fig-label'})
            if not (figlabel is None):
                figCaptions += '<\>' + figlabel.text + '<\> '
            else:
                figCaptions += '<\>'
            paragraphs=elem.find_all('p')
            for paragraph in paragraphs:
                figCaptions += paragraph.text + ' '
    csvline.append(figCaptions)

    figureImageTags = soup.find_all(attrs={"class": re.compile("new-tab")})
    figLinks = ""
    if not (figureImageTags is None):
        for elem in figureImageTags:
            link=elem.find('a')
            figLinks += link.get('href') + ' '
    csvline.append(figLinks)

    numFigures = str(len(figureImageTags))
    csvline.append(numFigures)

    tableCaptionTags = soup.find_all(attrs={"class": re.compile("table-caption")})
    tableCaptions = ""
    if not (tableCaptionTags is None):
        for elem in tableCaptionTags:
            tablelabel = elem.find(attrs = {'class':'table-label'})
            if not (tablelabel is None):
                tableCaptions += '<\>' + tablelabel.text + '<\> '
            else:
                tableCaptions += '<\>'
            paragraphs=elem.find_all('p')
            for paragraph in paragraphs:
                tableCaptions += paragraph.text + ' '
    csvline.append(tableCaptions)

    tableLinkTags = soup.find_all(attrs={"class": re.compile("view-popup last")})
    tableLinks = ""
    if not (tableLinkTags is None):
        for elem in tableLinkTags:
            link=elem.find('a')
            tableLinks += 'https://tobaccocontrol.bmj.com' + link.get('href') + ' '
    csvline.append(tableLinks)

    numTables = str(len(tableLinkTags))
    csvline.append(numTables)

    if False: # show the results
        print('...journal title: ' + journalName)
        print('...paper title: ' + title)
        print('...paper type: ' + articleType)
        print("...author names: " + authornames)
        print("...author affiliations: " + authoraffiliations)
        print("...first page: " + firstpage)
        print("...last page: " + lastpage)
        print("...paper year: " + paperYear)
        print("...paper id: " + paperID)
        print("...paper doi: " + doi)
        print("...paper abstract: \n" + abstract)
        print("...what is new: " + whatsNew)
        print("...figure captions: " + figCaptions)
        print("...figure links: " + figLinks)
        print("...num of figures: " + numFigures)
        print("...table captions: " + tableCaptions)
        print("...figure links: " + tableLinks)
        print("...num of tables: " + numTables)

    # Note: use cs.writerow([a, abstract, b, c, etc]) to output as a single csv line

    writer.writerow(csvline)
    file.flush()


# %%
def getAuthorizedSession():
    # Function for accessing papers from OSU Off-Campus Login -- manually initiate this session for the first time
    # Access any paper with OSU proxy and get the following code from Chrome Developer tool
    # e.g., use https://tobaccocontrol-bmj-com.proxy.lib.ohio-state.edu/content/24/2/125
    # Check https://curl.trillworks.com/ for converting the bypass info from cURL to Python     

    proxy = os.getenv('_sn:2$_se:7$_ss:0$_st:1605189924124$vapi_domain:ohio-state.edu$ses_id:1605187919744%3Bexp-session$_pn:3%3Bexp-session')

    cookies = {
        'zabVisitId': '1611603508719zabv0.3191373679836651',
        'optimizelyEndUserId': 'oeu1604631622962r0.8979699495381592',
        'amplitude_id_9f6c0bb8b82021496164c672a7dc98d6_edmohio-state.edu': 'eyJkZXZpY2VJZCI6ImY3NzZiNWY3LTYxMTItNGYxOS1hOWJiLTY0NTU2NzE1YzQwZlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYwNDYzMTYyNDMyMywibGFzdEV2ZW50VGltZSI6MTYwNDYzMTYyNDMzMCwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MSwic2VxdWVuY2VOdW1iZXIiOjF9',
        'amplitude_id_408774472b1245a7df5814f20e7484d0ohio-state.edu': 'eyJkZXZpY2VJZCI6IjJjMTJhODgzLWM2NzUtNDQxNi1iZGNiLWZkNjY5NjJmZGE4NSIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjA0NjMxNjIzNjc4LCJsYXN0RXZlbnRUaW1lIjoxNjA0NjMxNjY2MzcwLCJldmVudElkIjoyLCJpZGVudGlmeUlkIjo0LCJzZXF1ZW5jZU51bWJlciI6Nn0=',
        '_rollupGA': 'GA1.2.459547342.1604631302',
        'zabUserId': '1604631682016zabu0.8835984226069582',
        's_fid': '3434826249D15B39-16C9B064FD45D3D8',
        'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1687686476%7CMCIDTS%7C18577%7CMCMID%7C39474372145734594052015963545670039167%7CMCAAMLH-1605792722%7C7%7CMCAAMB-1605792722%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1605195122s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0',
        'utag_main': f"v_id:0175b31cb65800017fef5cbed61c03073004e06b00bd0{proxy}",
        'has_js': '1',
        '_ga_0BJESHLY6P': 'GS1.1.1611337050.1.0.1611337051.0',
        '_gid': 'GA1.2.2069313241.1611586093',
        '_rollupGA_gid': 'GA1.2.1608026604.1611586093',
        'fcsid': '9uhuf1sdkc2hk14khnb3j6csf4',
        'ezproxy': 'oLeLtD9BYqzxxAv',
        'ezproxyl': 'oLeLtD9BYqzxxAv',
        'ezproxyn': 'oLeLtD9BYqzxxAv',
        '_ga_EXTSVLH45V': 'GS1.1.1611603499.9.1.1611603506.0',
        '_ga': 'GA1.2.459547342.1604631302',
        '_gat_UA-77367228-1': '1',
        '_gat_UA-5351042-23': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en',
    }

    response = requests.get('https://tobaccocontrol-bmj-com.proxy.lib.ohio-state.edu/content/24/2/125', headers=headers, cookies=cookies)

    return headers, cookies


# %%
def getAllArticleData(urls, writer, file, givenyear):
    
    print("Fetching data for " + str(len(urls)) + " articles")

    csvline = ['Journal Title', 'Paper Title', 'Paper Type','Author Names',
    'Author Affiliations', 'First Page', 'Last Page', 'Year', 'Paper ID', 
    'Paper DOI', 'Abstract', 'Highlights', 'Figure Captions', 'Figure Links',
    'Num of Figures', 'Table Captions', 'Table Links', 'Num of Tables']
    writer.writerow(csvline)

    for url in urls:
        if(url==''):
            continue

        #Getting the Paper ID out of the url
        articleID = url.split("content/")[1]

        getSingleArticleData(url, writer, file, articleID)

        # delay = random.randint(1,5)
        # print("Waiting for: " + str(delay) + " minutes")
        # time.sleep(60 * delay)

    
# %%

def main(args):

    url = ""

    # y = args
    # y=2016

    url = [ 'https://tobaccocontrol.bmj.com/content/24/Suppl_1',
            'https://tobaccocontrol.bmj.com/content/24/Suppl_2',
            'https://tobaccocontrol.bmj.com/content/24/Suppl_3',
            'https://tobaccocontrol.bmj.com/content/24/Suppl_4',
            'https://tobaccocontrol.bmj.com/content/25/1',
            'https://tobaccocontrol.bmj.com/content/25/2',
            'https://tobaccocontrol.bmj.com/content/25/e1',
            'https://tobaccocontrol.bmj.com/content/25/3',
            'https://tobaccocontrol.bmj.com/content/25/4',
            'https://tobaccocontrol.bmj.com/content/25/5',
            'https://tobaccocontrol.bmj.com/content/25/6',
            'https://tobaccocontrol.bmj.com/content/25/e2',
            'https://tobaccocontrol.bmj.com/content/25/Suppl_1',
            'https://tobaccocontrol.bmj.com/content/25/Suppl_2',
            'https://tobaccocontrol.bmj.com/content/26/1',
            'https://tobaccocontrol.bmj.com/content/26/2',
            'https://tobaccocontrol.bmj.com/content/26/e1',
            'https://tobaccocontrol.bmj.com/content/26/3',
            'https://tobaccocontrol.bmj.com/content/26/4',
            'https://tobaccocontrol.bmj.com/content/26/5',
            'https://tobaccocontrol.bmj.com/content/26/6',
            'https://tobaccocontrol.bmj.com/content/26/e2',
            'https://tobaccocontrol.bmj.com/content/27/1',
            'https://tobaccocontrol.bmj.com/content/27/2',
            'https://tobaccocontrol.bmj.com/content/27/3',
            'https://tobaccocontrol.bmj.com/content/27/4',
            'https://tobaccocontrol.bmj.com/content/27/e1',
            'https://tobaccocontrol.bmj.com/content/27/5',
            'https://tobaccocontrol.bmj.com/content/27/e2',
            'https://tobaccocontrol.bmj.com/content/27/6',
            'https://tobaccocontrol.bmj.com/content/27/Suppl_1',
            'https://tobaccocontrol.bmj.com/content/28/1',
            'https://tobaccocontrol.bmj.com/content/28/2',
            'https://tobaccocontrol.bmj.com/content/28/3',
            'https://tobaccocontrol.bmj.com/content/28/4',
            'https://tobaccocontrol.bmj.com/content/28/e1',
            'https://tobaccocontrol.bmj.com/content/28/5',
            'https://tobaccocontrol.bmj.com/content/28/6',
            'https://tobaccocontrol.bmj.com/content/28/e2',
            'https://tobaccocontrol.bmj.com/content/28/Suppl_1',
            'https://tobaccocontrol.bmj.com/content/28/Suppl_2',
            'https://tobaccocontrol.bmj.com/content/29/1',
            'https://tobaccocontrol.bmj.com/content/29/2',
            'https://tobaccocontrol.bmj.com/content/29/3',
            'https://tobaccocontrol.bmj.com/content/29/4',
            'https://tobaccocontrol.bmj.com/content/29/5',
            'https://tobaccocontrol.bmj.com/content/29/6',
            'https://tobaccocontrol.bmj.com/content/29/e1',
            'https://tobaccocontrol.bmj.com/content/29/Suppl_1',
            'https://tobaccocontrol.bmj.com/content/29/Suppl_2',
            'https://tobaccocontrol.bmj.com/content/29/Suppl_3',
            'https://tobaccocontrol.bmj.com/content/29/Suppl_4',
            'https://tobaccocontrol.bmj.com/content/29/Suppl_5']
   
    folder = '.\\TobaccoControl\\'
    articleURLs = []

    for u in url:
        
        issue = u.split('/')[-1]
        vol = u.split('/')[-2]
        if vol=='24':
            y=2015
        elif vol=='25':
            y=2016
        elif vol=='26':
            y=2017
        elif vol=='27':
            y=2018
        elif vol=='28':
            y=2019
        elif vol=='29':
            y=2020

        print("Looking for article urls in year %s issue %s" % (str(y), issue))
 
        articleURLs = getArticleURLs(u)
        fname = folder + 'articleURLs' + '_' + str(y) + '_' + issue + '.csv'
        if (not os.path.isfile(fname)):
            with open(fname, 'w', newline='',encoding='utf-8') as file:
                for article in articleURLs:
                    file.writelines(article+'\n')
        else:
            print('%s already exists' % fname)
        
        fname = folder + 'articleData' +  '_' + str(y) + '_' + issue + '.csv'

        if (not os.path.isfile(fname)):
            with open(fname,'w',newline='',encoding='utf-8') as file:
                writer = csv.writer(file) # , delimiter='\t'
                getAllArticleData(articleURLs, writer, file, str(y))
        else:
            print('%s already exists' % fname)

    print("Done Scraping")

    ############################################
    #uncomment for debugging a single article
    #file = open('test.csv', 'w',newline='',encoding='utf-8')
    #writer = csv.writer(file, delimiter='\t')
    #getSingleArticleData('https://tobaccocontrol.bmj.com/content/24/1/28',writer,file,"Conf","0000")
    ############################################
    
# %% For external call with arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Give the year you want to parse as a command line argument')
    parser.add_argument('year',type=int,help='give the year that you want to scrape as an integer. The year should be anywhere between 1990 and 2013 (both included).')
    args = parser.parse_args()
    main(args)


# %% Run the scraping here 
proxy_headers, proxy_cookies = getAuthorizedSession()
main(2015)


# %% Combine all the scraped data into one file
import pandas as pd

data_folder = '.\\TobaccoControl\\'
df_combined = pd.DataFrame() # create an empty dataframe for holding everything

i = 1
for fname in os.listdir(data_folder):
    if 'Data' in fname:
        print(i, fname)
        i += 1
        df = pd.read_csv(data_folder+fname, encoding='utf8') # read in the csv file as dataframe
        df_combined = df_combined.append(df) # for all other times; df.Append returns a new df

df_combined.to_csv('.\\CombinedData\\TobaccoControl_data_combined.csv')

# %%
