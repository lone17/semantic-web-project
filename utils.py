import requests
import datetime
import re
from dateutil.parser import parse
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
                'đàn tranh', 'ukulele', 'keyboard', 'contrabass', 'accordeon']

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
                       'tay bass': 'guitar', 'và bass': 'guitar',
                       'accordéon': 'accordeon', 'phong cầm': 'accordeon'}

cities = ['An Giang', 'Biên Hòa', 'Buôn Ma Thuột', 'Bà Rịa', 'Bà Rịa - Vũng Tàu',
          'Bình Dương', 'Bình Phước', 'Bình Thuận', 'Bình Định', 'Bạc Liêu',
          'Bảo Lộc', 'Bắc Giang', 'Bắc Kạn', 'Bắc Ninh', 'Bến Tre', 'Cam Ranh',
          'Cao Bằng', 'Cao Lãnh', 'Châu Đốc', 'Cà Mau', 'Cần Thơ', 'Cẩm Phả',
          'Gia Lai', 'Huế', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tiên', 'Hà Tĩnh',
          'Hòa Bình', 'Hưng Yên', 'Hạ Long', 'Hải Dương', 'Hải Phòng', 'Hậu Giang',
          'Hội An', 'Khánh Hòa', 'Kiên Giang', 'Kon Tum', 'Lai Châu', 'Long An',
          'Long Xuyên', 'Lào Cai', 'Lâm Đồng', 'Lạng Sơn', 'Móng Cái', 'Mỹ Tho',
          'Nam Định', 'Nghệ An', 'Nha Trang', 'Ninh Bình', 'Ninh Thuận',
          'Phan Rang - Tháp Chàm', 'Phan Thiết', 'Phú Thọ', 'Phú Yên', 'Phúc Yên',
          'Phủ Lý', 'Pleiku', 'Quy Nhơn', 'Quảng Bình', 'Quảng Nam', 'Quảng Ngãi',
          'Quảng Ninh', 'Quảng Trị', 'Rạch Giá', 'Sa Đéc', 'Sóc Trăng', 'Sông Công',
          'Sơn La', 'Sầm Sơn', 'Tam Kỳ', 'Tam Điệp', 'Thanh Hóa',
          'Hồ Chí Minh', 'HCM', 'thành phố mang tên Bác', 'Sài Gòn',
          'Thái Bình', 'Thái Nguyên', 'Thủ Dầu Một', 'Thừa Thiên - Huế',
          'Tiền Giang', 'Trà Vinh', 'Tuy Hòa', 'Tuyên Quang', 'Tân An',
          'Tây Ninh', 'Uông Bí', 'Vinh', 'Việt Trì', 'Vĩnh Long', 'Vĩnh Phúc',
          'Vĩnh Yên', 'Vũng Tàu', 'Vị Thanh', 'Yên Bái', 'Điện Biên', 'Đà Lạt',
          'Đà Nẵng', 'Đông Hà', 'Đắk Lắk', 'Đắk Nông', 'Đồng Hới', 'Đồng Nai',
          'Đồng Tháp', 'Đồng Xoài']

bands = ['R.E.D', 'HKT', 'ATM', 'B.O.M', 'Nhóm Hot Steps', 'Piano Band', 'SMS',
         'Team A', 'TVM', 'Vboys', 'Ban Nhạc Trúc Xanh', 'Ban Nhạc Hương Sen',
         'Nhóm Nhạc ...', 'Ban Nhạc Anh Em', 'Zero9', 'Nobb', 'P.M Band',
         'C.V Band']

cities = [c.lower() for c in cities]
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

