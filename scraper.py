#!/usr/bin/env python

import csv
import shlex
import subprocess

from utils import cartesian, flatten, is_valid_query, pairwise


# Get the hashtags for parties and topics

topic_hashtags = 'topics/economyShort.csv'
party_hashtags = 'parties/republicansHashtagsShort.csv'

with open(party_hashtags) as f:
    party_reader = csv.reader(f)
    parties = flatten(list(party_reader))

with open(topic_hashtags) as f:
    topic_reader = csv.reader(f)
    topics = flatten(list(topic_reader))


# Build the topic lists in order to fit them in the queries

def group_topics(parties, topics):
    topic_lists = []
    while topics:
        topic_list = []
        for t in topics:
            if is_valid_query(parties, topic_list + [t]):
                topic_list.append(t)
            else:
                topic_lists.append(topic_list)
                topics = list(set(topics) - set(topic_list))
                print topics
                break
        if topic_list == topics:
            topic_lists.append(topic_list)
            break
    return topic_lists


# Build the Twitter queries

names = []
queries = []
for p1, p2 in pairwise(parties):
    party_list = [p1, p2]
    topic_lists = group_topics(party_list, topics)
    for topic_list in topic_lists:
        query_total = ''
        couples = cartesian([party_list, topic_list])
        for party, topic in couples:
            query = '((' + party + ' OR #' + party + ') (' + topic + ' OR #' + topic + '))'
            if not query_total:
                query_total = query
            else:
                query_total = query_total + ' OR ' + query
        names.append('#'.join(party_list + topic_list))
        queries.append(query_total)

# Launch the scraping processes

db_name = 'trump' # TODO pass as param of the script
for i, query in enumerate(queries):
    scraper_command = 'twitter-scraper-cli -q ' + '"' + query + '" -T twitterconfig.json -d ' + db_name + ' -c ' + names[i]
    args = shlex.split(scraper_command)
    if len(query) <= 500:
        print 'Launching scraping process for query ' + query
        subprocess.Popen(args)
    else:
        print 'WARNING: the query ' + query +' is too long!'
print 'Done!'
