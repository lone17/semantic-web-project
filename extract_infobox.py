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
    cur_html = ''
    cur_url = None
    for line in f:
        if line.startswith('https://vi.wikipedia.org/wiki/'):
            line = line.strip()
            flag = True
            if cur_url:
                if len(cur_notion) > 0:
                    flag = False
                    for s in notions:
                        if s in cur_notion[0]:
                            flag = True
                            break
                if flag:
                    try:
                        idx = entities_lower.index(cur_subject)
                        tmp = {'name': entities[idx], 'infobox': cur_html}
                        if cur_url in info:
                            tmp['url'] = cur_url
                            error.append(tmp)
                        else:
                            info[cur_url] = tmp
                            print(cur_url)
                    except ValueError:
                        pass
            cur_url = line
            cur_html = ''
            line = line.replace('https://vi.wikipedia.org/wiki/', '').replace('_', ' ').lower()
            cur_subject = re.sub('\([^)]*\)', '', line).strip()
            cur_notion = re.findall('(?<=\().*(?=\))', line)
        else:
            cur_html += line

with open('wiki.kb', 'wb') as f:
    pickle.dump(info, f)
