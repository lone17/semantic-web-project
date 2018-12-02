from underthesea import pos_tag
from bs4 import BeautifulSoup
import requests
import pickle
from utils import *

sep = '##### NEW FILE #####\n'

def get_pages():
    files = ['chieu-cao.net/category/nhac-sy.html', 'chieu-cao.net/category/ca-sy.html']
    files += ['chieu-cao.net/category/ca-sy/page/' + str(i) + '.html' for i in range(2, 27)]

    css_selector = 'article > header > h2 > a'
    pages = []
    for file in files:
        with open(file, 'r', encoding='utf8') as f:
            html = f.read()
        soup = BeautifulSoup(html, features='lxml')
        pages += [a.get('href').replace('https://', '') for a in soup.select(css_selector)]

    return pages

def extract_title(html):
    soup = BeautifulSoup(html, features='lxml')
    css_selector = 'article > header > h1'
    header = soup.select(css_selector)[0].text

    return header

def extract_content(html):
    soup = BeautifulSoup(html, features='lxml')
    css_selector = 'article > div'
    content = soup.select(css_selector)[0].text

    return content

def test(html):
    print('#'*80)
    header = extract_title(html)
    print(header)
    entity = extract_first_named_entity(header)
    print(entity)
    content = extract_content(html)
    height = extract_height(content)
    print(height)
    # print(content)

with open('chieucao_pages.txt', 'r', encoding='utf8') as f:
    pages = f.read().split(sep)[1:]
with open('files_chieucao_net.txt', 'r') as f:
    paths = f.read().split('\n')

# kb = {}
# for path, html in zip(paths, pages):
#     title = extract_title(html)
#     entity = extract_first_named_entity(title)
#
#     if entity not in kb:
#         kb[entity] = {'height': set(), 'articles': []}
#
#     content = extract_content(html)
#     kb[entity]['height'].update(extract_height(content))
#     kb[entity]['articles'].append(path)
#
# multi = {k: v for k, v in kb.items() if len(v['height']) > 1}
# print(len(multi))
# uni = {k: v for k, v in kb.items() if len(v['height']) == 1}
# print(len(uni))

# heights = [extract_height(extract_content(html)) for html in pages]
# print(len(heights))
# multiple = [h for h in heights if len(set(h)) > 1]
# print(len(multiple))
# single = [h for h in heights if len(set(h)) == 1]
# print(len(single))

with open('chieucao.kb', 'rb') as f:
    kb = pickle.load(f)

error = []
for k in kb.keys():
    if 'city' not in kb[k]:
        kb[k]['city'] = set()
    if 'professions' not in kb[k]:
        kb[k]['professions'] =  set()
    for article in kb[k]['articles']:
        if article in paths[:7]:
            kb[k]['professions'].add('nhạc sỹ')
        else:
            kb[k]['professions'].add('ca sỹ')

        try:
            html = pages[paths.index(article)]
            content = extract_content(html)
            city = extract_city(content)
            if city:
                kb[k]['city'].add(city)
        except Exception:
            error.append(article)
    print(k)
    print(kb[k]['city'])

# with open('chieucao.kb', 'wb') as f:
#     kb = pickle.dump(kb ,f)
