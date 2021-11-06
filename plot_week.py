#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def stats(w):
    mean = np.mean(w)
    std = np.std(w)
    p = 100*std/mean
    print(f' mean = {mean:6.1f} std = {std:6.1f} percent = {p:6.1f} %')

week = 1
if len(sys.argv) > 1:
    week = int(sys.argv[1])

if week == 1:
    path = 'week01'
    target = 210
elif week == 2:
    path = 'week02'
    target = 215
elif week == 3:
    path = 'week03'
    target = 220

files = Path(path).glob('*.csv')
files = sorted(list(files))

df_list = []
for f in files:
    df = pd.read_csv(f)
    df_list.append(df)

num_2ks = 3*len(df_list)    
print(f" total number of 2k's = {num_2ks}")
    
fig, ax = plt.subplots(figsize=(10,4))

yy = None
for df in df_list:
    t = df['Time (seconds)']
    d = df['Distance (meters)']
    w = df['Watts']

    t = t.to_numpy()
    d = d.to_numpy()
    w = w.to_numpy()

    m = np.isfinite(w)
    t = t[m]
    d = d[m]
    w = w[m]    

    m, = np.where((d < 2000) & (w >=150))
    t = t[m]
    d = d[m]
    w = w[m]

    stats(w)
    
    if yy is None:
        yy = w
    else:
        yy = np.append(yy, w)

    plt.scatter(t, w, s=12)

print(' all data')    
stats(yy)

plt.ylim((-10,480))
plt.ylim((150,350))
plt.xlabel('Time (sec)')
plt.ylabel('Watts')
plt.title(f"{path} | num 2k's = {num_2ks} | target watts = {target}")

ax.axvline(x=420, ymin=0, ymax=150/200)
plt.text(420, 310, 'Goal 300w', va='center', horizontalalignment='center')

ax.axhline(target)
plt.text(478, target-10, f'{target}w', horizontalalignment='center')

plt.tight_layout()
plt.savefig(f'plot_{path}.png')
plt.show()


