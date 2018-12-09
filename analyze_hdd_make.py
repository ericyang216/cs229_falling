import os
import argparse
import json
import pandas as pd
from glob import glob
from datetime import datetime, timedelta

hdd_make_model_dict = {}

fail_df = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2015_failures.csv')
nom_df = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2015_sample.csv')
all = pd.concat([fail_df, nom_df])

df = all[all['model'].str.startswith('ST')]
df.min(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/st_min.csv')
df.max(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/st_max.csv')

df = all[all['model'].str.startswith('WD')]
df.min(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/wd_min.csv')
df.max(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/wd_max.csv')

df = all[all['model'].str.startswith('TOSHIBA')]
df.min(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/to_min.csv')
df.max(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/to_max.csv')

df = all[all['model'].str.startswith('Hitachi')]
df.min(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/hi_min.csv')
df.max(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/hi_max.csv')

df = all[all['model'].str.startswith('HGST')]
df.min(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/hg_min.csv')
df.max(skipna=True).to_csv('/Users/eric/git/cs229/cs229_falling/hg_max.csv')
