import requests
from bs4 import BeautifulSoup

genres = ['country', 'christian', 'gospel', 'pop', 'audiophile', 'cải lương',
          'classical', 'rock', 'indie', 'folk', 'electronic', 'dance', 'rap',
          'hip-hop', 'blues', 'jazz', 'trance', 'house', 'techno', 'r&b', 'soul',
          'quan họ', 'instrumental', 'opera', 'edm', 'dubstep', 'acappella',
          'reggae', 'disco', 'orchestra', 'beatbox', 'ballad', 'bolero', 'funk',
          'tuồng']

other_genres = ['nhạc trữ tình', 'nhạc trịnh', 'nhạc cách mạng',
                'new age', 'world music', 'bossa nova', 'nhạc vàng']

convert_genres = {'nhạc trẻ': 'pop', 'nhạc không lời': 'instrumental',
                  'new age': 'instrumental', 'world music': 'instrumental',
                  'hip hop': 'hip-hop', 'electro': 'electronic', 'metal': 'rock',
                  'orchestra': 'instrumental', ' dj ': 'edm', 'deejay': 'edm',
                  'nhạc thiếu nhi': "children's music", 'trữ tình': 'nhạc trữ tình',
                  'nhạc quê hương': 'nhạc dân ca - quê hương', 'boléro': 'bolero',
                  'dân ca': 'nhạc dân ca - quê hương', 'hoà tấu': 'instrumental',
                  'hòa tấu': 'instrumental', 'balad': 'ballad'}

instruments = ['cello', 'violin', 'piano', 'guitar', 'saxophone', 'banjo',
               'clarinet', ' cornet', 'drum', 'flute', 'organ', 'trombone',
               'xylophone', 'harmonica', 'kèn bầu', 'đàn bầu', 'đàn nguyệt',
                'đàn tranh', 'ukulele', 'keyboard', 'contrabass']

other_instruments = ['nhạc cụ dân tộc', 'đàn gáo', 'đàn tam thập lục', 'đàn tỳ bà',
                     ]

convert_instruments = {'vi ô lông': 'violin', 'vi-ô-lông': 'violin',
                       'vĩ cầm': 'violin', 'xen-lô': 'cello',
                       'dương cầm': 'piano', 'ghi ta': 'guitar', 'sáo': 'flute',
                       'công tra bát': 'contrabass', 'công-tra-bát': 'contrabass',
                       'một trống': 'drum', 'đánh trống': 'drum',
                       'học trống': 'drum', 'chơi trống': 'drum',
                       'tay trống': 'drum', 'và trống': 'drum',
                       'một bass': 'guitar', 'chơi bass': 'guitar',
                       'tay bass': 'guitar', 'và bass': 'guitar'}

genres += other_genres
instruments += other_instruments

def extract_name(html, site):
    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.full-banner > div > div > div > div > div > h1'
    elif site == 'nct':
        css_selector = 'body > div.singer-top-cover > div.wrap > div > div.singer-left-avatar > h1.singer-name'

    soup = BeautifulSoup(html, features='lxml')
    name = soup.select(css_selector)[0].text

    return name

def extract_tieu_su(html, site):
    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div'
    elif site == 'nct':
        css_selector = '#divDescription'

    soup = BeautifulSoup(html, features='lxml')
    try:
        text = soup.select(css_selector)[0].text
    except IndexError:
        if site == 'zing':
            css_selector = 'body > div.wrapper-page > div.full-banner > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div'
        try:
            text = soup.select(css_selector)[0].text
        except IndexError:
            if site == 'zing':
                css_selector = 'body > div.wrapper-page > div > div.container > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content'
            text = soup.select(css_selector)[0].text

    return text

def extract_professions(text):
    text = text.lower()
    ret = []
    for g in genres:
        if g in text:
            ret.append(g)
    for g in convert_genres.keys():
        if g in text:
            ret.append(convert_genres[g])

    return ret

def extract_instruments(text):
    text = text.lower()
    ret = []
    for i in instruments:
        if i in text:
            ret.append(i)
    for i in convert_instruments.keys():
        if i in text:
            ret.append(convert_instruments[i])

    return ret

# url = 'https://mp3.zing.vn/nghe-si/Son-Tung-M-TP/tieu-su'
# url = 'https://www.nhaccuatui.com/nghe-si-son-tung-mtp.html'
# def test(url):
#     if 'https://mp3.zing.vn' in url:
#         site = 'zing'
#     elif 'https://www.nhaccuatui.com' in url:
#         site = 'nct'
#
#     req = requests.get(url)
#     html = req.text
#     text = extract_tieu_su(html, site)
#     print(extract_name(html, site))
#     print(extract_professions(text))
#     print(extract_instruments(text))
