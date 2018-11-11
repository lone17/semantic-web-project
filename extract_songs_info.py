from utils import *
import pickle
import traceback
import os

sep = '##### NEW FILE #####\n'
site = 'nct'

if site == 'zing':
    files = ['zing/songs_' + str(i) + '.txt' for i in range(52)]
elif site == 'nct':
    files = ['nct/songs_' + str(i) + '.txt' for i in range(15)]

with open(site + '_songs.kb', 'rb') as f:
    kb = pickle.load(f)

if os.path.exists('error.pickle'):
    with open('error.pickle', 'rb') as f:
        error = pickle.load(f)
else:
    error = {}

for file in files:
    print('>>>', file)
    with open(file, 'r', encoding='utf8') as f:
        pages = f.read().split(sep)[1:]

    for page in pages:
        url, html = page.split('\n', 1)

        if url not in kb:
            continue

        try:
            name = extract_song_name(html, site)
            performers = extract_performers(html, site)
            composers = extract_composers(html, site)
            lyric = extract_lyric(html, site)

            kb[url]['name'] = name
            kb[url]['performed_by'] = performers
            kb[url]['composed_by'] = composers
            kb[url]['lyric'] = lyric

            print('#'*80)
            print('url:', url)
            print('name:', name)
            print('performers:', performers)
            print('composers:', composers)
            print('lyric:')
            print(lyric[:100])
            print()
        except Exception as e:
            error[url] = e.__traceback__

with open(site + '_songs.kb', 'wb') as f:
    pickle.dump(kb, f)

with open('error.pickle', 'wb') as f:
    pickle.dump(error, f)
