import requests
from bs4 import BeautifulSoup

error_404 = '<p class="title-404">Không tìm thấy trang mà bạn yêu cầu</p>'
zing_video_indicator = 'class="wrap-body group page-play-song container playing-video"'

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

cities = ['An Giang', 'Bà Rịa - Vũng Tàu', 'Bắc Giang', 'Bắc Kạn', 'Bạc Liêu',
         'Bắc Ninh', 'Bến Tre', 'Bình Định', 'Bình Dương', 'Bình Phước',
         'Bình Thuận', 'Cà Mau', 'Cao Bằng', 'Đắk Lắk', 'Đắk Nông', 'Điện Biên',
         'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Giang', 'Hà Nam', 'Hà Tĩnh',
         'Hải Dương', 'Hậu Giang', 'Hòa Bình', 'Hưng Yên', 'Khánh Hòa',
         'Kiên Giang', 'Kon Tum', 'Lai Châu', 'Lâm Đồng', 'Lạng Sơn', 'Lào Cai',
         'Long An', 'Nam Định', 'Nghệ An', 'Ninh Bình', 'Ninh Thuận', 'Phú Thọ',
         'Quảng Bình', 'Quảng Nam', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị',
         'Sóc Trăng', 'Sơn La', 'Tây Ninh', 'Thái Bình', 'Thái Nguyên',
         'Thanh Hóa', 'Thừa Thiên Huế', 'Tiền Giang', 'Trà Vinh', 'Tuyên Quang',
         'Vĩnh Long', 'Vĩnh Phúc', 'Yên Bái', 'Phú Yên', 'Cần Thơ', 'Đà Nẵng',
         'Hải Phòng', 'Hà Nội', 'TP Hồ Chí Minh']
genres += other_genres
instruments += other_instruments

def extract_artist_name(html, site):
    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.full-banner > div > div > div > div > div > h1'
    elif site == 'nct':
        css_selector = 'body > div.singer-top-cover > div.wrap > div > div.singer-left-avatar > h1.singer-name'
    name = soup.select(css_selector)[0].text

    return name

def extract_biography(html, site):
    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div'
    elif site == 'nct':
        css_selector = '#divDescription'
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

def extract_song_name(html, site):
    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.wrap-body.group.page-play-song.container.playing-song > div.info-top-play.group.mb7 > div.info-content.otr.mb7 > div.pull-left > h1.txt-primary'
        if zing_video_indicator in html:
            css_selector = css_selector.replace('playing-song', 'playing-video')
    elif site == 'nct':
        css_selector = '#box_playing_id > div.info_name_songmv > div.name_title > h1'

    if site == 'zing':
        name = soup.select(css_selector)[0].text.strip().split('\n')[0]
    elif site == 'nct':
        name = soup.select(css_selector)[0].text

    return name.strip()

def extract_lyric(html, site):
    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = '#lyrics > div.fn-container > div:nth-of-type(1) > p'
    elif site == 'nct':
        css_selector = '#divLyric'
    lyric = soup.select(css_selector)[0].text

    return lyric.strip()

def extract_performers(html, site):
    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = 'body > div.wrapper-page > div.wrap-body.group.page-play-song.container.playing-song > div.info-top-play.group.mb7 > div.info-content.otr.mb7 > div.pull-left > h1 > div > h2 > a'
        if zing_video_indicator in html:
            css_selector = css_selector.replace('playing-song', 'playing-video')
    elif site == 'nct':
        css_selector = '#box_playing_id > div.info_name_songmv > div.name_title > h2 > a'

    if site == 'zing':
        ret = ['https://mp3.zing.vn' + a.get('href') + '/tieu_su'
               for a in soup.select(css_selector)]
    elif site == 'nct':
        ret = [a.get('href') if 'tim-kiem' not in a.get('href') else a.text
               for a in soup.select(css_selector)]

    return ret

