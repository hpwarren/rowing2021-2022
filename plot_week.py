#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def stats(w, h):
    mean = np.mean(w)
    std = np.std(w)
    p = 100*std/mean
    hr = np.median(h)
    print(f' mean = {mean:6.1f} std = {std:6.1f} percent = {p:6.1f} % med HR = {hr}')
    return mean, std, p

if '--total' in sys.argv:
    dirs = Path().cwd().glob('week*')
    dirs = sorted(list(dirs))
    sum = 0
    for d in dirs:
        files = d.glob('*.csv')
        files = sorted(list(files))
        nfiles = len(files)
        sum += nfiles
        print(f'{d.name} {nfiles:4d} {nfiles*3:4d} {sum:4d} {sum*3:4d}')
    exit()

week = 1
if len(sys.argv) > 1:
    week = int(sys.argv[1])

path = f'week{week:02d}'
target = 210 + 5*(week-1)
print(path, target)

files = Path(path).glob('*.csv')
files = sorted(list(files))

df_list = []
for f in files:
    df = pd.read_csv(f)
    df_list.append(df)

num_2ks = 3*len(df_list)    
print(f" total number of 2k's = {num_2ks}")
    
fig, ax = plt.subplots(figsize=(10,4))

ww, hh = None, None
for df in df_list:
    t = df['Time (seconds)']
    d = df['Distance (meters)']
    w = df['Watts']
    h = df['Heart Rate']

    t = t.to_numpy()
    d = d.to_numpy()
    w = w.to_numpy()
    h = h.to_numpy()

    m = np.isfinite(w)
    t = t[m]
    d = d[m]
    w = w[m]
    h = h[m]

    m, = np.where((d < 2000) & (w >=150))
    t = t[m]
    d = d[m]
    w = w[m]
    h = h[m]

    s = stats(w, h)
    
    if ww is None:
        ww = w
        hh = h
    else:
        ww = np.append(ww, w)
        hh = np.append(hh, h)

    plt.scatter(t, w, s=12)

print(' all data')    
s = stats(ww, hh)

plt.xlim((-25,480))
plt.ylim((150,350))
plt.xlabel('Time (sec)')
plt.ylabel('Watts')
plt.title(f"{path} | num 2k's = {num_2ks} | target watts = {target} | $\sigma$ = {s[2]:0.1f}%")

ax.axvline(x=420, ymin=0, ymax=150/200)
plt.text(420, 307, 'Goal 300w', va='center', ha='center')

ax.axhline(target)
plt.text(-10, target-7, f'{target}w', va='center', ha='center')

plt.tight_layout()
plt.savefig(f'plot_{path}.png')
plt.show()


