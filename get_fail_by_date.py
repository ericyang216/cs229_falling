import os
import argparse
import json
import pandas as pd
from glob import glob
from datetime import datetime, timedelta

pd.options.mode.chained_assignment = None
path = 'data/2018/'
out = 'sn_fail_by_date.json'

files = glob(os.path.join(path, "*.csv"))

fail_date_dict = {}

for i, file in enumerate(files):
    all = pd.read_csv(file)
    fails = all[all['failure'] == 1]
    fails = fails[fails['capacity_bytes'] > 0]

    date = all['date'][1]
    fail_date_dict[date] = list(fails['serial_number'])

    print('[{}/{}] {} failing serial numbers in {}'\
          .format(i, len(files), len(list(fails['serial_number'])), file))

print("Saving {}".format(out))
with open(out, 'w') as outfile:
    json.dump(fail_date_dict, outfile, indent=4, sort_keys=True,
    separators=(',', ': '), ensure_ascii=False)
