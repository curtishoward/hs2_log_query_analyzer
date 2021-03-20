import sys

read_agg = {}
write_agg = {}

for line in sys.stdin:
    f = line.split('\t')
    duration = float(f[3])

    for t in f[7].lower().split('#'):
        if len(t) > 1:
            if t not in read_agg.keys():
                read_agg[t] = {'factor':0.0, 'count':0}
            read_agg[t]['factor'] = read_agg[t]['factor'] + duration
            read_agg[t]['count']  = read_agg[t]['count'] + 1

    for t in f[8].lower().split('#'):
        if len(t) > 1:
            if t not in write_agg.keys():
                write_agg[t] = {'factor':0.0, 'count':0}
            write_agg[t]['factor'] = write_agg[t]['factor'] + duration
            write_agg[t]['count']  = write_agg[t]['count'] + 1


for k in read_agg.keys():
    print '\t'.join(['R', k, str(read_agg[k]['factor']), str(read_agg[k]['count'])])

for k in write_agg.keys():
    print '\t'.join(['W', k, str(write_agg[k]['factor']), str(write_agg[k]['count'])])
