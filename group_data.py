import os
import string
import sys
import json

from collections import Counter
from collections import OrderedDict
import operator

grouped_data = {}

def print_od(od):
    dd = OrderedDict(sorted(od.items(), key=lambda x: x[1], reverse=True))
    return json.dumps(dd)

def add_to_group(line_vals):
    key = line_vals.keys()[0]
    if key not in grouped_data.keys():
        grouped_data[key] = line_vals[key]
    else:
        grouped_data[key]["hs2_instance"] = Counter(grouped_data[key]["hs2_instance"]) + Counter(line_vals[key]["hs2_instance"])
        grouped_data[key]["duration_min"] = grouped_data[key]["duration_min"] if grouped_data[key]["duration_min"] < line_vals[key]["duration_min"] else line_vals[key]["duration_min"]
        grouped_data[key]["duration_max"] = grouped_data[key]["duration_max"] if grouped_data[key]["duration_max"] > line_vals[key]["duration_max"] else line_vals[key]["duration_max"]
        grouped_data[key]["count"] = grouped_data[key]["count"] + 1
        grouped_data[key]["duration_total"] = grouped_data[key]["duration_total"] + line_vals[key]["duration_min"]
        grouped_data[key]["jobs"] = grouped_data[key]["count"] + line_vals[key]["jobs"]
        grouped_data[key]["engine"] = Counter(grouped_data[key]["engine"]) + Counter(line_vals[key]["engine"])
        grouped_data[key]["reads"] = Counter(grouped_data[key]["reads"]) + Counter(line_vals[key]["reads"])
        grouped_data[key]["writes"] = Counter(grouped_data[key]["writes"]) + Counter(line_vals[key]["writes"])

def filter_control(d):
    fd = OrderedDict()
    for k,v in d.items():
        if 'ctrl' in k or 'ctl' in k or 'config' in k or 'status' in k:
            fd[k] = v
    return fd

file_handle = open('new_output.txt', 'r')
lines = file_handle.readlines()
for line in lines:
    f = line.split('\t')
    reads_od = OrderedDict()
    writes_od = OrderedDict()
    for t in f[7].lower().split('#'):
        if len(t) > 1:
            reads_od[t] = reads_od[t] + 1 if t in reads_od.keys() else 1
    for t in f[8].lower().split('#'):
        if len(t) > 1:
            writes_od[t] = writes_od[t] + 1 if t in writes_od.keys() else 1

    line_vals = {f[9][0:100].lower(): {"hs2_instance":OrderedDict([(f[0].lower(),1)]), "duration_min":int(f[3]), "duration_max":int(f[3]), "duration_total":int(f[3]),
                                       "count":1, "jobs":len(f[4].split('#')), "engine": OrderedDict([(f[5].lower(),1)]), "reads": reads_od, "writes": writes_od } }
    add_to_group(line_vals)

for key in grouped_data.keys():
    cols = []



    cols.append(key)
    cols.append(print_od(grouped_data[key]['hs2_instance']))
    cols.append(str(grouped_data[key]['duration_min'] / 1000.0))
    cols.append(str(grouped_data[key]['duration_total'] / grouped_data[key]['count'] / 1000.0))
    cols.append(str(grouped_data[key]['duration_max'] / 1000.0))
    cols.append(str(grouped_data[key]['duration_total'] / 1000.0))
    cols.append(str(grouped_data[key]['count']))
    cols.append(str(grouped_data[key]['jobs']))
    cols.append(print_od(grouped_data[key]['engine']))
    cols.append(str(len(grouped_data[key]['reads'].keys())))
    cols.append(str(len(grouped_data[key]['writes'].keys())))
    cols.append(print_od(grouped_data[key]['reads']))
    cols.append(print_od(grouped_data[key]['writes']))
    control_reads = print_od(filter_control(grouped_data[key]['reads']))
    control_writes = print_od(filter_control(grouped_data[key]['writes']))
    cols.append(str(1 if len(control_reads) > 2 or len(control_writes) > 2 else 0))
    cols.append(control_reads)
    cols.append(control_writes)
    print '\t'.join(cols).replace('\n','')
