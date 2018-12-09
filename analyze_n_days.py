import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

feature_columns = ['smart_1_raw', 'smart_3_raw', 'smart_4_raw', 'smart_5_raw',
           'smart_7_raw','smart_12_raw', 'smart_194_raw',
           'smart_197_raw', 'smart_198_raw', 'smart_199_raw']

wanted_columns = ['model', 'gray_n'] + feature_columns


def scale(data_samples):
    # Scale
    data_norm = pd.DataFrame()
    manufacturers = ['ST','Hi','WD','To','HG']
    for man in manufacturers:
        data_sub = data_samples[data_samples['model'].str.startswith(man)]
        max_ = pd.read_csv('scaling/%s_max.csv' % man.lower())
        max_.index = max_['date']
        del max_['date']
        max_.columns = ['value']
        min_ = pd.read_csv('scaling/%s_min.csv' % man.lower())
        min_.index = min_['date']
        del min_['date']
        min_.columns = ['value']
        for col in feature_columns:
            range_ = float(max_.value[col]) - float(min_.value[col])
            if range_ == 0:
                range_ = 1
            data_sub[col] = (data_sub[col] - float(min_.value[col]) )/range_
        data_norm = pd.concat([data_norm, data_sub])
    return data_norm

def get_wanted_columns(data):
    return data[wanted_columns].dropna(axis=0)

### Use pre-sampled datasets
data_path = "samples/"
sample_name_format = "2015_%s_samples_n%s.csv" # (category, n)
categories = ['failure', 'nominal', 'gray']
n_range = range(1, 10)

