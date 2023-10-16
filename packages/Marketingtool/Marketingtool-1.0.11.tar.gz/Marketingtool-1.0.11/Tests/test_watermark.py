#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from Marketingtool.modules.watermark import Watermark
import os
import time

class WatermarkTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_remove_watermark(self):
        videopath=os.path.abspath('./Tests/data/test_watermark.flv')
        outputpath=os.path.abspath('./Tests/data/tmp/result_'+str(int(time.time()))+'.mp4')
        if os.path.exists(videopath) is not True:
            return
        
        #get timestamp
        # print(outputpath)
        videoModel=Watermark()
        videoModel.remove_watermark(videopath,outputpath,50)
        
