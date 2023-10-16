# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile
import re
import logging
from Marketingtool.modules.get_watermark import get_watermark
import shutil

logger = logging.getLogger(__name__)
class RunCommandError(Exception):
    pass
class Watermark():
    def __init__(self):
        pass
    def remove_watermark(self,video_path:str,output_path:str,max_frames:int=50):
        """
        remove watermark from video
        """
        if os.path.exists(video_path) is not True:
            raise FileNotFoundError("File not found")        
        tmpdir =self.getframe(video_path,max_frames)
        getWaterMark=get_watermark()
        image_path=getWaterMark.get_watermarks(tmpdir)
        # logger.info(image_path)
        if image_path is None:
            raise Exception("watermark not generate success")
        # start to remove watermark
        removecmd="ffmpeg -hide_banner -loglevel error -y -stats -i "+video_path+" -acodec copy -vf \"removelogo="+image_path+"\" "+output_path+""
        self.cmd(removecmd)
        shutil.rmtree(tmpdir)
    def getframe(self,video_path:str,max_frames:int=50)->str:    
        """
        get frame from video
        """
        getframe="ffprobe -hide_banner -loglevel warning -select_streams v -skip_frame nokey -show_frames -show_entries frame=pkt_dts_time "+video_path+" | grep \"pkt_dts_time=\" | xargs shuf -n "+str(max_frames)+" -e | awk -F  \"=\" '{print $2}'"
        keyframes_time=self.cmd(getframe).splitlines()

        tmpdir = tempfile.mkdtemp()
        logger.info("Extracting frames (up to: "+str(max_frames)+")... to the tmp path:"+tmpdir)
        logger.info(keyframes_time)
        counter=0
        for i in keyframes_time: 
            if not re.match("^[0-9]+([.][0-9]+)?$", i): 
                logger.info("Skipping unrecognize timing: " + i)
                continue
            
            generateframe="ffmpeg -y -hide_banner -loglevel error -ss "+i+" -i "+video_path+" -vframes 1 "+tmpdir+"/output_"+str(counter)+".png"
            logger.info("run get frame pic command: "+generateframe)
            self.cmd(generateframe)
        # print("$counter ")
            counter=counter+1
        if counter < 2:
            raise Exception("frames extracted, need at least 2, aborting. The command "+getframe+" failed.")
        return tmpdir
    def cmd(self,command):
        """
        run shell command
        """
        try:
            subp = subprocess.check_output(command,shell=True,encoding="utf-8")
            return subp
        except subprocess.CalledProcessError:
            
            raise RunCommandError("run command error for:"+command)
        