def extract_artist_info(html, site):
    soup = BeautifulSoup(html, features='lxml')
    birth_name, dob, country = None, None, None

    if site == 'zing':
        css_selectors = ['body > div.wrapper-page > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div > ul > li',
                         'body > div.wrapper-page > div.full-banner > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div > ul > li',
                         'body > div.wrapper-page > div > div.container > div.wrap-body.group.page-artist-all.page-artist.container > div.wrap-2-col > div.wrap-content > div > div.row > div > div > ul > li']
        for css_selector in css_selectors:
            for li in soup.select(css_selector):
                text = li.text
                lower_text = text.lower()
                matches = list(re.finditer('tên thật:?\s*', lower_text))
                if len(matches) > 0:
                    span = matches[0]
                    text = text[span.end():].strip()
                    if text != '':
                        birth_name = text
                else:
                    matches = list(re.finditer('ngày sinh:?\s*', lower_text))
                    if len(matches) > 0:
                        span = matches[0]
                        text = text[span.end():].replace('0000', '').replace('.', '/')
                        text = re.sub('/\s+', '/', text).strip('/')
                        if text != '':
                            test1 = parse(text, dayfirst=True, default=datetime.datetime(4,4,4))
                            test2 = parse(text, dayfirst=True, default=datetime.datetime(8,8,8))
                            if test1.year > 2500:
                                test1 = test1.replace(year=test1.year-1000)
                                test2 = test2.replace(year=test2.year-1000)
                            dob = []
                            tmp = test1.strftime('%d%m%Y')
                            if test1.day == test2.day:
                                dob.append(tmp[:2])
                            if test1.month == test2.month:
                                dob.append(tmp[2:4])
                            if test1.year == test2.year:
                                dob.append(tmp[4:])
                            dob = '/'.join(dob)
                    else:
                        matches = list(re.finditer('quốc gia:?\s*', lower_text))
                        if len(matches) > 0:
                            span = matches[0]
                            text = text[span.end():].strip()
                            if text != '':
                                country = text
                            elif 'trung quốc' in text_lower or 'hoa ngữ' in text_lower or 'china' in text_lower:
                                kb[url]['country'] = 'China'
                            elif 'nhật bản' in text_lower or 'japan' in text_lower:
                                kb[url]['country'] = 'Japan'
                            elif 'hàn quốc' in text_lower or ' korea' in text_lower:
                                kb[url]['country'] = 'South Korea'
                            elif 'việt' in lower_text:
                                country = 'Việt Nam'
                            elif 'âu mỹ' in text_lower:
                                kb[url]['country'] = 'Unknown'
            if birth_name or dob or country:
                break
    elif site == 'nct':
        css_selector = 'body > div.singer-top-cover > div.wrap > div > div.singer-left-avatar > p'
        for p in soup.select(css_selector):
            text = p.text
            lower_text = text.lower()
            matches = list(re.finditer('tên thật:?\s*', lower_text))
            if len(matches) > 0:
                span = matches[0]
                text = text[span.end():].strip()
                if text != '':
                    birth_name = text
            else:
                matches = list(re.finditer('sinh nhật:?\s*', lower_text))
                if len(matches) > 0:
                    span = matches[0]
                    text = text[span.end():].replace('0000', '').replace('.', '/')
                    text = re.sub('/\s+', '/', text).strip('/')
                    if text != '':
                        test1 = parse(text, dayfirst=True, default=datetime.datetime(4,4,4))
                        test2 = parse(text, dayfirst=True, default=datetime.datetime(8,8,8))
                        if test1.year > 2500:
                            test1 = test1.replace(year=test1.year-1000)
                            test2 = test2.replace(year=test2.year-1000)
                        dob = []
                        tmp = test1.strftime('%d%m%Y')
                        if test1.day == test2.day:
                            dob.append(tmp[:2])
                        if test1.month == test2.month:
                            dob.append(tmp[2:4])
                        if test1.year == test2.year:
                            dob.append(tmp[4:])
                        dob = '/'.join(dob)
                else:
                    matches = list(re.finditer('quốc gia:?\s*', lower_text))
                    if len(matches) > 0:
                        span = matches[0]
                        text = text[span.end():].strip()
                        if text != '':
                            country = text
                        elif 'trung quốc' in text_lower or 'hoa ngữ' in text_lower or 'china' in text_lower:
                            kb[url]['country'] = 'China'
                        elif 'nhật bản' in text_lower or 'japan' in text_lower:
                            kb[url]['country'] = 'Japan'
                        elif 'hàn quốc' in text_lower or ' korea' in text_lower:
                            kb[url]['country'] = 'South Korea'
                        elif 'việt' in lower_text:
                            country = 'Việt Nam'
                        elif 'âu mỹ' in text_lower:
                            kb[url]['country'] = 'Unknown'

    return {'birth_name': birth_name, 'dob': dob, 'country': country}

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

