# %%
import os
from os import listdir
import wand.image as wandImage

# do the following line to disable the authorize-policy
#
# /etc/ImageMagick-6$ sudo mv policy.xml policy.xml.off
#
# restore back if need

# %%
pdf_path = '~/papers/CHI'
outpath = 'converted_images'

# p=0
for issue in listdir(pdf_path):

    print(issue)
    if issue != '2020':
        continue

    issue_path = '%s/%s' % (pdf_path, issue)

    img_outpath = '%s/CHI/%s' % (outpath,issue)
    if not os.path.exists(img_outpath):
        os.makedirs(img_outpath, exist_ok=True)

    cnt = 0
    for paper in listdir(issue_path):
        if not paper.endswith(".pdf"): 
            continue
        if paper.startswith('._'):  # the hidden files
            continue
        # if issue=='2016' and cnt==269:
        #     cnt += 1
        #     continue

        paper_path = '%s/%s' % (issue_path, paper)
        print(cnt, paper)

        # default resolution is 72
        with wandImage.Image(filename = paper_path, resolution=150) as pdf:
            pdfimage = pdf.convert("jpg")
            i=0
            for img in pdfimage.sequence:
                img.alpha_channel = 'remove'
                img.background_color = wandImage.Color('white')
                page = wandImage.Image(image=img)
                i+=1
                pagename = paper.replace('.pdf','') + '_%02d.jpg' % i
                page.save(filename = '%s/%s' % (img_outpath, pagename))

        cnt += 1


# %%
