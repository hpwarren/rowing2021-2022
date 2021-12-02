#!/usr/bin/env python

import sys

def convert_sec2str(pace):
    pace_min = int(pace / 60)
    pace_sec = pace - pace_min*60
    pace_sec_int= int(pace_sec)
    pace_sec_frac = int(10*(pace_sec - pace_sec_int))
    out = f'{pace_min}:{pace_sec_int:02d}.{pace_sec_frac}'
    return out

watts = 300
if len(sys.argv) > 1:
    watts = int(sys.argv[1])

pace = 500*(2.8/watts)**0.3333

split = convert_sec2str(pace)
time = convert_sec2str(pace*4)

print(f' watts = {watts:d}')
print(f' split = {split}')
print(f'  time = {time}')