def extract_composers(html, site):
    soup = BeautifulSoup(html, features='lxml')
    ret = []

    if site == 'zing':
        css_selector = '#composer-container > h2'
    elif site == 'nct':
        css_selector = '#_divLyricHtml > div.pd_name_lyric > p'

    if site == 'zing':
        ret = [h2.text.strip() for h2 in soup.select(css_selector)]
    elif site == 'nct':
        for p in soup.select(css_selector):
            if 'Nhạc sĩ:' in p.text:
                ret = [s.strip() for s in p.text.replace('Nhạc sĩ:', '').split(',')]

    return ret

# url = 'https://mp3.zing.vn/nghe-si/Son-Tung-M-TP/tieu-su'
# url = 'https://www.nhaccuatui.com/nghe-si-son-tung-mtp.html'
# def test_artist(url):
#     if 'https://mp3.zing.vn' in url:
#         site = 'zing'
#     elif 'https://www.nhaccuatui.com' in url:
#         site = 'nct'
#
#     req = requests.get(url)
#     html = req.text
#     text = extract_biography(html, site)
#     print(extract_name(html, site))
#     print(extract_professions(text))
#     print(extract_instruments(text))

def test_song(url):
    if 'https://mp3.zing.vn' in url:
        site = 'zing'
    elif 'https://www.nhaccuatui.com' in url:
        site = 'nct'

    req = requests.get(url)
    html = req.text
    print('\n##############\n')
    print(url)
    print('----- Name -----')
    print(extract_song_name(html, site))
    print('----- Performed by -----')
    print(extract_performers(html, site))
    print('----- Composed by -----')
    print(extract_composers(html, site))
    print('----- Lyric -----')
    print(extract_lyric(html, site))

urls = ['https://mp3.zing.vn/bai-hat/Never-Not-Lauv/ZW9C6EWD.html',
        'https://mp3.zing.vn/bai-hat/Noi-Nay-Co-Anh-Son-Tung-M-TP/ZW79ZBE8.html',
        'https://mp3.zing.vn/bai-hat/Thang-Dien-JustaTee-Phuong-Ly/ZW9DFW9A.html',
        'https://www.nhaccuatui.com/bai-hat/em-khong-the-tien-tien-ft-touliver.8gSTnzCeZxUF.html',
        'https://www.nhaccuatui.com/bai-hat/runnin-low-blackbear.o5Vyidiyu5XQ.html',
        'https://www.nhaccuatui.com/bai-hat/i-hate-u-i-love-u-gnash-ft-olivia-obrien.8BPviDWw6QX6.html',
        'https://www.nhaccuatui.com/bai-hat/buon-cua-anh-k-icm-ft-dat-g-ft-masew.mlMk7cvOOa5b.html']

# for url in urls:
#     test_song(url)

# {
#     'https://mp3.zing.vn/bai-hat/Thang-Dien-JustaTee-Phuong-Ly/ZW9DFW9A.html':
#         {
#             'name': 'Thằng Điên',
#             'performed_by': ['https://mp3.zing.vn/nghe-si/JustaTee/tieu-su',
#                              'https://mp3.zing.vn/nghe-si/Phuong-Ly/tieu-su'],
#             'composed_by': ['VirusS', 'JustaTee'],
#             'lyric': 'kljladklas'
#             'listens': 44036538,
#             'likes': 81677
#         },
#
#     'https://mp3.zing.vn/bai-hat/Cho-Toi-Lang-Thang-Ngot-Den/ZW79DF7C.html':
#         {
#             'name': 'Cho Tôi Lang Thang',
#             'performed_by': ['https://mp3.zing.vn/nghe-si/Ngot/tieu-su',
#                              'https://mp3.zing.vn/nghe-si/Den/tieu-su'],
#             'composed_by': ['Ngọt', 'Đen'],
#             'lyric': 'kljladklas',
#             'listens': 3640910,
#             'likes': 11472
#         }
# }
