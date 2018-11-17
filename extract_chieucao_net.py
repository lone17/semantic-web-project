from underthesea import pos_tag
from bs4 import BeautifulSoup
import requests
import re

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

def get_context(text, pattern, span):
    lower_text = text.lower()
    matches = re.findall(pattern, lower_text)

    contexts = []
    for match in matches:
        left, right = text.split(match, 1)
        context = left.splt()[-span[0]:] + [match] + right.split()[:span[1]]
        contexts.append(' '.join(context))

    return contexts

def extract_first_named_entity(context):
    tags = pos_tag(context)
    entity = []
    for i in range(len(tags)):
        if tags[i][1] == 'Np':
            entity.append(tags[i][0])
            for j in range(i+1, len(tags)):
                if tags[j][1] != 'Np':
                    break
                entity.append(tags[j][0])
            return ' '.join(entity)

def extract_height(text):
    context = text

    pattern = '1\s{0,2}m\s{0,2}\d{1,2}|1\d\d\s{0,2}cm|1[\.,]\d{1,2}\s{0,2}m|1\d\d[,\.]\d?\s{0,2}cm'
    height = re.findall(pattern, context)
    height = [int(re.sub('\s|m|,|\.|c', '', s)) for s in height]
    height = [h if h >= 100 else h*10 for h in height]
    height = [h if h < 1000 else h/10 for h in height]

    return height

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

kb = {}
for path, html in zip(paths, pages):
    title = extract_title(html)
    entity = extract_first_named_entity(title)

    if entity not in kb:
        kb[entity] = {'height': set(), 'articles': []}

    content = extract_content(html)
    kb[entity]['height'].update(extract_height(content))
    kb[entity]['articles'].append(path)

multi = {k: v for k, v in kb.items() if len(v['height']) > 1}
print(len(multi))
uni = {k: v for k, v in kb.items() if len(v['height']) == 1}
print(len(uni))

# heights = [extract_height(extract_content(html)) for html in pages]
# print(len(heights))
# multiple = [h for h in heights if len(set(h)) > 1]
# print(len(multiple))
# single = [h for h in heights if len(set(h)) == 1]
# print(len(single))
