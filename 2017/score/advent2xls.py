#!/usr/bin/env python

import sys
import json
import pprint
import xlsxwriter
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


def get_star_times(jsmember, part):
    levels = jsmember['completion_day_level']
    for x in xrange(1, 26):
        try:
            yield dt_parse(levels[str(x)][str(part)]['get_star_ts'])
        except KeyError:
            yield None

def to_member_dict(mid, jsmember):
    '''
        Member dictionary has:
           name
           global_score
           local_score
           stars
           1: [ date|None, date|None, ...]
           2: [ date|None, date|None, ...]

        Date/times are indexed on level.  If unsolved, datetime is None
     '''

    member = {}
    for x in ['name', 'global_score', 'local_score', 'stars']:
        member[x] = jsmember[x]
    if not member['name']:
        member['name'] = mid
    

    member['1'] = [ d for d in get_star_times(jsmember, '1') ]
    member['2'] = [ d for d in get_star_times(jsmember, '2') ]
    return member



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s scorefile" % (sys.argv[0],)
        sys.exit(1)
    # Read advent json
    score = readscore(sys.argv[1])

    # convert to a simpler dictionary
    members = [ to_member_dict(k, v) for k, v in score['members'].items() ]

    pprint.pprint(members)
