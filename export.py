from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
# from rdflib.namespace import RDF, FOAF
from rdflib import Graph
from utils import *

ns = "https://www.sw.uet.vnu.edu.vn/group4/"
RDF = Namespace(ns)
FOAF = Namespace(ns)

with open('songs.final.kb', 'rb') as f:
    songs_final = pickle.load(f)

with open('artists.final.kb', 'rb') as f:
    artists_final = pickle.load(f)

with open('unknown_composers.txt', 'r', encoding='utf-8-sig') as f:
    unknown_composers = f.read().strip().split('\n')

for n in unknown_composers:
    artists_final[n] = new_artist(n)

# with open('city.wiki', 'rb') as f:
#     tmp = pickle.load(f)
#     wiki_to_city = {v: '_'.join(k.split()) for k, v in tmp.items()}

g = Graph()

# for v in wiki_to_city.values():
#     obj = URIRef(ns + v)
#     g.add( (obj, RDF.type, FOAF.Location) )

for k, v in artists_final.items():
    k = k.replace('<', '[').replace('>', ']')
    obj = URIRef(ns + '_'.join(k.split()))
    if v['is_band']:
        g.add( (obj, RDF.type, FOAF.Organization) )
    else:
        g.add( (obj, RDF.type, FOAF.Person) )
        if v['height']:
            g.add( (obj, FOAF.Height, Literal(v['height'])) )
        if v['birth_name']:
            name = standardize_name(v['birth_name'])
            g.add( (obj, FOAF.birthName, Literal(name)) )
        if v['city']:
            location = Literal(v['city'])
            # location = URIRef(v['city'])
            # g.add( (location, RDF.type, FOAF.Location) )
            g.add( (obj, FOAF.birthPlace, location) )
        if v['dob'] and v['dob'] != 'yyyy-mm-dd':
            dob = Literal(v['dob'].upper())
            g.add( (obj, FOAF.birthDate, dob) )
        for item in v['member_of']:
            band = URIRef(ns + '_'.join(item['band'].split()))
            g.add( (obj, FOAF.memberOf, band) )

    for item in v['instruments']:
        g.add( (obj, FOAF.instrument, Literal(item)) )
    for item in v['genres']:
        g.add( (obj, FOAF.profession, Literal(item)) )
    if v['img']:
        g.add( (obj, FOAF.image, Literal(v['img'])) )
    if v['wiki']:
        g.add( (obj, FOAF.linkToWiki, Literal(v['wiki'])) )

for k, v in songs_final.items():
    k = k.replace('"', '').replace('\\', '')
    obj = URIRef(ns + '_'.join(k.split()))
    g.add( (obj, RDF.type, FOAF.Song) )

    for n in v['performed_by']:
        n = n.replace('<', '[').replace('>', ']')
        performer = URIRef(ns + '_'.join(n.split()))
        g.add( (obj, FOAF.performedBy, performer) )
    for n in v['composed_by']:
        n = n.replace('<', '[').replace('>', ']')
        composer = URIRef(ns + '_'.join(n.split()))
        g.add( (obj, FOAF.composed_by, composer) )
    if v['lyric']:
        g.add( (obj, FOAF.lyric, Literal(v['lyric'])) )

# bob = URIRef("http://example.org/people/Bob")
# linda = URIRef("http://example.org/people/Linda")
# jack = URIRef("http://example.org/people/Jack")
#
# g = Graph()
#
# g.add( (bob, RDF.type, FOAF.Person) )
# g.add( (bob, FOAF.name, Literal('Bob')) )
# g.add( (linda, RDF.type, FOAF.Person) )
# g.add( (linda, FOAF.name, Literal('Linda')) )
# g.add( (jack, RDF.type, FOAF.Person) )
# g.add( (jack, FOAF.name, Literal('Jack')) )
#
# g.add( (bob, FOAF.knows, linda) )
# bob2 = URIRef("http://example.org/people/Bob")
# g.add( (bob, FOAF.knows, jack) )
#
# ian = URIRef("http://example.org/people/Ian")
# g.add( (ian, RDF.type, FOAF.Person) )
# g.add( (ian, FOAF.name, Literal('Ian')) )
# g.add( (ian, FOAF.knows, bob2) )
#
g.serialize(destination='final.xml', format='xml', encoding='utf-8-sig')
