#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Phillip 
@Time        :   2023/9/14 15:40
@Author      :   Xuesong Chen
@Description :   
"""

import os

from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from wuji.Reader.Annotation.Base import Base
import pandas as pd
import xmltodict
from datetime import datetime


class PhilipsAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        f = open(file_path, encoding='utf-8')
        self.info_dict = xmltodict.parse(f.read())
        start_time_str = self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session'][
            'RecordingStart']
        self.recording_start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
        self.duration = int(self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session']['Duration'])

    def get_standard_sleep_stages(self, **kwargs):
        stage_list = self.info_dict['PatientStudy']['ScoringData']['StagingData'][
            'UserStaging']['NeuroAdultAASMStaging']['Stage']
        stage_dic = {
            'Start': [int(i['@Start']) for i in stage_list],
            'Type': [i['@Type'] for i in stage_list],
        }
        stages = pd.DataFrame.from_dict(stage_dic)
        stages['Duration'] = stages['Start'].shift(-1) - stages['Start']
        stages.at[stages.index[-1], 'Duration'] = self.duration - stages['Start'].iloc[-1]
        map_dic = {
            'Wake': 'Wake', 'NonREM1': 'N1', 'NonREM2': 'N2',
            'NonREM3': 'N3', 'NonREM4': 'N3', 'REM': 'REM',
        }
        stages.loc[:, 'Type'] = stages['Type'].map(map_dic)
        standard_stages = get_equal_duration_and_labeled_chunks(stages, **kwargs)
        self.sleep_stages = standard_stages
        return standard_stages

    def get_standard_respiration_events(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
        }
        for e in resp_events_list:
            if e['@Type'] in ['PeriodicRespiration']:
                continue
            type_list.append(map_dic[e['@Type']])
            start_list.append(float(e['@Start']))
            duration_list.append(float(e['@Duration']))
        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        respiratory_events = pd.DataFrame.from_dict(respiratory_events_dic)
        self.respiratory_events = respiratory_events
        return respiratory_events


if __name__ == '__main__':
    fp = '/Volumes/Extreme SSD/parallel_data/00000720-LEBS21876_2621497/00000720-LEBS21876_2621497.rml'
    anno = PhilipsAnnotationReader(fp)
    res = anno.get_standard_sleep_stages()
    res = anno.get_standard_respiration_events()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    anno.plot_sleep_stage(ax=ax)
    plt.show()
