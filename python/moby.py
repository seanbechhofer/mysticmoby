#!/usr/local/bin/python
"""Generate a tracery grammar for horoscopes"""
__author__ = "Sean Bechhofer"
__copyright__ = "Copyright 2016, Sean Bechhofer"
__credits__ = ["Sean Bechhofer"]
import json
import argparse
from html.parser import HTMLParser

import tracery
from tracery.modifiers import base_english
import sparql
import re
from terms import terms

parser = argparse.ArgumentParser(description='Generate Tracery Grammar.')
parser.add_argument('-o', '--output', help='output file', default="moby.json")

args = parser.parse_args()

# Grab stuff from dbpedia
star_trek_planet = terms['star_trek_planet']
asteroid = terms['asteroid']
constellation = terms['constellation']
minor_planet = terms['minor_planet']
element = terms['element']
village = terms['village']
town = terms['town']

godzilla = terms['godzilla']
rodent = terms['rodent']
amphibian = terms['amphibian']
pest = terms['pest']
primate = terms['primate']

horse_colour = []
for c in terms['horse_colour']:
    horse_colour.append(re.sub(' (.*)', '', c))
zodiac = terms['zodiac']
got_house = terms['got_house']

origin_rules = []
stems_primary = ['travel', 'work', 'love', 'news', 'money', 'change']
stems_secondary = ['travel', 'work', 'love', 'news', 'money', 'change']
for s1 in stems_primary:
    for s2 in stems_secondary:
        if s1 != s2:
            origin_rules.append("#stellar.capitalize#. #{}.capitalize#. #{}.capitalize#. #maybe_lucky#".format(s1,s2))
            origin_rules.append("#{}.capitalize# as #stellar.capitalize#. #{}.capitalize#. #maybe_lucky#".format(s1,s2))

# Tracery Grammar
rules = {
    'origin': origin_rules,
    'love': ['new love #horizon#', '#qualifier.a# time to rekindle an old flame',
             '#qualifier.a# period for relationships',
             'you #you_may# find love in #place#',
             'pay attention to your relationships'],
    'you_may': ['may', 'might', 'could', 'may not', 'probably won\'t'],
    'may': ['#may_positive#', '#may_ambivalent#', '#may_negative#'],
    'may_positive': ['may', 'might', 'could'],
    'may_ambivalent': ['seems to', 'appears to', 'is likely to'],
    'may_negative': ['may not', 'is unlikely to'],
    'place': ['#village#', '#town#', '#capital#'],
    'horizon': ['is on the horizon',
                'is highly unlikely',
                'could be round the corner',
                'is on the cards',
                'may come to pass'],
    'travel': ['avoid #town#',
               '#surprise_modifier.a# surprise awaits in #village#',
               'travel to #town# is not recommended',
               'travel to #place# will reap rewards',
               'a trip to #place# offers promise',
               'going to #place# is ill-advised' ],
    'money': ['unexpected expenses could arise',
              '#qualifier# fortune #may# come your way #today#',
              'profit #horizon#'],
    'change': ['consider a change of #changed#',
               'it may be time to reconsider your #changed#'],
    'changed': ['relationship', 'career', 'clothing', 'opinion', 'perspective',
                'direction','beliefs', 'vocation', 'banking arrangements'],
    'surprise_modifier': ['pleasant', 'nasty', 'unpleasant', '', 'unexpected'],
    'work': ['work will #work_modifier# #today#', 'work #may# #be# #rewarding# #today#'],
    'be': ['prove', 'be', 'become'],
    'rewarding': ['rewarding', 'a waste of time', 'boring', 'a revelation', 'unbearable'],
    'work_modifier': ['bear fruit', 'prove difficult', 'try your patience'],
    'today': ['today', 'tomorrow', 'this week'],
    'day': ['#qualifier.a# day#', '#good_qualifier.a# opportunity'],
    'news': ['#qualifier# news #may_positive# come from #stranger.a#',
             'news #may_positive# arrive with #stranger.a#'],
    'stranger': ['stranger', 'friend', 'old friend', 'unexpected quarter'], 
    'qualifier': ['#good_qualifier#', '#bad_qualifier#'],
    'good_qualifier': ['good', 'excellent'],
    'bad_qualifier': ['bad', 'unwelcome'],
    
    'activity': ['#day# to #job# the #room#'],
    
    'job': ['clean', 'paint', 'defumigate', 'dismantle', 'spend time in', 'rebuild',
        'clear up',
        'disinfect',
        'dust',
        'sweep',
        'tidy up',
        'fix',
        'redecorate',
        'renovate',
        'rearrange'],
    'room': ['kitchen', 'office', 'bathroom', 'attic', 'garden', 'toilet',
             'closet', 'living room', 'dining room', 'garage', 'study',
             'workshop', 'conservatory', 'cellar', 'front yard'
        ],
    'stellar': ['#body# #coinciding# #constellation#',
                '#body# #coinciding# #constellation#',
                '#body# #coinciding# #zodiac#',
                '#body# #coinciding# #zodiac#',
                '#body# #coinciding# #zodiac#',
                '#zodiac# #coinciding# #body#',
                '#zodiac# #coinciding# #body#',
                '#body# #coinciding# #got_house#',
                '#got_house# #coinciding# #zodiac#',
                '#constellation# #modified#',
                '#constellation# #modified#',
                '#zodiac# #modified#',
                '#zodiac# #modified#',
                '#zodiac# #modified#'],
    'planet': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Neptune', 'Saturn',
               'Uranus', 'Pluto'],
    'body': ['#planet#', '#planet#', '#planet#', '#star_trek_planet#'],
