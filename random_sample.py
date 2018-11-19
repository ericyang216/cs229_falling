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

def rand_undersample(args):
    samp = pd.DataFrame()
    fails = pd.read_csv(args.fail)
    num_fails = len(fails.index)

    files = glob(os.path.join(args.path, '*.csv'))

    if args.json:
        with open(args.json, 'r') as f:
            fail_date_dict = json.load(f)
        print("Loaded {}".format(args.json))


    # Oversample per file
    samp_per_file = math.ceil(num_fails/len(files)) * 2
    i = 0

    for file in files:
        # try:
        df = pd.read_csv(file)
        curr_date = df['date'][1]

        fail_sns = []
        for d in range(args.nday + 1):
            next_datetime = datetime.strptime(curr_date, '%Y-%m-%d') + timedelta(days=d)
            next_day = next_datetime.strftime('%Y-%m-%d')
            if next_day in fail_date_dict:
                fail_sns = fail_sns + fail_date_dict[next_day]

        s = df[~df['serial_number'].isin(fail_sns)].sample(samp_per_file)
        i = i + samp_per_file
        # print(s['failure'])
        print("[{}/{}] nominal sample from {}".format(i, num_fails, file))
        samp = samp.append(s)
        # except KeyboardInterrupt:
        #     break
        # except:
        #     continue

    # Resample to exact amount
    samp = samp.sample(num_fails)

    print("Saving {} samples to {}".format(num_fails, args.out))
    samp.to_csv(args.out, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create training csv by combining failures and sampling nominal data')
    parser.add_argument('-f', '--fail', required=True, help='fail csv')
    parser.add_argument('-p', '--path', required=True, help='path to data directory')
    parser.add_argument('-o', '--out', required=True, help='output file name (xxx.csv)')
    parser.add_argument('-j', '--json', required=True, help='failure sn dates json')
    parser.add_argument('-n', '--nday', required=True, type=int, help='smooth additional n day as failure')

    args = parser.parse_args()
    rand_undersample(args)
