#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NSRR 
@Time        :   2023/8/17 16:47
@Author      :   Xuesong Chen
@Description :   
"""
import xmltodict
import pandas as pd

from Reader.Annotation.Base import Base
from utils.psg import get_equal_duration_and_labeled_chunks
from datetime import datetime


class NSRRAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            info_dict = xmltodict.parse(f.read())
            self.scored_events = pd.DataFrame(info_dict['PSGAnnotation']['ScoredEvents']['ScoredEvent'])
            date_string = self.scored_events.loc[0, 'ClockTime']
            fake_datetime = datetime.strptime('2000-01-01 ' + date_string.split(' ')[-1], '%Y-%m-%d %H.%M.%S')
            self.recording_start_time = fake_datetime
            self.duration = float(self.scored_events.loc[0, 'Duration'])
            self.scored_events[['Start', 'Duration']] = self.scored_events[['Start', 'Duration']].astype(float)
            self.scored_events = self.scored_events.iloc[1:]

    def get_standard_sleep_stages(self):
        stages = self.scored_events[self.scored_events['EventType'] == 'Stages|Stages'].copy()
        stages.loc[:, 'stage_num'] = stages['EventConcept'].str.split('|', expand=True)[1].astype(int)
        map_dic = {0: 'Wake', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'N3', 5: 'REM'}
        stages.loc[:, 'Type'] = stages['stage_num'].map(map_dic)
        stages = stages[['Type', 'Start', 'Duration']]
        standard_stages = get_equal_duration_and_labeled_chunks(stages)
        self.sleep_stages = standard_stages
        return standard_stages

    def get_standard_respiratory_events(self):
        pass

    def gen_respiratory_events(self):
        pass


if __name__ == '__main__':
    fp = '/Users/cxs/project/OSAPillow/data/SHHS/annotations/shhs1-200001-nsrr.xml'
    reader = NSRRAnnotationReader(fp)
    stages = reader.get_standard_sleep_stages()
    print()
