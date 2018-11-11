import random
import os
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob

data_path = "data/2015"
fail_path = '%s_failures.csv' % os.path.basename(data_path)
out_path = '%s_sample.csv' % os.path.basename(data_path)

def rand_undersample(args):
    samp = pd.DataFrame()
    fails = pd.read_csv(args.fail)
    num_fails = len(fails.index)

    files = glob(os.path.join(args.path, '*.csv'))

    # Oversample per file
    samp_per_file = math.ceil(num_fails/len(files)) * 2
    i = 0
    
    for file in files:
        try:
            df = pd.read_csv(file)
            s = df[df['failure'] == 0].sample(samp_per_file)
            i = i + samp_per_file
            print("[{}/{}] nominal sample from {}".format(i, num_fails, file))
            samp = samp.append(s)
        except KeyboardInterrupt:
            break
        except:
            continue

    # Resample to exact amount
    samp = samp.sample(num_fails)

    print("Saving {} samples to {}".format(num_fails, args.out))
    samp.to_csv(args.out, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create training csv by combining failures and sampling nominal data')
    parser.add_argument('-f', '--fail', default=fail_path, help='fail csv')
    parser.add_argument('-p', '--path', default=data_path, help='path to data directory')
    parser.add_argument('-o', '--out', default=out_path, help='output file name (xxx.csv)')

    args = parser.parse_args()
    rand_undersample(args)
