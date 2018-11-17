from utils import *
import pickle

notions = ['ca sĩ', 'ca sỹ', 'nghệ sĩ', 'nghệ sỹ', 'nhạc sĩ', 'nhạc sỹ', 'tỉnh',
           'thành phố', 'nhóm nhạc', 'band', 'ban nhạc']

with open('artist_name.txt', 'r', encoding='utf8') as f:
    names = f.read().split('\n')

entities = [s for s in names + cities]
entities_lower = [s.lower() for s in entities]

# css_selector = 'tbody > tr:nth-of-type(1) > th'
info = {}
error = []
with open('infoboxalldump', 'r', encoding='utf8') as f:
    html = ''
    cur = None
    for line in f:
        line = line.strip()
        if line.startswith('https://vi.wikipedia.org/wiki/'):
            if cur:
                flag = False
                if len(notion) > 0:
                    for s in notions:
                        if notion[0] in s:
                            flag = True
                            break
                    if not flag:
                        continue
                try:
                    idx = entities_lower.index(subject)
                except ValueError:
                    continue
                tmp = {'name': entities[idx], 'infobox': html}
                if cur in info:
                    tmp['url'] = line
                    error.append(tmp)
                else:
                    info[line] = tmp
                    print(line)
                    cur = line
                    html = ''
            line = line.replace('https://vi.wikipedia.org/wiki/', '').replace('_', ' ').lower()
            subject = re.sub('\([^)]*\)', '', line).strip()
            notion = re.findall('(?<=\().*(?=\))', line)
        else:
            html += line

with open('wiki.kb', 'wb') as f:
    pickle.dump(info, f)
