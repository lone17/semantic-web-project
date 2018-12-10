import pickle
from utils import *
from Levenshtein import distance

# site = 'zing'
#
# with open(site + '_artists.vn.kb', 'rb') as f:
#     artists = pickle.load(f)

# names = {v['name'] for v in artists.values()}
# with open(site + '_songs.kb', 'rb') as f:
#     songs = pickle.load(f)
#
# vn = {}
# for k, v in songs.items():
#     print(k)
#     checked = False
#     for n in v['performed_by']:
#         if n in artists:
#             checked = True
#             break
#     if checked:
#         vn[k] = v
#         continue
#     for n in v['composed_by']:
#         if n in names:
#             checked = True
#             break
#     if checked:
#         vn[k] = v
#         continue

# with open(site + '_songs.vn.kb', 'wb') as f:
#     pickle.dump(vn, f)

# with open('zing_artists.vn.kb', 'rb') as f:
#     zing = pickle.load(f)
# with open('nct_artists.vn.kb', 'rb') as f:
#     nct = pickle.load(f)

# zing_final = {}
# for k, v in zing.items():
#     name = v.pop('name')
#     v['zing_urls'] = [k]
#     zing_final[name] = v
#
# nct_final = {}
# for k, v in nct.items():
#     name = v.pop('name')
#     v['zing_urls'] = [k]
#     nct_final[name] = v
#
# with open('zing_artists.vn.final.kb', 'wb') as f:
#     pickle.dump(zing_final, f)
#
# with open('nct_artists.vn.final.kb', 'wb') as f:
#     pickle.dump(nct_final, f)

# s = ''
# for n in zing:
#     s += n
# chars = set(s)
#
# chars = [' ', '#', '$', '&', "'", '(', ')', ',', '-', '.', '=', '>',
#          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
#          '̀', '́', '̃', '̉', '̣', '–',
#          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
#          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
#          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
#          'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
#          'Á', 'Â', 'É', 'Ê', 'Ô', 'Ù', 'Ú', 'Ý', 'à', 'á', 'â', 'ã', 'è', 'é',
#          'ê', 'ì', 'í', 'ò', 'ó', 'ô', 'õ', 'ù', 'ú', 'ý', 'ă', 'Đ', 'ĩ', 'ũ',
#          'ơ', 'Ư', 'ư', 'ạ', 'ả', 'ấ', 'ầ', 'Ẩ', 'ẩ', 'ẫ', 'ậ', 'ắ', 'ằ', 'ẳ',
#          'ặ', 'ẹ', 'ẻ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'ỉ', 'ị', 'ọ', 'ỏ', 'ố', 'ồ',
#          'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ợ', 'ụ', 'ủ', 'Ứ', 'ứ', 'ừ', 'ử', 'ữ',
#          'ự', 'ỳ', 'ỵ', 'ỷ', 'Ỹ', 'ỹ', ]

