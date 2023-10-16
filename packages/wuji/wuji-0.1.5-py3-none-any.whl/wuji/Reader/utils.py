#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils 
@Time        :   2023/9/14 17:33
@Author      :   Xuesong Chen
@Description :   
"""

import pandas as pd


def get_equal_duration_and_labeled_chunks(event_df, chunk_duration=30):
    """将标注数据框转换为等长事件列表，如果最后一个事件的持续时长不足chunk_duration，则以真实值填充。

        Parameters
        ----------
        event_df : pandas.DataFrame
            具有标注名称(Type)、开始时长(Start)和持续时长(Duration)的数据框。

        Returns
        -------
        ret_df : pandas.DataFrame
            具有标注名称(Type)、开始时长(Start)和持续时长(Duration)的数据框。
        """
    assert 'Type' in event_df.columns and 'Start' in event_df.columns and 'Duration' in event_df.columns, "check columns"

    ret_df = pd.DataFrame(columns=['Type', 'Start', 'Duration'])
    for idx, row in event_df.iterrows():
        start = int(row['Start'])
        duration = row['Duration']
        while duration > 0:
            cur_duration = duration if duration < chunk_duration else chunk_duration
            ret_df = pd.concat([
                ret_df,
                pd.DataFrame({'Type': row['Type'], 'Start': start, 'Duration': cur_duration}, index=[0])])
            start += chunk_duration
            duration -= chunk_duration
    assert sum(ret_df['Duration'] % 30 != 0) <= 1, "sleep stage duration error"
    return ret_df.reset_index(drop=True)
