#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AnnotationBase 
@Time        :   2023/8/17 16:21
@Author      :   Xuesong Chen
@Description :   
"""
from abc import ABC, abstractmethod

import pandas as pd


class Base(ABC):
    def __init__(self, file_path):
        self.sleep_stages = None
        self.respiratory_events = None
        self._parse_file(file_path)

    @abstractmethod
    def _parse_file(self, file_path):
        self.recording_start_time = None
        self.duration = None
        self.anno_df = None

    def get_recording_start_time(self):
        return self.recording_start_time

    def get_duration(self):
        return self.duration

    def get_sleep_onset_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        onset_time = self.sleep_stages[self.sleep_stages['Type'] != 'Wake']['Start'].values[0]
        return onset_time

    def total_sleep_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        total_sleep_time = self.sleep_stages[self.sleep_stages['Type'] != 'Wake']['Duration'].sum()
        return total_sleep_time

    def get_standard_sleep_stages(self):
        '''
        用于获取标准的睡眠分期标记

        | Type | Start | Duration |
        |------|-------|----------|

        Type: Wake, N1, N2, N3, REM
        Start: 从睡眠开始到当前分期的时间
        Duration: 当前分期的持续时间，统一为30s

        :return:
        上述Dataframe格式
        '''
        return None

    def get_standard_respiratory_events(self):
        pass

    def plot_sleep_stage(self, ax=None):
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter

        # 设置开始时间
        start_time = self.recording_start_time
        sleep_stage = self.get_standard_sleep_stages() if self.sleep_stages is None else self.sleep_stages

        # 按照指定的顺序更新类型映射
        type_order = ['N3', 'N2', 'N1', 'REM', 'Wake', 'NotScored']
        type_mapping = {type: i for i, type in enumerate(type_order)}
        # 创建颜色映射，根据每个类型的实际含义选择颜色
        color_mapping = {
            "N3": "darkblue",
            "N2": "purple",
            "N1": "blue",
            "REM": "green",
            "Wake": "lightblue",
            "NotScored": "grey"
        }

        sleep_stage['Start'] = pd.to_timedelta(sleep_stage['Start'], unit='s') + start_time
        sleep_stage['End'] = sleep_stage['Start'] + pd.to_timedelta(sleep_stage['Duration'], unit='s')

        # 创建图表
        if not ax:
            fig, ax = plt.subplots(figsize=(100, 5))

        prev_end = None
        prev_type = None
        for _, row in sleep_stage.iterrows():
            ax.barh(type_mapping[row['Type']], row['End'] - row['Start'], left=row['Start'], height=0.5, align='center',
                    color=color_mapping[row['Type']])
            if prev_end is not None and prev_type is not None:
                ax.plot([prev_end, row['Start']], [type_mapping[prev_type], type_mapping[row['Type']]],
                        color='lightgrey')
            prev_end = row['End']
            prev_type = row['Type']

        # 设置y轴的标签
        ax.set_yticks(range(len(type_mapping)))
        ax.set_yticklabels(list(type_mapping.keys()))

        # 设置x轴的刻度标签为实际的小时和分钟
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        # set x limits
        start_time = sleep_stage['Start'].values[0]
        end_time = sleep_stage['End'].values[-1]
        ax.set_xlim([start_time, end_time])


