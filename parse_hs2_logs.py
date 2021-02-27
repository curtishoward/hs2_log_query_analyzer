import json
import os
import re
import string
import sys

def match_tables(regex_str, db, j):
    return [x.encode('ascii','replace').replace('`','') if '.' in x else '.'.join([db, x.encode('ascii','replace').replace('`','')]) for x in re.findall(regex_str, j["queryText"].lower())]

def try_parse(json_obj, hs2_name):
    user      = j['user'].encode('ascii','replace')
    timestamp = str(j['timestamp']).encode('ascii','replace')
    duration  = str(j['duration']).encode('ascii','replace')
    jobIds    = [x.encode('ascii','replace') for x in j['jobIds']]
    engine    = j['engine'].encode('ascii','replace')
    db        = j['database'].encode('ascii','replace')
    reads     = match_tables(r'(?:from|join)[\s\n]+([^\(\s]+)', db, j)
    writes    = match_tables(r'(?:insert\s+overwrite\s+table|into\s+table|into|create\s+table)[\s\n]+(\S+)', db, j)
    print '\t'.join([hs2_name, user, timestamp, duration, '#'.join(jobIds), engine, db, '#'.join(reads), '#'.join(writes),  ''.join(s for s in j["queryText"] if s in string.printable).replace('`','').replace('\t', ' ').replace('\n', ' ')])

files = os.listdir("./")
for file in files:
    hs2 = re.match(r'^(.*HIVESERVER2.*).log.out.*', file)
    if hs2:
        hs2_name = hs2.group(1)
        file_handle = open(file, 'r')
        lines = file_handle.readlines()
        count = 0
        for line in lines:
            count += 1
            m = re.match(r'^.*org.apache.hadoop.hive.ql.hooks.LineageLogger:\s+\[\S+:\s+[^\]]+\]:\s+(\{.*\})\s*$', line)
            if m:
                try:
                    j = json.loads(m.group(1), strict=False)
                    try_parse(j, hs2_name)
                except Exception as e1:
                    pass
                    # print "###ERROR###: ", line, count, e1
