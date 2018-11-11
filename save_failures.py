import os
import argparse
import pandas as pd
from glob import glob

data_path = "data/2015"
out_path = '%s_failures.csv' % os.path.basename(data_path)

def save_failures(args):
    all_fail = pd.DataFrame()

    i = 1
    data_size = 0
    fail_size = 0

    files = glob(os.path.join(args.path, "*.csv"))
    for file in files:
        all = pd.read_csv(file)
        fails = all[all['failure'] == 1]

        print("[{}/{}] {} failures from {}".format(i, len(files), len(fails.index), file))

        all_fail = all_fail.append(fails)

        data_size = data_size + len(all.index)
        fail_size = fail_size + len(fails.index)
        i = i + 1

    print("{} failures / {} total samples".format(fail_size, data_size))
    print("Saving failures to {}".format(args.out))
    all_fail.to_csv(args.out, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse all data and save all failures to single csv')
    parser.add_argument('-p', '--path', default=data_path, help='path to data directory')
    parser.add_argument('-o', '--out', default=out_path, help='output file name (xxx.csv)')

    args = parser.parse_args()
    save_failures(args)
