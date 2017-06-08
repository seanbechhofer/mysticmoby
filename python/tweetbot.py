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

import boto.s3
from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Twitter character limit
LIMIT = 140

# Max number of attempts
ATTEMPTS = 10

# Construct a tweet replying to a user
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
    return api.GetMentions(since_id=since,count=100)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate Tweets.')
    parser.add_argument('-c', '--config', help='configuration file', default="config.json")
    parser.add_argument('-n', '--notweet', help='no tweeting', action="store_true")
    parser.add_argument('-d', '--debug', help='debug', action="store_true")

    args = parser.parse_args()

    config = json.load(open(args.config))

    consumer_key=os.environ['API_KEY']
    consumer_secret=os.environ['API_SECRET']
    access_token_key=os.environ['ACCESS_TOKEN']
    access_token_secret=os.environ['ACCESS_SECRET']
    aws_access_key=os.environ['AWS_ACCESS_KEY']
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']

    # Connect to S3
    aws_connection = boto.s3.connect_to_region('eu-west-2',
       aws_access_key_id=aws_access_key,
       aws_secret_access_key=aws_secret_access_key,
       is_secure=True,               # uncomment if you are not using ssl
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )

    # Get the moby bucket    
    print aws_connection
    bucket = aws_connection.get_bucket('mystic-moby-tweetbot')
    print bucket

    # Get since.id file contents. Should contain the id of the last tweet that I made
    # This should ensure that each tweet is only replied to once. 
    key = Key(bucket)
    key.key = 'since.id'
    since = key.get_contents_as_string()

    lastTweet = int(since)
    print lastTweet
    
    grammar = config['grammar']
    production = config['production']
    frequency = config['frequency']

    print "Grammar: {}, production: {}".format(grammar, production)
    
    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret)
    account_name = api.VerifyCredentials().screen_name

    print "Verified: {}".format((account_name))
    # Find mentions of me. This will only pick up a limited number of
    # tweets, so if I become really popular, it may miss things.
    mentions = get_mentions(api,lastTweet)
    print mentions
    for mention in mentions:
        # For each mention reply
        print mention.id
        print mention.user.screen_name
        tweetText = tweet(to_user=mention.user.screen_name,grammar=grammar,production=production)
        if tweetText == "":
            print "Unsuccessful Generation"
        else:
            if args.notweet or args.debug:
                print "Not tweeted"
                print tweetText
            else:
                # Post update
                status = api.PostUpdate(tweetText, in_reply_to_status_id=mention.id)
                print "http://twitter.com/{}/status/{}".format(account_name, status.id)
                print status.text
                # Store id of tweet in S3
                key.set_contents_from_string(str(status.id))
            
                

            