#    'body': ['#planet#', '#planet#', '#planet#', '#star_trek_planet#', '#minor_planet#', '#asteroid#'],
    'constellation': constellation,
    'star_trek_planet': star_trek_planet,
    'asteroid': asteroid,
    'minor_planet': minor_planet,
    'coinciding': ['is in confluence with', 'is in opposition to',
                   'is ascending in', 'is entering',
                   'is leaving', 'will be duetting with', 'is in the #quarter# of',
                   'is annoyed with'],
    'quarter': ['upper quarter', 'lower quarter', 'fifth quarter', 'vicinity'],
    'modified': ['is obscure', 'is acute', 'is descending',
                 'is angry', 'has inverted', 'is hidden', 'is partially oblated',
                 'is oblated', 'is rhomboid', 'enters a spherical period'],
    'maybe_lucky': ['#lucky#', '#lucky#', ''],
    'lucky': ['#lucky_colour#.', '#lucky_animal#.', '#lucky_number#.', '#lucky_element#.', '#lucky_flower#.'],
    'lucky_number': ['Lucky number: #number#', 'Lucky numbers: #number# #number#',
                     'Lucky number: #cheese#'],
    'number': map(lambda x:("{:02d}".format(x)), range(0,100)),
    'lucky_colour': ['Lucky colour: #horse_colour#'],
    'horse_colour': horse_colour,
    'lucky_animal': ['Lucky animal: #beast#'],
    'lucky_flower': ['Lucky flower: #poisonous_plant#'],
    'beast': ['#godzilla#', '#rodent#', '#amphibian#', '#pest#', '#primate#'],
    'godzilla': godzilla,
    'rodent': rodent,
    'amphibian': amphibian,
    'pest': pest,
    'primate': primate,
    'lucky_element': ['Lucky element: #element#'],
    'element': element,
    'town': town,
    'village': village,
    'zodiac': zodiac,
    'got_house': got_house,
    'poisonous_plant': terms['poisonous_plant'],
    'cheese': terms['cheese'],
    'capital': terms['capital']
}

# Write the grammar out to json
with open(args.output,'w') as f:
    json.dump(rules,f,indent=4)
    
