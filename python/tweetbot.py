#!/usr/local/bin/python
"""Generate reports from a tracery grammar"""
__author__ = "Sean Bechhofer"
__copyright__ = "Copyright 2016, Sean Bechhofer"
__credits__ = ["Sean Bechhofer"]
import json
import argparse
import twitter
import tracery
from tracery.modifiers import base_english
import twitter
import os
from random import randint

# Twitter character limit
LIMIT = 140

# Max number of attempts
ATTEMPTS = 10

def tweet(to_user,grammar, production):
    stuff = ""
    with open(grammar) as f:
        rules = json.load(f)
    
        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)

        stuff = '@' + to_user + ' ' + grammar.flatten("#" + production + "#")
        count = 0
        while len(stuff) > LIMIT and count < ATTEMPTS:
            print "Re-rolling..."
            stuff = '@' + to_user + ' ' + grammar.flatten("#" + production + "#")
            count += 1
    if len(stuff) > LIMIT:
        stuff = ""
    return stuff

def get_mentions(api,since):
    return api.GetMentions(since_id=since)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate Tweets.')
    parser.add_argument('-c', '--config', help='configuration file', default="config.json")
    parser.add_argument('-n', '--notweet', help='no tweeting', action="store_true")
    parser.add_argument('-d', '--debug', help='debug', action="store_true")
    parser.add_argument('-s', '--since', help='since file', default="since.id")

    args = parser.parse_args()

    config = json.load(open(args.config))

    consumer_key=os.environ['API_KEY']
    consumer_secret=os.environ['API_SECRET']
    access_token_key=os.environ['ACCESS_TOKEN']
    access_token_secret=os.environ['ACCESS_SECRET']


    grammar = config['grammar']
    production = config['production']
    frequency = config['frequency']

    print "Grammar: {}, production: {}".format(grammar, production)
    
    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret)
    account_name = api.VerifyCredentials().screen_name

    with open(args.since, 'r') as f:
        last_known_id = f.readline()
        
    print "Verified: {}".format((account_name))
    # Find mentions of me 
    mentions = get_mentions(api,int(last_known_id))
    print mentions
    for mention in mentions:
        # For each mention reply
        print mention.id
        print mention.user.screen_name
        tweetText = tweet(to_user=mention.user.screen_name,grammar=grammar,production=production)
        if tweetText == "":
            print "Unsuccesful Generation"
        else:
            if args.notweet or args.debug:
                print "Not tweeted"
                print tweetText
            else:
                status = api.PostUpdate(tweetText, in_reply_to_status_id=mention.id)
                print "http://twitter.com/{}/status/{}".format(account_name, status.id)
                print status.text
                since_file = open(args.since, "w")
                since_file.write(str(status.id))
                since_file.close()
            
                

            