def merge_zing_nct():
    with open('zing_artists.vn.final.kb', 'rb') as f:
        zing = pickle.load(f)
    with open('nct_artists.vn.final.kb', 'rb') as f:
        nct = pickle.load(f)

    zing_names = [k.lower() for k in zing]
    nct_names = [k.lower() for k in nct]
    name_diff = []
    dob_diff = []
    height_diff = []
    city_diff = []
    final = zing

    for k in final:
        final[k]['nct_url'] = None

    for k in nct:
        if k in final:
            zing_url = final[k]['zing_url']
            nct_url = nct[k]['nct_url']
            if final[k]['birth_name'] != nct[k]['birth_name']:
                zing_name = final[k]['birth_name']
                nct_name = nct[k]['birth_name']
                # score = distance(zing_name, nct_name) / max(len(zing_name), len(nct_name))
                # print((k, zing_name, nct_name, score))
                final[k]['birth_name'] = (k, zing_name, nct_name, zing_url, nct_url)
                name_diff.append(','.join(final[k]['birth_name']))

            if nct[k]['dob'] != 'yyyy/mm/dd':
                err = False
                zing_dob = final[k]['dob'].split('/')
                nct_dob = nct[k]['dob'].split('/')
                def_dob = ['yyyy', 'mm', 'dd']
                final_dob = def_dob
                for i in range(3):
                    if nct_dob[i] != def_dob[i]:
                        if zing_dob[i] != def_dob[i] and zing_dob[i] != nct_dob[i]:
                            err = True
                        else:
                            final_dob[i] = nct_dob[i]
                if err:
                    final[k]['dob'] = ((k, '/'.join(zing_dob), '/'.join(nct_dob), zing_url, nct_url))
                    dob_diff.append(','.join(final[k]['dob']))
                else:
                    final[k]['dob'] = '/'.join(final_dob)

            if nct[k]['city'] is not None:
                if final[k]['city'] is None:
                    final[k]['city'] = nct[k]['city']
                elif final[k]['city'] != nct[k]['city']:
                    zing_city = final[k]['city']
                    nct_city = nct[k]['city']
                    final[k]['city'] = ((k, zing_city, nct_city, zing_url, nct_url))
                    city_diff.append(','.join(final[k]['city']))

            if nct[k]['height'] is not None:
                if final[k]['height'] is None:
                    final[k]['height'] = nct[k]['height']
                elif final[k]['height'] != nct[k]['height']:
                    height_diff.append(k)

            if nct[k]['img'] is not None:
                final[k]['img'] = nct[k]['img']

            final[k]['instruments'].update(nct[k]['instruments'])
            final[k]['genres'].update(nct[k]['genres'])

            if not final[k]['is_band']:
                final[k]['is_band'] = nct[k]['is_band']

            final[k]['nct_url'] = nct_url
        else:
            final[k] = nct[k]
            final[k]['zing_url'] = None

    with open('city.fix', 'rb') as f:
        fix_city = pickle.load(f)
        for k in fix_city:
            final[k] = fix_city[k]

    city_diff = [k for k, v in final.items() if v['city'] and type(v['city']) is not str]

    with open('dob_diff.csv', 'r', encoding='utf-8-sig') as f:
        fix_dob = f.read().strip().split('\n')
        fix_dob = [s.split(',') for s in fix_dob]

    for k, dob, wiki in fix_dob:
        final[k]['dob'] = dob
        if wiki and 'wiki' not in final[k]:
            final[k]['wiki'] = wiki

    dob_diff = [k for k, v in final.items() if type(v['dob']) is not str]

    with open('name_diff.csv', 'r', encoding='utf-8-sig') as f:
        fix_name = f.read().strip().split('\n')
        fix_name = [s.split(',') for s in fix_name]

    for k, name, wiki in fix_name:
        final[k]['birth_name'] = name
        if wiki and 'wiki' not in final[k]:
            final[k]['wiki'] = wiki

    name_diff = [k for k, v in final.items() if type(v['birth_name']) is not str]

def save_final(final):
    with open('artists.final.kb', 'wb') as f:
        pickle.dump(final, f)

def city_to_wiki():
    with open('artists.final.kb', 'rb') as f:
        final = pickle.load(f)

    with open('city.wiki', 'rb') as f:
        city_wiki = pickle.load(f)

    for k, v in final.items():
        if v['city']:
            final[k]['city'] = city_wiki[v['city']]

def merge_chieucao():
    height_err = []
    city_err = []
    with open('artists.final.kb', 'rb') as f:
        final = pickle.load(f)

    with open('chieucao.kb', 'rb') as f:
        chieucao = pickle.load(f)

    for k, v in chieucao.items():
        if k not in final:
            print('missing', k)
            continue
        if v['height']:
            if final[k]['height']:
                if v['height'] != final[k]['height']:
                    height_err.append(k)
            else:
                final[k]['height'] = v['height']
        if v['city']:
            if final[k]['city']:
                if v['city'] != final[k]['city']:
                    city_err.append(k)
            else:
                final[k]['city'] = v['city']

def merge_wiki():
    with open('artists.final.kb', 'rb') as f:
        final = pickle.load(f)

    with open('artist.wiki', 'rb') as f:
        wiki = pickle.load(f)

    err = []
    missing = []

    for k, v in wiki.items():
        if k not in final:
            missing.append(k)
        else:
            if 'wiki' not in final[k]:
                final[k]['wiki'] = v['wiki']
            elif final[k]['wiki'] != v['wiki']:
                err.append((k, final[k]['wiki'], v['wiki']))

    for v in final.values():
        if 'wiki' not in v:
            v['wiki'] = None

# save_final(final)
