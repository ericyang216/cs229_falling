import os
import argparse
import json
import pandas as pd
from glob import glob
from datetime import datetime, timedelta

pd.options.mode.chained_assignment = None

path = 'data/2015/'
out_path = 'data/2015_n'

fail_csv = '2015_failures.csv'
fail_df = pd.read_csv(fail_csv)

files = glob(os.path.join(path, "*.csv"))

fail_list = fail_df['serial_number'].tolist()

for i, file in enumerate(files):
    print('[{}/{}] Calculating gray n for {}'.format(i, len(files), file))
    gray_n = []

    df = pd.read_csv(file)
    for index, row in df.iterrows():
        curr_date = row['date']
        sn = row['serial_number']
        # print(fail_row)

        if not sn in fail_list:
            # -1 means this sn did not fail for a long time (n is very large)
            gray_n.append(-1)
        else:
            fail_date = fail_df.loc[fail_df['serial_number'] == sn]['date'].iloc[0]

            delta_date = datetime.strptime(fail_date, '%Y-%m-%d') \
                         - datetime.strptime(curr_date, '%Y-%m-%d')
            n = delta_date.days

            # means this sn must be refurbished?
            if n < 0:
                gray_n.append(-1)
            else:
                gray_n.append(n)

    df['gray_n'] = gray_n
    df.to_csv(os.path.join(out_path, os.path.basename(file)), index=False)
