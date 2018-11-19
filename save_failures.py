import os
import argparse
import json
import pandas as pd
from glob import glob
from datetime import datetime, timedelta

pd.options.mode.chained_assignment = None


def save_failures(args):
    files = glob(os.path.join(args.path, "*.csv"))

    fail_date_dict = {}

    if args.json:
        with open(args.json, 'r') as f:
            fail_date_dict = json.load(f)
        print("Loaded {}".format(args.json))

    else:
        for i, file in enumerate(files):
            all = pd.read_csv(file)
            fails = all[all['failure'] == 1]
            fails = fails[fails['capacity_bytes'] > 0]

            date = all['date'][1]
            fail_date_dict[date] = list(fails['serial_number'])

            print('[{}/{}] {} failing serial numbers in {}'\
                  .format(i, len(files), len(list(fails['serial_number'])), file))

        print("Saving sn_date_failures.json")
        with open('sn_date_failures.json', 'w') as outfile:
            json.dump(fail_date_dict, outfile, indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)

    all_fail = pd.DataFrame()
    num_fail = 0

    for date_key in fail_date_dict:

        print("Backtracking {} day(s) for date {} ({} failures)"\
              .format(args.nday, date_key, len(fail_date_dict[date_key])))

        fail_dates = []
        for i in range(args.nday + 1):
            date = datetime.strptime(date_key, '%Y-%m-%d') - timedelta(days=i)
            fail_dates.append(date.strftime('%Y-%m-%d'))

        for date in fail_dates:
            # print("{} - finding failing serial numbers".format(date))
            file = os.path.join(args.path, date + ".csv")

            try:
                all = pd.read_csv(file)

                sns = fail_date_dict[date_key]
                fails = all[all['serial_number'].isin(sns)]

                if not fails.empty:
                    fails.loc[:, 'failure'] = 1
                    all_fail = all_fail.append(fails)
                    num_fail = num_fail + len(fails)

            except KeyboardInterrupt:
                exit()
            except:
                continue

    print("Saving {} failures to {}".format(num_fail, args.out))
    all_fail.to_csv(args.out, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse all data and save all failures to single csv')
    parser.add_argument('-p', '--path', required=True, help='path to data directory')
    parser.add_argument('-o', '--out', required=True, help='output file name (xxx.csv)')
    parser.add_argument('-n', '--nday', required=True, type=int, help='smooth additional n day as failure')
    parser.add_argument('-j', '--json', required=False, default=None, help='failure sn dates json')
    args = parser.parse_args()
    save_failures(args)
