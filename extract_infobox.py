from utils import *

print('running ...')
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
        if line.startswith('https://vi.wikipedia.org/wiki/'):
            subject = line.replace('https://vi.wikipedia.org/wiki/', '').replace('_', ' ')
            subject = re.sub('\([^)]*\)', '', subject).strip().lower()
            try:
                idx = entities_lower.index(subject)
            except ValueError:
                continue
            if cur:
                # soup = BeautifulSoup(html, features='lxml')
                # name = soup.select(css_selector)[0].text
                tmp = {'name': entities[idx], 'infobox': html}
                if cur in info:
                    tmp['url'] = line
                    error.append(tmp)
                else:
                    info[line] = tmp
                    print(line)
            cur = line
            html = ''
        else:
            html += line

with open('wiki.kb', 'wb') as f:
    pickle.dump(info, f)
