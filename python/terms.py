import sparql
from html.parser import HTMLParser
from unidecode import unidecode

terms = {}
queries = {}
lists = ['subject','sport']

for l in lists:
    with open ('sources/{}.txt'.format(l)) as f:
        content = f.readlines()
    terms[l] = [x.strip() for x in content]

queries['metal_band'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?n WHERE
{
{
{?thing dct:subject dbc:Thrash_metal_musical_groups.}
UNION
{?thing dct:subject dbc:Extreme_metal_musical_groups.}
UNION
{?thing dct:subject dbc:Progressive_metal_musical_groups.}
UNION
{?thing dct:subject dbc:Norwegian_avant-garde_metal_musical_groups.}
UNION
{?thing dct:subject dbc:Doom_metal_musical_groups.}
}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "list", "i"))
BIND(REPLACE(?name, " \\\\(.*\\\\)", "", "i") AS ?n)
}
"""
    
queries['scientist'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?n WHERE
{
{?thing dct:subject dbc:Fictional_mad_scientists.
?thing rdf:type yago:Person100007846.}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
BIND(REPLACE(?name, " \\\\(.*\\\\)", "", "i") AS ?n)
}
"""

queries['martial_artist'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?n WHERE
{
{?thing dct:subject dbc:Anthropomorphic_martial_artists.
}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "list", "i"))

BIND(REPLACE(?name, " \\\\(.*\\\\)", "", "i") AS ?n)
FILTER (!regex(?n, "s$", "i"))

}
"""

queries['conjecture'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Conjectures.}
}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""
    
queries['capital'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Capitals_in_Africa.}
UNION
{?thing dct:subject dbc:Capitals_in_South_America.}
}
?thing rdfs:label ?n.
FILTER (lang(?n) = 'en')
FILTER (!regex(?n, "list", "i"))
BIND(REPLACE(?n, " \\\\(city\\\\)", "", "i") AS ?name)
}
"""

queries['cheese'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:English_cheeses.
?thing rdfs:label ?n.
FILTER (lang(?n) = 'en')
FILTER (!regex(?n, "list", "i"))
BIND(REPLACE(?n, " cheese", "", "i") AS ?name)
}
"""

queries['poisonous_plant'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing a yago:PoisonousPlant113100156.
?thing dbp:name ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "list", "i"))
}
"""

queries['star_trek_planet'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Star_Trek_planets.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""

queries['asteroid'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Mars-crossing_asteroids.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""

queries['minor_planet'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Minor_planets_named_from_Roman_mythology.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""

queries['constellation'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Constellations.
?thing dbp:name ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""

queries['horse_colour'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Horse_coat_colors.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "Equine", "i"))
}
"""

# European Rodents
queries['rodent'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Rodents_of_Europe.}
UNION
{?thing dct:subject dbc:Rodents_of_North_America.}
}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
}
"""

queries['godzilla'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Godzilla_characters.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""
# Pests. This is a bit hacky as the list includes some things we don't
# really want, like latin names. Also, tracery's plural modifier
# doesn't handle moths!

queries['pest'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Household_pest_insects.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "tus", "i"))
FILTER (!regex(?name, "pes", "i"))
FILTER (!regex(?name, "mex", "i"))
FILTER (!regex(?name, "ella", "i"))
FILTER (!regex(?name, "dae", "i"))
FILTER (!regex(?name, "genus", "i"))
FILTER (!regex(?name, "entomology", "i"))
FILTER (!regex(?name, "moth", "i"))

}
"""

# European Rodents
queries['amphibian'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Amphibians_of_Europe.}
UNION
{?thing dct:subject dbc:Amphibians_of_North_America.}
}
?thing rdf:type dbo:Amphibian.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
}
"""

queries['element'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Chemical_elements.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name,"\\\\(","i"))
FILTER (!regex(?name,"element","i"))
}
"""

# North American Primates
queries['primate'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Primates_of_Africa.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name,"\\\\(","i"))
FILTER (!regex(?name, "list", "i"))
}
"""

queries['village'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Villages_in_Wiltshire.}
UNION
{?thing dct:subject dbc:Villages_in_Lancashire.}
UNION
{?thing dct:subject dbc:Villages_in_Norfolk.}
UNION
{?thing dct:subject dbc:Villages_in_Argyll_and_Bute.}
UNION
{?thing dct:subject dbc:Villages_in_Lewis.}
UNION
{?thing dct:subject dbc:Villages_in_the_Outer_Hebrides.}
UNION
{?thing dct:subject dbc:Villages_in_Gwynedd.}
}
?thing foaf:name ?name.
FILTER (lang(?name) = 'en')
}
"""

queries['town'] = """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT distinct ?thing ?name WHERE
{
{
{?thing dct:subject dbc:Towns_in_Wiltshire.}
UNION
{?thing dct:subject dbc:Towns_in_Lancashire.}
UNION
{?thing dct:subject dbc:Towns_in_Norfolk.}
}
?thing foaf:name ?name.
FILTER (lang(?name) = 'en')
}
"""

def dbpedia_things(query):
    things = []
    result = sparql.query('http://dbpedia.org/sparql', query)
    for row in result.fetchall():
        values = sparql.unpack_row(row)
        name = values[1]
        things.append(name)
    return things

def unescape(l):
    h = HTMLParser()
    return map(lambda x : unidecode(h.unescape(x)), l)

for n, q in queries.iteritems():
    terms[n] = unescape(dbpedia_things(q))
    
#terms['village'] = unescape(dbpedia_things(queries['village']))

terms['zodiac'] = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces' ]

terms['got_house'] = ['House Arryn', 'House Baratheon', 'House Bolton',
    'House Frey', 'House Greyjoy', 'House Lannister', 'House Martell', 'House Stark',
    'House Targaryen', 'House Tully', 'House Tyrell']