def extract_img(html, site):

    soup = BeautifulSoup(html, features='lxml')

    if site == 'zing':
        css_selector = 'body > div > div > div > div > div > div > img'
        default_img = 'https://photo-zmp3.zadn.vn/default.jpg'
    elif site == 'nct':
        css_selector = 'body > div.singer-top-cover > div.wrap > div > div.singer-left-avatar > div > img'
        default_img = None

    try:
        img = soup.select(css_selector)[0].get('src')
    except Exception as e:
        raise e

    if img == default_img:
        img = None

    return img

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
        name = soup.select(css_selector)[0].text.strip().split('\n')[0]
    elif site == 'nct':
        css_selector = '#box_playing_id > div.info_name_songmv > div.name_title > h1'
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
        ret = ['https://mp3.zing.vn' + a.get('href') + '/tieu_su'
               for a in soup.select(css_selector)]
    elif site == 'nct':
        css_selector = '#box_playing_id > div.info_name_songmv > div.name_title > h2 > a'
        ret = [a.get('href') if 'tim-kiem' not in a.get('href') else a.text
               for a in soup.select(css_selector)]

    return ret

def extract_composers(html, site):
    soup = BeautifulSoup(html, features='lxml')
    ret = []

    if site == 'zing':
        css_selector = '#composer-container > h2'
        ret = [h2.text.strip() for h2 in soup.select(css_selector)]
    elif site == 'nct':
        css_selector = '#_divLyricHtml > div.pd_name_lyric > p'
        for p in soup.select(css_selector):
            if 'Nhạc sĩ:' in p.text:
                ret = [s.strip() for s in p.text.replace('Nhạc sĩ:', '').split(',')]


    return ret

def get_all_contexts(text, pattern, span):
    lower_text = text.lower()
    matches = re.findall(pattern, lower_text)

    contexts = []
    for match in matches:
        start, end = match.span()
        left = text[:start]
        right = text[end:]
        indicator = text[start:end]
        if span[0] == 0:
            context = [indicator] + right.split()[:span[1]]
        else:
            context = left.split()[-span[0]:] + [indicator] + right.split()[:span[1]]
        contexts.append(' '.join(context))

    return contexts

def get_first_context(text, indicators, span):
    lower_text = text.lower()
    pattern = '|'.join(indicators)
    first = re.search(pattern, lower_text)

    if first is None:
        return ''

    start, end = first.span()
    left = text[:start]
    right = text[end:]
    indicator = text[start:end]
    if span[0] == 0:
        context = [indicator] + right.split()[:span[1]]
    else:
        context = left.split()[-span[0]:] + [indicator] + right.split()[:span[1]]

    return ' '.join(context)

def get_first_context_in_sentence(text, indicators, span):
    text = text.lower()
    pattern = '|'.join(indicators)
    context = ''
    for sentence in text.split('.'):
        indicator = re.search(pattern, sentence)
        if indicator:
            indicator = indicator.group(0)
            context = sentence
            break

    if context == '':
        return '', ''

    left, right = context.split(indicator, 1)
    if span[0] == 0:
        # context = [indicator] + right.split()[:span[1]]
        return '', ' '.join(right.split()[:span[1]])
    else:
        # context = left.split()[-span[0]:] + [indicator] + right.split()[:span[1]]
        return ' '.join(left.split()[-span[0]:]), ' '.join(right.split()[:span[1]])

    # return ' '.join(context)

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

def extract_first_city(context):
    if not context:
        return None

    first_city = None
    first_index = 99999
    for c in cities:
        idx = context.find(c)
        if idx != -1 and idx < first_index:
            first_index = idx
            first_city = c

    return first_city

