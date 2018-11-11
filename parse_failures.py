import os
import pandas as pd
from glob import glob

dir = "/Users/eric/Downloads/data_Q4_2016"

all_fail = pd.DataFrame()

count = 0
for file in glob(os.path.join(dir, "*.csv")):
    all = pd.read_csv(file)
    fails = all[all['failure'] == 1]
    print(len(fails.index), "failures from", file)
    all_fail = all_fail.append(fails)
    count = count + 1

all_fail.to_csv("data_Q4_2016_fail.csv", index=False)
