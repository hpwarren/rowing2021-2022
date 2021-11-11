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
    return mean, std, p

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

    s = stats(w)
    
    if yy is None:
        yy = w
    else:
        yy = np.append(yy, w)

    plt.scatter(t, w, s=12)

print(' all data')    
stats(yy)

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


