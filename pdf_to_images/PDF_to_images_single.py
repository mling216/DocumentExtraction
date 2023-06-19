# %%
import os
from os import listdir
import wand.image as wandImage


# %%
pdf_path = '~/papers/CHI/2016/p3683-gupta.pdf'
outpath = 'single'

with wandImage.Image(filename = pdf_path) as pdf:
    paper = pdf_path.split('/')[-1]
    print(paper)
    pdfimage = pdf.convert("jpg")
    i=0
    for img in pdfimage.sequence:
        img.alpha_channel = 'remove'
        img.background_color = wandImage.Color('white')
        page = wandImage.Image(image=img)
        i+=1
        pagename = paper.replace('.pdf','') + '_%02d.jpg' % i
        page.save(filename = '%s/%s' % (outpath, pagename))


# %%
