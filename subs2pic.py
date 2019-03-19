import pandas as pd
import numpy as np
import shutil
import requests
from PIL import Image
from os.path import isfile, join

print("Reding emails from emails.csv file")
emails = pd.read_csv("./emails.csv")
emails["domain"] = emails["email"].apply(lambda x: x.split('@')[1].lower())
print("Number of emails: {}".format(emails.shape[0]))
print("Number of unique domains: {}".format(len(np.unique(emails["domain"]))))

# Get list of free mail domains
free_email_domains = ""
with open("./20_freemail_domains.cf", "r") as fin:
    free_email_domains = fin.read()
# Filter free / work emails
domains = np.unique(emails["domain"])
work_domains = []
for d in domains:
    # ugly check
    if not d.split('.')[0] in free_email_domains:
        work_domains += [d]
print("Number of work domains: {}".format(len(work_domains)))
print("Download logos with ClearBit free logo API ...")
for d in work_domains:
    if not isfile("imgs/{}.png".format(d)):
        url = 'https://logo.clearbit.com/{}?size=128'.format(d)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open('imgs/{}.png'.format(d), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        del response
# Get list of logo images
logo_files = []
for d in work_domains:
    if isfile("imgs/{}.png".format(d)):
        logo_files += ["imgs/{}.png".format(d)]
# Create big picture of subscribers
images = map(Image.open, logo_files)
imgs_row = 15 # logos per row
imgs_col = int(np.ceil(len(logo_files)/imgs_row)) # logos per column
total_width = 128*imgs_row
max_height = 128*imgs_col
new_im = Image.new('RGB', (total_width, max_height), color=(255,255,255,0))
x_offset = 0
y_offset = 0
cnt = 0
for im in images:
    new_im.paste(im, (x_offset,y_offset))
    x_offset += 128
    cnt += 1
    if cnt > imgs_row:
        y_offset += 128
        x_offset = 0
        cnt = 0
new_im.save('./subscribers_big_picture.jpg')
