#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import time
from Marketingtool.modules.videoedit import Videoedit
import os

class VideoeditTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_insert_text(self):
        videopath=os.path.abspath('./Tests/data/test.flv')
        outputpath=os.path.abspath('./Tests/data/tmp/result_'+str(int(time.time()))+'.mp4')
        if os.path.exists(videopath) is not True:
            return
        
        #get timestamp
        # print(outputpath)
        text='test text,you should see it!'
        videoModel=Videoedit()
        videoModel.InsertText(videopath,outputpath,text,15,3,15,'red',10)

if __name__ == '__main__':
    unittest.main(warnings='ignore')