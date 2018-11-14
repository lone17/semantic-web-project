from utils import *
import pickle
import traceback
import os
from datetime import datetime

sep = '##### NEW FILE #####\n'
site = 'zing'

if site == 'zing':
    files = ['zing/songs_' + str(i) + '.txt' for i in range(52)]
elif site == 'nct':
    files = ['nct/songs_' + str(i) + '.txt' for i in range(15)]

# kb_file = site + '_songs.kb'
kb_file = 'tmp.kb'
if os.path.exists(kb_file):
    with open(kb_file, 'rb') as f:
        kb = pickle.load(f)
else:
    kb = {}

if os.path.exists('error.pickle'):
    with open('error.pickle', 'rb') as f:
        error = pickle.load(f)
else:
    error = []

for file in files:
    print(datetime.now())
    print('>>>', file)
    with open(file, 'r', encoding='utf8') as f:
        pages = f.read().split(sep)[1:]

    for page in pages:
        url, html = page.split('\n', 1)

        if error_404 in html:
            continue

        kb[url] = {}

        try:
            name = extract_song_name(html, site)
            performers = extract_performers(html, site)
            composers = extract_composers(html, site)
            lyric = extract_lyric(html, site)

            kb[url]['name'] = name
            kb[url]['performed_by'] = performers
            kb[url]['composed_by'] = composers
            kb[url]['lyric'] = lyric

            # print('#'*80)
            # print('url:', url)
            # print('name:', name)
            # print('performers:', performers)
            # print('composers:', composers)
            # print('lyric:')
            # print(lyric[:100])
            # print()
        except Exception as e:
            error.append(url)

    with open(kb_file, 'wb') as f:
        pickle.dump(kb, f)

    with open('error.pickle', 'wb') as f:
        pickle.dump(error, f)
