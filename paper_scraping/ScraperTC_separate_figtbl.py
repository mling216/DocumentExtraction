# %% ####################################################################################
# This section is to separate figures and tables from each paper into a figtbl_datafile.
# Figures are downloaded during parsing
# Tables are in html link (markup), which are converted to PDF then image in the next section
#

import os
import csv
import pandas as pd
from PIL import Image
import wget

# %% read in the paper data with fig/tbl information
inputDataFile = '.\\CombinedData\\paperData_w_figtbl.csv'
full_data = pd.read_csv(inputDataFile)
    # full_data = main_data.iloc[:, 1:] # if need to drop the first column
full_data.head(5)

# %% 
# Create the figure/table datafile for AWS 

# create an empty dataframe and append the header line
outputDataFile = '.\\CombinedData\\figtblData.csv'
imgdownloadFolder = '.\\CombinedData\\images_downloaded\\'

if not os.path.isfile(outputDataFile):
    outputnotyet = True
else:
    outputnotyet = False

# loop through each paper, extract fig/tbl captions and links, and output the data file
with open(outputDataFile,'a+',newline='',encoding='utf-8') as file:
    writer = csv.writer(file)

    csvline = ['Conference','PaperType','FirstPage','filename','paperImageName','sizeW','sizeH',
    'image_proportion','left','top','right','bottom','vis_type','caption_index','Year','pageNum',
    'Paper DOI','thumb_url','url','cap_url','Paper type','Paper Title','Author','Keywords Author',
    'paper_url','Paper FirstPage','Paper LastPage','rank','imageID']
    if outputnotyet:
        writer.writerow(csvline)

    # figtbl_data.append(csvline)
    # figtbl_data.to_csv('.\\CombinedData\\test.csv')

    # Iterate through full_data and extract figures and tables into separate rows
    for index, row in full_data.iterrows():
        
        numFig = int(row['Num of Figures'])
        numTbl = int(row['Num of Tables'])
        numFigTbl = numFig + numTbl

        if numFigTbl > 0:
        ######## point to resume
            if index >= 1131: 
                print(index,numFig,numTbl)
            else:
                continue

            # parse the fig/tbl captions and image links
            captions = []
            imgURLs = []
            imgNames = []
            imgSizes = []
            visTypes = []
            if numFig > 0:
                # print(row['Figure Captions'])
                figCaps = row['Figure Captions'].split('<\>')
                # print(figCaps)
                figLinks = row['Figure Links'].split(' ')
                for i in range(numFig):
                    if 'Figure' in row['Figure Captions']:
                        captions.append(figCaps[i*2+1].replace('\xa0',' ') + figCaps[i*2+2])
                    else:
                        if (i+1)>=len(figCaps):
                            captions.append('')
                        else:
                            captions.append(figCaps[i+1])
                    imgURLs.append(figLinks[i])
                    imgName = wget.download(figLinks[i],out=imgdownloadFolder)
                    imgNames.append(imgName.split('/')[1])
                    with Image.open(imgName) as im:
                        width, height = im.size
                    imgSizes.append([width,height])
                    visTypes.append('100') # 100 for figures
            if numTbl > 0:
                tblCaps = row['Table Captions'].split('<\>')
                tblLinks = row['Table Links'].split(' ')
                for i in range(numTbl):
                    if 'Table' in row['Table Captions']:
                        if (i*2+1)>=len(tblCaps):
                            captions.append('')
                        else:
                            captions.append(tblCaps[i*2+1].replace('\xa0',' ') + tblCaps[i*2+2])
                    else:
                        if (i+1)>=len(tblCaps):
                            captions.append('')
                        else:
                            captions.append(tblCaps[i+1])
                    if i >= len(tblLinks):
                        imgURLs.append('')
                    else:
                        imgURLs.append(tblLinks[i]) ### this may change later
                    imgName = '.'.join(['TC', str(row['Year']), row['FirstPage'], 
                                        tblLinks[i].split('markup/')[1].split('/')[0]])
                    imgNames.append(imgName)
                    imgSizes.append([600,300])
                    visTypes.append('16') # 16 for tables

            for i in range(numFigTbl):
                csvline = []
                csvline.append(row['Conference'])
                csvline.append(row['PaperType'])
                csvline.append(row['FirstPage'])
                csvline.append(imgNames[i]) # filename
                csvline.append('') # paperImageName
                csvline.append(imgSizes[i][0]) # sizeW
                csvline.append(imgSizes[i][1]) # sizeH
                csvline.append(0.1) # image_proportion
                csvline.append(0) # left
                csvline.append(0) # top
                csvline.append(0) # right
                csvline.append(0) # bottom
                csvline.append(visTypes[i]) # vis_type
                csvline.append('') # caption_index
                csvline.append(row['Year'])
                csvline.append('') # pageNum
                csvline.append(row['DOI']) # Paper DOI
                csvline.append('') # thumb_url
                csvline.append(imgURLs[i]) # url
                csvline.append(captions[i]) # cap_url
                csvline.append(row['PaperType']) # Paper type
                csvline.append(row['Title']) # Paper Title
                authorNames = row['AuthorNames']
                if pd.isnull(authorNames):
                    authorNames = ''
                else:
                    authorNames = authorNames[0:len(authorNames)-2]
                csvline.append(authorNames) # Author
                csvline.append('nan') # Keywords
                csvline.append(row['Link']) # paper_url
                csvline.append(row['FirstPage']) # Paper FirstPage
                csvline.append(row['LastPage']) # Paper LastPage
                csvline.append(row['Index']) # rank
                csvline.append('i'+str(row['Index'])+'Y'+str(row['Year'])) # imageID

                writer.writerow(csvline)
                # print(csvline)


