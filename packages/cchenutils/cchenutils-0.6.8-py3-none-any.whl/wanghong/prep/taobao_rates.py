#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/1/20
# @File  : [wanghong] taobao_rates.py


import json
from datetime import datetime, timedelta
import random
import pandas as pd

from utils import DATA_DIR


def parse_default_rating(content):
    if content == '评价方未及时做出评价,系统默认好评!':
        return 1
    else:
        return 0


def parse_valid_comment(content):
    if content in {'此用户没有填写评价。', '评价方未及时做出评价,系统默认好评!', '系统默认评论'}:
        return 0
    else:
        return 1


def adj_date(date, is_default):
    if not is_default:
        return date
    this_date = datetime.strptime(date, u'%Y-%m-%d')
    this_date += timedelta(days=-15)
    return this_date.strftime('%Y-%m-%d')


def adj_date_by(date, adj):
    this_date = datetime.strptime(date, u'%Y-%m-%d')
    this_date += timedelta(days=adj)
    return this_date.strftime('%Y-%m-%d')


def main():
    print(__name__)

    df_rates = pd.read_csv(f'{DATA_DIR}/_taobao_rates.csv', #nrows=100000,
                           dtype={'_id': str, 'itemid': str, 'reply': str})
    df_rates = df_rates.dropna(subset=['date']) \
        .rename(columns={'_id': 'Taobao_RID', 'itemid': 'Taobao_IID', 'date': 'rate_date', 'buyAmount': 'purchases'}) \
        .drop_duplicates(subset=['Taobao_RID', 'Taobao_IID', 'rate_date', 'content', 'user.nick',
                                 'purchases', 'bidPriceMoney.amount', 'promotionType', 'rate']) \
        .drop(columns=['user.nick'])

    df_rates['Taobao_RID'] = 'TR' + df_rates['Taobao_RID']
    df_rates['Taobao_IID'] = 'TI' + df_rates['Taobao_IID']
    df_rates['default'] = df_rates['content'].apply(parse_default_rating)
    df_rates['valid'] = df_rates['content'].apply(parse_valid_comment)
    df_rates['purchases'] = df_rates['purchases'].apply(lambda x: 1 if x == 0 or not x else x)
    df_rates['rate_date'] = df_rates['rate_date'].apply(
        lambda x: datetime.strptime(x, '%Y年%m月%d日 %H:%M').strftime('%Y-%m-%d'))
    df_rates['date'] = df_rates.apply(lambda x: adj_date_by(x['rate_date'], -15 if x['default'] else 0), axis=1)
    df_rates['date1'] = df_rates['date'].apply(lambda x: adj_date_by(x, -1))
    df_rates['date2'] = df_rates['date'].apply(lambda x: adj_date_by(x, -2))
    random.seed(1)
    df_rates['date12'] = df_rates['date'].apply(lambda x: adj_date_by(x, -1 if random.random() > 0.5 else -2))
    df_rates['promo'] = df_rates.pop('promotionType').fillna('').apply(lambda x: '活动促销' in x).astype(int)
    df_rates['content'] = df_rates.apply(lambda x: x['content'] if x['valid'] else '', axis=1)
    df_rates['photos'] = df_rates['photos'].apply(lambda x: len(eval(x)))
    df_rates['video'] = df_rates['video'].notnull().astype(int)
    df_rates['seller_replied'] = df_rates.pop('reply').notnull().astype(int)
    df_rates['vicious'] = df_rates['vicious'].fillna(0)

    # 追加评论
    append_rates = []
    for idx, row in df_rates[df_rates['appendList'].apply(lambda x: x != '[]')].iterrows():
        for rate in json.loads(row['appendList']):
            if rate['appendId'] == 0:
                continue
            Taobao_RID = 'TR' + rate['appendId']['$numberLong']
            Taobao_IID = row['Taobao_IID']
            rate_date = (datetime.strptime(row['rate_date'], '%Y-%m-%d') + timedelta(days=rate['dayAfterConfirm'])) \
                .strftime('%Y-%m-%d')
            photos = len(rate['photos'])
            video = len(rate['videos'])
            vicious = rate['vicious']
            content = rate['content']
            seller_replied = int(rate['reply'] is not None)
            append_rates.append([Taobao_RID, Taobao_IID, rate_date, photos, video, vicious, seller_replied, content])
    df_append = pd.DataFrame(append_rates,
                             columns=['Taobao_RID', 'Taobao_IID',
                                      'rate_date', 'photos', 'video',
                                      'vicious', 'seller_replied', 'content'])

    # export
    df_rates.drop(columns=['appendList']).to_csv(f'{DATA_DIR}/taobao_rates.csv', index=False)
    df_append.to_csv(f'{DATA_DIR}/taobao_appendrates.csv', index=False)


if __name__ == '__main__':
    main()
