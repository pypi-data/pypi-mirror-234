# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/12/20
# @File  : [wanghong] taobao_rates_.py


import pandas as pd

from utils import DATA_DIR


def main():
    print(__name__)

    df_users = pd.read_csv(f'{DATA_DIR}/uids.csv', usecols=['Taobao_SID', 'Yizhibo_UID'])
    df_first = pd.read_csv(f'{DATA_DIR}/yizhibo_first.csv', parse_dates=['first_stream_date'])
    df_items = pd.read_csv(f'{DATA_DIR}/taobao_items.csv', usecols=['Taobao_SID', 'Taobao_IID'])
    df_rates = pd.read_csv(f'{DATA_DIR}/taobao_rates.csv', parse_dates=['date'])

    df_rates_ = df_users \
        .merge(df_items, on='Taobao_SID', how='inner') \
        .merge(df_first, on='Yizhibo_UID', how='inner') \
        .merge(df_rates, on='Taobao_IID', how='inner') \
        .drop(columns=['Yizhibo_UID'])
    df_rates_['after'] = df_rates_['date'] > df_rates_['first_stream_date']
    df_rates_['after'] = df_rates_['after'].astype(int)
    del df_rates_['first_stream_date']
    df_rates_.to_csv(f'{DATA_DIR}/taobao_rates_.csv', index=False)


if __name__ == '__main__':
    main()
