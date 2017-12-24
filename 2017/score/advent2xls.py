#!/usr/bin/env python

import sys
import json
import pprint
from datetime import datetime,timedelta

def readscore(scorefile):
    with open(scorefile, 'r') as f:
        return json.load(f)

# 2017-12-10T20:06:03-0500'
STRFORMAT = "%Y-%m-%dT%H:%M:%S-%zZ"

def dt_parse(t):
    ret = datetime.strptime(t[0:16],'%Y-%m-%dT%H:%M')
    if t[18]=='+':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[18]=='-':
        ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret

def get_star_times(member, part):
    yield member['name']
    yield member['global_score']
    yield member['local_score']
    yield member['stars']
    yield part
    levels = member['completion_day_level']
    for x in xrange(1, 26):
        try:
            yield dt_parse(levels[str(x)][str(part)]['get_star_ts'])
        except KeyError:
            yield ''


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s scorefile" % (sys.argv[0],)
        sys.exit(1)
    score = readscore(sys.argv[1])
    #print json.dumps(score, sort_keys=True, indent=4)

    #pprint.pprint(score)
 
    print ','.join(['Name', 'Global', 'Local', 'Stars', 'Part'] + [ str(x) for x in xrange(1, 26)])
    for member in score['members'].values():
        for part in ('1', '2'):
            print ','.join(str(col) for col in get_star_times(member, part))