for n in [1]:
    print(n)

    failures = pd.read_csv(os.path.join(data_path, sample_name_format%('failure', n)))
    nominals = pd.read_csv(os.path.join(data_path, sample_name_format%('nominal', n)))
    grays = pd.read_csv(os.path.join(data_path, sample_name_format%('gray', n)))

    failures = scale(get_wanted_columns(failures))
    nominals = scale(get_wanted_columns(nominals))
    grays = scale(get_wanted_columns(grays))

    fail_mean = failures.mean(axis=0, numeric_only=True)
    fail_med = failures.median(axis=0, numeric_only=True)
    fail_min = failures.min(axis=0, numeric_only=True)
    fail_max = failures.max(axis=0, numeric_only=True)
    fail_std = failures.std(axis=0, numeric_only=True)

    nom_mean = nominals.mean(axis=0, numeric_only=True)
    nom_med = nominals.median(axis=0, numeric_only=True)
    nom_min = nominals.min(axis=0, numeric_only=True)
    nom_max = nominals.max(axis=0, numeric_only=True)
    nom_std = nominals.std(axis=0, numeric_only=True)

    gray_mean = grays.mean(axis=0, numeric_only=True)
    gray_med = grays.median(axis=0, numeric_only=True)
    gray_min = grays.min(axis=0, numeric_only=True)
    gray_max = grays.max(axis=0, numeric_only=True)
    gray_std = grays.std(axis=0, numeric_only=True)

    for feature in feature_columns:
        print(feature)
        plt.subplot(1, 3, 1)
        objects = ('Fail', 'Gray', 'Nominal')
        y_pos = np.arange(len(objects))
        means = [fail_mean[feature], gray_mean[feature], nom_mean[feature]]
        plt.bar(y_pos, means, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.title('mean')

        plt.subplot(1, 3, 2)
        objects = ('Fail', 'Gray', 'Nominal')
        y_pos = np.arange(len(objects))
        meds = [fail_med[feature], gray_med[feature], nom_med[feature]]
        plt.bar(y_pos, meds, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.title('median')

        plt.subplot(1, 3, 3)
        objects = ('Fail', 'Gray', 'Nominal')
        y_pos = np.arange(len(objects))
        maxs = [fail_max[feature], gray_max[feature], nom_max[feature]]
        plt.bar(y_pos, maxs, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.title('max')

        plt.show()
        plt.clf()





# ### Below is code that will search/sample through all data points (takes long)
# def sample_by_gray_n(df, n, samples=0):
#     mask = df['gray_n'] == n
#     if samples and samples > len(mask):
#         return df[mask].sample(samples)
#     else:
#         return df[mask]
#
# data_path = "data/2015_n"
# fail_csv = "2015_failures.csv"
# files = glob(os.path.join(data_path, "*.csv"))
#
# all_mean = pd.DataFrame()
# all_median = pd.DataFrame()
# all_min = pd.DataFrame()
# all_max = pd.DataFrame()
# all_std = pd.DataFrame()
#
# feature_columns = ['smart_1_raw', 'smart_3_raw', 'smart_4_raw', 'smart_5_raw',
#            'smart_7_raw','smart_12_raw', 'smart_194_raw',
#            'smart_197_raw', 'smart_198_raw', 'smart_199_raw']
#
# wanted_columns = ['model', 'gray_n'] + feature_columns
#
# for n in range(0, 10):
#     data_samples = pd.DataFrame()
#
#     if n == 0:
#         data_samples = pd.read_csv(fail_csv)
#         data_samples['gray_n'] = 0
#         data_samples = data_samples[wanted_columns]
#         data_samples = data_samples.dropna(axis=0)
#     else:
#         for i, file in enumerate(files):
#             print("[n={}] [{}/{}] {}".format(n, i, len(files), file))
#             data = pd.read_csv(file)
#             data = data[wanted_columns]
#             data = data.dropna(axis=0)
#             data_samples = data_samples.append(sample_by_gray_n(data, n))
#
#     # Scale
#     data_norm = pd.DataFrame()
#     manufacturers = ['ST','Hi','WD','To','HG']
#     for man in manufacturers:
#         data_sub = data_samples[data_samples['model'].str.startswith(man)]
#         max_ = pd.read_csv('scaling/%s_max.csv' % man.lower())
#         max_.index = max_['date']
#         del max_['date']
#         max_.columns = ['value']
#         min_ = pd.read_csv('scaling/%s_min.csv' % man.lower())
#         min_.index = min_['date']
#         del min_['date']
#         min_.columns = ['value']
#         for col in feature_columns:
#             range_ = float(max_.value[col]) - float(min_.value[col])
#             if range_ == 0:
#                 range_ = 1
#             data_sub[col] = (data_sub[col] - float(min_.value[col]) )/range_
#         data_norm = pd.concat([data_norm, data_sub])
#
#     data_norm['gray_n'] = n
#
#     mean = data_norm.mean(axis=0, numeric_only=True)
#     median = data_norm.median(axis=0, numeric_only=True)
#     min = data_norm.min(axis=0, numeric_only=True)
#     max = data_norm.max(axis=0, numeric_only=True)
#     std = data_norm.std(axis=0, numeric_only=True)
#
#     all_mean = all_mean.append(mean, ignore_index=True)
#     all_median = all_median.append(median, ignore_index=True)
#     all_min = all_min.append(min, ignore_index=True)
#     all_max =all_max.append(max, ignore_index=True)
#     all_std = all_std.append(std, ignore_index=True)
#
# for feature in feature_columns:
#     plt.plot(all_max['gray_n'],    all_max[feature],    label='max')
#     plt.plot(all_min['gray_n'],    all_min[feature],    label='min')
#     plt.plot(all_mean['gray_n'],   all_mean[feature],   label='mean')
#     plt.plot(all_median['gray_n'], all_median[feature], label='med')
#     plt.plot(all_std['gray_n'],    all_std[feature],    label='std')
#     plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=5,
#             borderaxespad=0, frameon=False)
#     plt.xlabel('n-th day before fail')
#     plt.ylabel('Scaled {}'.format(feature))
#     plt.savefig('n_{}_plot.png'.format(feature))
#     plt.clf()
