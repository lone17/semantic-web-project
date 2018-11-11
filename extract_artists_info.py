from utils import *
import pickle

sep = '##### NEW FILE #####\n'
error = []
site = 'zing'

if site == 'zing':
    files = ['zing/tieu_su_' + str(i) + '.txt' for i in range(3)]
elif site == 'nct':
    files = ['nct/tieu_su_' + str(i) + '.txt' for i in range(1)]

with open('tmp' + '.kb', 'rb') as f:
    kb = pickle.load(f)

for file in files:
    print('>>>', file)
    with open(file, 'r', encoding='utf8') as f:
        list_tieu_su = f.read().split(sep)[1:]

    for tieu_su in list_tieu_su:
        url, html = tieu_su.split('\n', 1)

        if url not in kb:
            continue

        try:
            name = kb[url]['name']
            professions = kb[url]['professions']
            instruments = kb[url]['instruments']
            # name = extract_artist_name(html, site)
            # text = extract_biography(html, site)
            # professions = extract_professions(text)
            # instruments = extract_instruments(text)

            # kb[url]['name'] = name
            # kb[url]['professions'].update(professions)
            # kb[url]['instruments'].update(instruments)

            print('url:', url)
            print('name:', name)
            print('professions:', professions)
            print('instruments:', instruments)
            print()
        except:
            error.append(url)

# with open(site + '.kb', 'wb') as f:
#     pickle.dump(kb, f)
