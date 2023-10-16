#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Philips 
@Time        :   2023/9/14 15:41
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.Reader.EDF.Base import Base


class PhilipsEDFReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)
