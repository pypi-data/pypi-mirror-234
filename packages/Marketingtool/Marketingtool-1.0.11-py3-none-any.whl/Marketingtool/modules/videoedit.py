from moviepy.editor import VideoFileClip, concatenate_videoclips,TextClip,CompositeVideoClip
import os.path
import io
import subprocess

class Videoedit():
    def __init__(self)-> None:
        pass 
    
    def insertVideo(self, origin, inVideo, outputpath):
        """
        insert an video into another video
        """
        if os.path.exists(origin) is not True:
            raise FileNotFoundError("origin video File not found")
        if os.path.exists(inVideo) is True:
            raise FileNotFoundError("insert video File not found")
        splist=self.splitVideo(origin,2)
        clip1=splist[0].resize((1280, 720))
        clip2=splist[1].resize((1280, 720))
        clip3=VideoFileClip(inVideo).resize((1280, 720))
        final_clip = concatenate_videoclips([clip1,clip3,clip2])
        final_clip.write_videofile(outputpath)
        pass
    def splitVideo(self,videopath:str,parts:int)->list:
        
        clip = VideoFileClip(videopath)
        duration = clip.duration
        clip_list = []
        for i in range(parts):
            clip_list.append(clip.subclip(i*duration/parts,(i+1)*duration/parts))
        return clip_list
    def InsertText(self,videopath:str, outputpath:str,text:str,step:int,insertNum:int,frontsize:int,frontcolor:str,durations:int)->str:
        """
        Insert text into video
        """
        outputfilename=os.path.basename(outputpath)
        if outputfilename.lower=='fly':
            raise Exception("output path should not use fly") 
        
        clip = VideoFileClip(videopath) 
        t = 0
        # duration = duration
        textlist=[]
        for x in range(0,insertNum):
            textlist.append(text)
        txt_clips=[]
        for intext,i in zip(textlist,range(0,insertNum)):
            txt_clip = TextClip(intext, fontsize = frontsize, color = frontcolor)
            txt_clip = txt_clip.set_start(t)
            txt_clip = txt_clip.set_pos('top').set_duration(durations) 
            txt_clips.append(txt_clip)
            t=t+step
        finalVideo=[clip]
        for item in txt_clips:
            finalVideo.append(item)
        video = CompositeVideoClip(finalVideo) 
        video.write_videofile(outputpath)   
        return outputpath
    def InsertTextfromfile(self,videopath:str, outputpath:str,textpath:str,step:int=15,insertNum:int=10,fronsize:int=15,frontcolor:str="red",durations:int=10)->str:
        """insert text into video from file
        
        Args:
            videopath (str): insert video path
            outputpath (str): output video path
            textpath (str): text file path
            step (int): the interval between each text
            insertNum (int): how many text want to duplicate insert
            fronsize (int): front size
            frontcolor (str): _description_
            durations (int): _description_

        Raises:
            Exception: _description_

        Returns:
            str: _description_
        """
        text=None
        with io.open(textpath,'r',encoding='utf8') as f:
            text = f.read()
        if text is None:
            raise Exception("text file is empty")
        return self.InsertText(videopath, outputpath, text, step, insertNum, fronsize, frontcolor, durations)  
    def convertvideo(self,videopath:str,outputpath:str)->str:
        """
        convert video
        """
        convertCommand="ffmpeg -loglevel error -y -i "+videopath+" -qscale 0 "+outputpath
        try:
            subp = subprocess.check_output(convertCommand,shell=True,encoding="utf-8")
            return subp
        except subprocess.CalledProcessError:
            
            raise Exception("run convert video command error for:"+convertCommand)        
          
