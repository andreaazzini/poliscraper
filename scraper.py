#!/usr/bin/env python

import csv
import shlex
import subprocess

from utils import flatten


# Get the hashtags for parties and topics

topic_hashtags = 'topics/economyShort.csv'
party_hashtags = 'parties/republicansHashtagsShort.csv'

with open(party_hashtags) as f:
    party_reader = csv.reader(f)
    party_list = flatten(list(party_reader))

with open(topic_hashtags) as f:
    topic_reader = csv.reader(f)
    topic_list = flatten(list(topic_reader))


# Build the Twitter query

query_total = ''
for party in party_list:
    for topic in topic_list:
        query = '((' + party + ' OR #' + party + ') (' + topic + ' OR #' + topic + '))'
        if not query_total:
            query_total = query
        else:
            query_total = query_total + ' OR ' + query


# Launch the scraping process

db_name = 'trump'
scraper_command = 'twitter-scraper-cli -q ' + '"' + query_total + '" -T twitterconfig.json -d ' + db_name
args = shlex.split(scraper_command)

print 'Launching scraping process for query ' + query_total
subprocess.Popen(args)
print 'Done!'
