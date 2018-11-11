import random
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob

raw_dir = 'data/data_Q4_2016'
fail_csv = 'data_Q4_2016_fail.csv'
fails = pd.read_csv(fail_csv)
num_fails = len(fails.index)

raw_files = glob(os.path.join(raw_dir, '*.csv'))
num_raw = len(raw_files)

train = fails

count = 0
while count < num_fails:
    rand_file = random.choice(raw_files)
    df = pd.read_csv(rand_file)
    rand_row = df.sample(1)

    if not rand_row['failure'].any():
        print(count, 'Sampled', rand_file)
        train = train.append(rand_row)
        count = count + 1

train.to_csv('data_Q4_2016_train.csv')
