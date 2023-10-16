#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NSRR 
@Time        :   2023/8/17 16:47
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.Reader.EDF.Base import Base
import neurokit2 as nk


class NSRREDFReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)


if __name__ == '__main__':
    fp = '/Users/cxs/project/OSAPillow/data/SHHS/edfs/shhs1-200001.edf'
    reader = NSRREDFReader(fp)
    print(reader.get_signal(type='ecg', tmax=10))
    # stages = Reader.get_standard_sleep_stages()

