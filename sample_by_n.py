import random
import os
import math
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
from datetime import datetime, timedelta

n = 10


data_path = "data/2015_n"
nom_out = "samples/2015_nominal_samples_n{}_inf.csv".format(n)
gray_out = "samples/2015_gray_samples_n{}_inf.csv".format(n)
fail_out = "samples/2015_failure_samples_n{}_inf.csv".format(n)

samples_per_file = 10

files = glob(os.path.join(data_path, '*.csv'))

feature_columns = ['smart_1_raw', 'smart_3_raw', 'smart_4_raw', 'smart_5_raw',
           'smart_7_raw','smart_12_raw', 'smart_194_raw',
           'smart_197_raw', 'smart_198_raw', 'smart_199_raw']

wanted_columns = ['model', 'gray_n'] + feature_columns

nominal_sample = pd.DataFrame()
gray_sample = pd.DataFrame()
fail_sample = pd.DataFrame()

for i, file in enumerate(files):
    print("[{}/{}] {}".format(i, len(files), file))

    all = pd.read_csv(file)
    all = all[np.logical_not(all[wanted_columns].isnull().any(axis=1))]
    # noms = all[np.logical_or(all['gray_n'] > n, all['gray_n'] == -1)]
    noms = all[all['gray_n'] == -1]
    grays = all[np.logical_and(all['gray_n'] <= n, all['gray_n'] > 0)]
    fails = all[all['gray_n'] == 0]

    nominal_sample = nominal_sample.append(noms.sample(samples_per_file))
    gray_sample = gray_sample.append(grays)
    fail_sample = fail_sample.append(fails)

print("Saving samples to:\n{} {}\n{} {}\n{} {}".format(
    nom_out, len(nominal_sample.index),
    gray_out, len(gray_sample.index),
    fail_out, len(fail_sample.index)))

nominal_sample.to_csv(nom_out, index=False)
gray_sample.to_csv(gray_out, index=False)
fail_sample.to_csv(fail_out, index=False)