def extract_city(text):
    indicators = ['sinh tại', 'sinh ra', 'quê', 'đến từ', 'lớn lên', 'xuất thân',
                  'nguyên quán']
    left, right = get_first_context_in_sentence(text, indicators, (20, 20))
    first_city = extract_first_city(right)
    if not first_city:
        first_city = extract_first_city(left)

    if not first_city:
        indicators = ['sinh vào', 'sinh năm', 'sinh ngày', 'sống ở']
        left, right = get_first_context_in_sentence(text, indicators, (0, 30))
        first_city = extract_first_city(right)
        if not first_city:
            first_city = extract_first_city(left)

    if not first_city:
        indicators = ['gia đình', 'cha mẹ', 'bố mẹ']
        left, right = get_first_context_in_sentence(text, indicators, (0, 20))
        first_city = extract_first_city(right)
        if not first_city:
            first_city = extract_first_city(left)

    if first_city in ['hồ chí minh', 'hcm', 'thành phố mang tên bác', 'sài gòn']:
        return 'Thành phố Hồ Chí Minh'

    if first_city:
        return first_city.title()
    else:
        return None

urls = []
test_time = ['https://mp3.zing.vn/nghe-si/10cm/tieu-su',
             'https://mp3.zing.vn/nghe-si/Andamiro/tieu-su',
             'https://mp3.zing.vn/nghe-si/Baek-Chung-Kang/tieu-su',
             'https://mp3.zing.vn/nghe-si/Baek-Ki-Sung/tieu-su',
             'https://mp3.zing.vn/nghe-si/Chau-Ngan-Hoanh/tieu-su',
             'https://mp3.zing.vn/nghe-si/Debelah-Morgan/tieu-su',
             'https://mp3.zing.vn/nghe-si/Hoang-Ngoc-My/tieu-su',
             'https://mp3.zing.vn/nghe-si/Hwasa/tieu-su',
             'https://mp3.zing.vn/nghe-si/Koshio-Sakura/tieu-su',
             'https://mp3.zing.vn/nghe-si/Minh-Ha/tieu-su',
             'https://mp3.zing.vn/nghe-si/Nga-Pham/tieu-su',
             'https://mp3.zing.vn/nghe-si/Sowelu/tieu-su',
             'https://mp3.zing.vn/nghe-si/Thai-Foon/tieu-su',
             'https://mp3.zing.vn/nghe-si/Tuan-Quynh/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-bach.html',
             'https://www.nhaccuatui.com/nghe-si-beethoven.html',
             'https://www.nhaccuatui.com/nghe-si-bridgit-mendler.html',
             'https://www.nhaccuatui.com/nghe-si-elliott-smith.html',
             'https://www.nhaccuatui.com/nghe-si-fergie.html',
             'https://www.nhaccuatui.com/nghe-si-kwill.html',
             'https://www.nhaccuatui.com/nghe-si-lee-soo-young.html',
             'https://www.nhaccuatui.com/nghe-si-matt-cardle.html']
test_img = ['https://mp3.zing.vn/nghe-si/Nhom-1080/tieu_su',
            'https://mp3.zing.vn/nghe-si/Eden/tieu-su']
test_city = ['https://mp3.zing.vn/nghe-si/Son-Tung-M-TP/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-son-tung-mtp.html',
             'https://mp3.zing.vn/nghe-si/Soobin-Hoang-Son/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-soobin-hoang-son.html',
             'https://mp3.zing.vn/nghe-si/Thuy-Chi/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-thuy-chi.html',
             'https://mp3.zing.vn/nghe-si/Noo-Phuoc-Thinh/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-noo-phuoc-thinh.html',
             'https://mp3.zing.vn/nghe-si/Dong-Nhi/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-dong-nhi.html',
             'https://mp3.zing.vn/nghe-si/Phan-Manh-Quynh/tieu-su',
             'https://www.nhaccuatui.com/nghe-si-phan-manh-quynh.html',]
urls += test_city
def test_artist(url):
    if 'https://mp3.zing.vn' in url:
        site = 'zing'
    elif 'https://www.nhaccuatui.com' in url:
        site = 'nct'

    req = requests.get(url)
    html = req.text
    print('\n##############\n')
    print(url)
    text = extract_biography(html, site)
    print(extract_artist_name(html, site))
    # print(extract_professions(text))
    # print(extract_instruments(text))
    # info = extract_artist_info(html, site)
    # print(info)
    # print(extract_img(html, site))
    print(extract_city(text))
    # print(extract_height(text))

