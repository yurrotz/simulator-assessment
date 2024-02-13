from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pickle as pk
import pandas as pd
import numpy as np
import os
import io
import re

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1t7VuJeYreATjtFCwR46DY6Q0A5TwHTm9']
file_names = ['scopus.xlsx']

def connect_to_drive(file_ids, file_names):
    for file_id, file_name in zip(file_ids, file_names):
        request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download progress {0}'.format(status.progress() * 100))

        fh.seek(0)

        with open(os.path.join('excel', file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

def eliminate_outliers(data, threshold):
    """
    :param values: values containing outliers
    :return: returns the values without outliers
    """
    z_scores = stats.zscore(data)
    list_pairing = list(zip(data, z_scores))

    for pair in list_pairing:
        if np.abs(pair[1]) > threshold:
            print(pair)
    filtered_data = [value for value, z_score in zip(data, z_scores) if np.abs(z_score) <= threshold]

    return filtered_data

if __name__ == "__main__":
    connect_to_drive(file_ids, file_names)

    pd.options.mode.copy_on_write = True

    df = pd.read_excel('excel/scopus.xlsx')

    # Not related
    print(len(df[~df['Accepted'].str.contains('ok') & ~df['Accepted'].str.contains('recall', flags=re.IGNORECASE)]['Accepted']))

    with_recall = df[(df['Recall Values'].notna()) & (df['Recall Values'] != '\n')]
    with_ok = df[df['Accepted'].str.contains('ok')]
    with_recall_without_ok = df[(df['Recall Values'].notna()) & (df['Recall Values'] != '\n') & ~df['Accepted'].str.contains('ok')]

    print(with_recall_without_ok)
    print(len(with_recall), len(with_ok))
    with_recall['Recall Values'].to_csv('file.csv')


    with_recall['Recall Values'] = with_recall['Recall Values'].str.replace(' {2,}', ' ', regex=True)
    with_recall['Recall Values'] = with_recall['Recall Values'].str.split(' ').apply(lambda x: x if isinstance(x, list) else [x])
    with_recall['Recall Values'] = with_recall['Recall Values'].apply(lambda lst: [x for x in lst if x != ''])
    with_recall['Recall Values'] = with_recall['Recall Values'].apply(lambda lst: [re.sub(',', '.', x) for x in lst])
    with_recall['Recall Values'] = with_recall['Recall Values'].apply(lambda lst: [float(y) for y in lst])

    concatenated_list = with_recall['Recall Values'].explode().to_list()
    concatenated_list_100 = [round(x / 100, 2) for x in concatenated_list]


    print(len(concatenated_list_100), np.mean(concatenated_list_100), np.std(concatenated_list_100))
    filtered_concatenated_list = eliminate_outliers(concatenated_list_100, 3)
    print(len(filtered_concatenated_list), np.mean(filtered_concatenated_list), np.std(filtered_concatenated_list),
          min(filtered_concatenated_list), max(filtered_concatenated_list))

    sns.displot(filtered_concatenated_list, kde='True')
    plt.show()

    par_sens = {'data_min_sens': min(filtered_concatenated_list), 'data_max_sens': max(filtered_concatenated_list),
                'data_loc_sens': np.mean(filtered_concatenated_list)}

    with open('binary_files/p_boxes/p_boxes_parameters_sens_1.pk', 'wb') as f:
        pk.dump(par_sens, f)