# %% ####################################################################################
# Get tables from online markup language and convert to PDF
#
figtblDataFile = '.\\CombinedData\\figtblData.csv'
figtbl_data = pd.read_csv(figtblDataFile)
    # full_data = main_data.iloc[:, 1:] # if need to drop the first column
figtbl_data.head(5)

# %% iterate and grab all tables
import pdfkit
tbldownloadFolder = '.\\CombinedData\\tables_downloaded\\'

for index, row in figtbl_data.iterrows():
    print(index, row['vis_type'])
    if index<10000:
        continue
    if row['vis_type'] == 16:
        pdfkit.from_url(row['url'], tbldownloadFolder+row['filename']+'.pdf')


# %% ####################################################################################
# Update fig/tbl data file to point to AWS links
#
figtblDataFileUpdate = '.\\CombinedData\\figtblDataAWS.csv'
AWS_image_path = 'https://tobaccoresearch.s3.us-east-2.amazonaws.com/images/'
AWS_thumbnail_path = 'https://tobaccoresearch.s3.us-east-2.amazonaws.com/images_thumnails/'
tblimgFolder = '.\\CombinedData\\tables_images_tight\\'
tbl_append_df = pd.DataFrame()

figtblDataFile = '.\\CombinedData\\figtblData.csv'
figtbl_data = pd.read_csv(figtblDataFile,encoding='utf-8')
figtbl_data['url'].fillna('', inplace=True) # convert NaN to ''
figtbl_data['thumb_url'].fillna('', inplace=True)
figtbl_data['vis_type'] = figtbl_data['vis_type'].astype('Int64') # convert to integer
figtbl_data['rank'] = figtbl_data['rank'].astype('Int64') # convert to integer

# display more 
pd.set_option('display.max_columns', 30)
original_rank = len(figtbl_data)
new_rank = 0
print(original_rank)

for index, row in figtbl_data.iterrows():
    
    print(index, row['vis_type'])
    if index>100000:
        break

    if row['vis_type'] == 16:   # tables
        fnameprefix = row['filename']
        fname = fnameprefix + '_1.png'
        print('table,',fname)
        figtbl_data.at[index, 'filename'] = fname
        figtbl_data.at[index, 'url'] = AWS_image_path + fname
        figtbl_data.at[index, 'thumb_url'] = AWS_thumbnail_path + fname
        with Image.open(tblimgFolder+fname) as im:
            width, height = im.size
        figtbl_data.at[index, 'sizeW'] = width
        figtbl_data.at[index, 'sizeH'] = height

        more_pages = True
        i = 2
        while more_pages:
            fname = fnameprefix + '_' + str(i) + '.png'
            if os.path.isfile(tblimgFolder+fname):
                new_rank += 1
                print('page no. ', i)
                # must assign back
                tbl_append_df = tbl_append_df.append(figtbl_data.iloc[index])
                tbl_append_df.reset_index(drop=True, inplace=True)
                cur_row = len(tbl_append_df.index) - 1
                tbl_append_df.at[cur_row, 'filename'] = fname
                tbl_append_df.at[cur_row,'url'] = AWS_image_path + fname
                tbl_append_df.at[cur_row,'thumb_url'] = AWS_thumbnail_path + fname
                with Image.open(tblimgFolder+fname) as im:
                    width, height = im.size
                tbl_append_df.at[cur_row, 'sizeW'] = width
                tbl_append_df.at[cur_row, 'sizeH'] = height
                updated_rank = original_rank + new_rank
                tbl_append_df.at[cur_row, 'rank'] = updated_rank
                tbl_append_df.at[cur_row, 'imageID'] = 'I' + str(updated_rank) + 'Y' + str(tbl_append_df.at[cur_row, 'Year'])
                i = i + 1
            else:
                more_pages = False

    else:   # figures
        fname = row['filename']
        figtbl_data.at[index, 'url'] = AWS_image_path + fname
        figtbl_data.at[index, 'thumb_url'] = AWS_thumbnail_path + fname
        print(figtbl_data.at[index, 'sizeW'], figtbl_data.at[index, 'sizeH'])

# tbl_append_df.head(5)
figtbl_data = figtbl_data.append(tbl_append_df)
figtbl_data.reset_index(drop=True, inplace=True)
figtbl_data['vis_type'] = figtbl_data['vis_type'].astype('Int64') # convert to integer
figtbl_data['sizeW'] = figtbl_data['sizeW'].astype('Int64') # convert to integer
figtbl_data['sizeH'] = figtbl_data['sizeH'].astype('Int64') # convert to integer
figtbl_data['rank'] = figtbl_data['rank'].astype('Int64') # convert to integer

column_order = ['Conference','PaperType','FirstPage','filename','paperImageName','sizeW','sizeH',
'image_proportion','left','top','right','bottom','vis_type','caption_index','Year','pageNum',
'Paper DOI','thumb_url','url','cap_url','Paper type','Paper Title','Author','Keywords Author',
'paper_url','Paper FirstPage','Paper LastPage','rank','imageID']

# figtbl_data[column_order].to_csv('check.csv',encoding='utf-8')
figtbl_data[column_order].to_csv(figtblDataFileUpdate,encoding='utf-8')
print(len(figtbl_data), 'done!')
