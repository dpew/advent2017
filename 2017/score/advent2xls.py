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

def partdatecmp(a, b):
    if a[1] and b[1]:
        return cmp(a[1], b[1])
    if a[1]:
        return -1
    if b[1]:
        return 1
    return cmp(a[0], b[0])


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

    member = { 'id': mid }
    for x in ['name', 'global_score', 'local_score', 'stars']:
        member[x] = jsmember[x]
    if not member['name']:
        member['name'] = mid
    

    member['1'] = [ d for d in get_star_times(jsmember, '1') ]
    member['2'] = [ d for d in get_star_times(jsmember, '2') ]
    return member

def members2levels(members, level, part):
    '''
        members - iterable of member dictionary
        level - zero based level (e.g. 0 == advent level 1)
        Returns a level list:
          [(name, date, localscore), (name, date, localscore), ...]
    '''
    levels=[ (m['name'], m[str(part)][level]) for m in members ]
    levels.sort(cmp=partdatecmp)
    size=len(levels)
    return [(l[0], l[1], size - e if l[1] else 0) for e, l in enumerate(levels)]

def p(x):
#    print "VALUE", x
    return x

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s scorefile" % (sys.argv[0],)
        sys.exit(1)
    # Read advent json
    score = readscore(sys.argv[1])

    # convert to a simpler dictionary
    members = [ to_member_dict(k, v) for k, v in score['members'].items() ]
    part1 = [ members2levels(members, l, 1) for l in xrange(25) ]
    part2 = [ members2levels(members, l, 2) for l in xrange(25) ]


    #pprint.pprint(part2)
    for m in members:
        print m['name'], sum(p(filter(lambda x: p(x)[0] == m['name'], level)[0][2]) for level in part1) + sum(p(filter(lambda x: p(x)[0] == m['name'], level)[0][2]) for level in part2)
    #pprint.pprint(part2)

   
