#!/usr/bin/env python

import sys
import json
import pprint
import itertools
from collections import defaultdict
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

def sum_level(part1, part2):
    sums=defaultdict(lambda: 0)
    for x in itertools.chain(part1, part2):
        sums[x[0]] += x[2]
    return sorted([(p[0], sums[p[0]]) for p in part1], key=lambda x: (-x[1], x[0]))

def scores2dict(partscores):
    '''
        scores - [[(name, date, value), (name, date, value), ...]]
        returns
           { name0: [ value0, value1, ... valueN ],
             name1  [ value0, value1, ... valueN ],
           }
    '''
    d = defaultdict(lambda: [0] * len(partscores))
    
    for e, level in enumerate(partscores):
        for score in level:
            d[score[0]][e] = score[2]

    return dict(d)

def runningsum(iterable):
    s = 0
    for x in iterable:
        s+=x
        yield s

def wb_write_part_dates(worksheet, members, key, dateformat):
    for l in xrange(25):
        worksheet.write(0, l + 1, l + 1)

    for r, m in enumerate(sorted(members.values(), key=lambda x: x['name'])):
        worksheet.write(r+1, 0, m['name'])
        for l in xrange(25):
            worksheet.write(r+1, l+1, m[key][l], dateformat)

def wb_write_part_scores(worksheet, members, key, dateformat):
    for l in xrange(25):
        worksheet.write(0, l + 1, l + 1)

    for r, m in enumerate(sorted(members.values(), key=lambda x: x['name'])):
        worksheet.write(r+1, 0, m['name'])
        for l in xrange(25):
            worksheet.write(r+1, l+1, m[key][l], numformat)


def write_data(members, filename):
    import xlsxwriter
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("Summary")

    COLS =  ('id', 'name', 'local_score', 'global_score', 'stars')
    for c, name in enumerate(COLS):
        worksheet.write(0, c, name)

    for r, m in enumerate(sorted(members.values(), key=lambda x: x['name'])):
        for c, name in enumerate(COLS):
            worksheet.write(r+1, c, m[name])

    dateformat = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
    numformat = workbook.add_format({'num_format': '0'})
    wb_write_part_dates(workbook.add_worksheet("Dates 1"), members, '1', dateformat) 
    wb_write_part_dates(workbook.add_worksheet("Dates 2"), members, '2', dateformat) 
    wb_write_part_dates(workbook.add_worksheet("Scores 1"), members, 'scores-1', numformat) 
    wb_write_part_dates(workbook.add_worksheet("Scores 2"), members, 'scores-2', numformat) 
    wb_write_part_dates(workbook.add_worksheet("Scores 1+2"), members, 'scores', numformat) 
    wb_write_part_dates(workbook.add_worksheet("Scores C"), members, 'scores-cumulative', numformat) 
    wb_write_part_dates(workbook.add_worksheet("Stars"), members, 'scores-stars', numformat) 
    workbook.close()
    

def p(x):
#    print "VALUE", x
    return x

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s scorefile [outfile]" % (sys.argv[0],)
        sys.exit(1)

    # Read advent json
    score = readscore(sys.argv[1])

    # convert to a simpler member dictionary
    memberlist = [ to_member_dict(k, v) for k, v in score['members'].items() ]
    members = dict((m['name'], m) for m in memberlist)

    # Compute local scores per level
    part1 = [ members2levels(members.values(), l, 1) for l in xrange(25) ]
    part2 = [ members2levels(members.values(), l, 2) for l in xrange(25) ]
    #both = [ sum_level(p1, p2) for p1, p2 in zip(part1, part2) ]

    # Roll local scores into each member 
    for k, v in scores2dict(part1).items():
       members[k]['scores-1'] = v
    for k, v in scores2dict(part2).items():
       members[k]['scores-2'] = v

    # Now sum up scores 
    for n, m in members.items():
        m['scores'] = map(sum, zip(m['scores-1'], m['scores-2']))
        m['scores-cumulative'] = list(runningsum(m['scores']))
        m['scores-stars'] = map(sum, zip((1 if x else 0 for x in m['1']), (1 if x else 0 for x in m['2'])))


    if len(sys.argv) > 2:
        write_data(members, sys.argv[2])
    else:
        pprint.pprint(members)
    sys.exit(0)