# for url in urls:
#     test_artist(url)

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

# urls = ['https://mp3.zing.vn/bai-hat/Never-Not-Lauv/ZW9C6EWD.html',
#         'https://mp3.zing.vn/bai-hat/Noi-Nay-Co-Anh-Son-Tung-M-TP/ZW79ZBE8.html',
#         'https://mp3.zing.vn/bai-hat/Thang-Dien-JustaTee-Phuong-Ly/ZW9DFW9A.html',
#         'https://www.nhaccuatui.com/bai-hat/em-khong-the-tien-tien-ft-touliver.8gSTnzCeZxUF.html',
#         'https://www.nhaccuatui.com/bai-hat/runnin-low-blackbear.o5Vyidiyu5XQ.html',
#         'https://www.nhaccuatui.com/bai-hat/i-hate-u-i-love-u-gnash-ft-olivia-obrien.8BPviDWw6QX6.html',
#         'https://www.nhaccuatui.com/bai-hat/buon-cua-anh-k-icm-ft-dat-g-ft-masew.mlMk7cvOOa5b.html']

# for url in urls:
#     test_song(url)

# {
#     'https://mp3.zing.vn/bai-hat/Thang-Dien-JustaTee-Phuong-Ly/ZW9DFW9A.html':
#         {
#             'name': 'Thằng Điên',
#             'performed_by': ['https://mp3.zing.vn/nghe-si/JustaTee/tieu-su',
#                              'https://mp3.zing.vn/nghe-si/Phuong-Ly/tieu-su'],
#             'composed_by': ['VirusS', 'JustaTee'],
#             'lyric': 'Giờ tôi lại lang thang ...'
#         },
#
#     'https://mp3.zing.vn/bai-hat/Cho-Toi-Lang-Thang-Ngot-Den/ZW79DF7C.html':
#         {
#             'name': 'Cho Tôi Lang Thang',
#             'performed_by': ['https://mp3.zing.vn/nghe-si/Ngot/tieu-su',
#                              'https://mp3.zing.vn/nghe-si/Den/tieu-su'],
#             'composed_by': ['Ngọt', 'Đen'],
#             'lyric': 'Cho tôi đi theo với Nơi anh đi về ...',
#         }
# }

# {
#     'https://mp3.zing.vn/nghe-si/Son-Tung-M-TP/tieu-su':
#         {
#             'name': 'Sơn Tùng M-TP',
#             'birth_name': 'Nguyễn Thanh Tùng',
#             'dob': '05/07/1994',
#             'height': 166,
#             'city': 'Thái Bình',
#             'country': 'Việt Nam',
#             'professions': {'hip-hop', 'pop', 'rap'},
#             'instruments': {'piano'},
#             'image': 'https://photo-resize-zmp3.zadn.vn/w240h240_jpeg/avatars/e/e/ee58fcc0ff45002b8d416bd7685809ce_1487040461.jpg'
#             'member_of': None,
#             'wiki': 'https://vi.wikipedia.org/wiki/S%C6%A1n_T%C3%B9ng_M-TP'
#         },
#
#     'https://mp3.zing.vn/nghe-si/Ngot/tieu-su':
#         {
#             'name': 'Ngọt',
#             'birth_name': 'Ngọt',
#             'dob': '01/11/2013',
#             'height': None,
#             'city': 'Hà Nội',
#             'country': 'Việt Nam',
#             'professions': {'indie', 'pop'},
#             'instruments': {'guitar', 'drum'},
#             'image': 'https://photo-resize-zmp3.zadn.vn/w240h240_jpeg/avatars/8/2/82c1b4ebd0ec188c2c3b0429504b8802_1507798683.jpg'
#             'member_of': None,
#             'wiki': 'https://vi.wikipedia.org/wiki/Ng%E1%BB%8Dt_(ban_nh%E1%BA%A1c)'
#         }
# }
