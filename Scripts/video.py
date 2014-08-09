#!/usr/bin/env python
import os
import re
import cv2
import numpy as np

class Video:
    def __init__(self, filepath):
        self.filepath = filepath
        self.extension = os.path.splitext(filepath)[1]
        self.videoname = re.sub(self.extension, '', filepath)
        tempcap = cv2.VideoCapture(filepath)
        self.width = int(tempcap.get(3))
        self.height = int(tempcap.get(4))
        self.fps = np.rint(tempcap.get(5))
        self.numframes = np.rint(tempcap.get(7))
        self.startt = 0.0
        self.endt = (self.numframes / self.fps)*1e3
        self.fourcc = int(tempcap.get(6))
        tempcap.release()
   
    def cut(self, ms_start, ms_end, outfile=None):
        """Cut the video from start time to end time (in milliseconds) and write to outpath
            Hack: use CV_FOURCC('D','I','V','X') and save as .avi file, then rename back to orignal extension"""
        
        cap = cv2.VideoCapture(self.filepath)
        if outfile==None:
            outfile = self.videoname + "_" + str(ms_start) + "_" + str(ms_end) + ".avi"
        print 'fourcc', self.fourcc
        print  'fps', self.fps
        print 'width', self.width
        print 'height', self.height
        fourcc = cv2.cv.CV_FOURCC('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(outfile, fourcc, self.fps, (self.width, self.height))
        while(cap.isOpened()):          
            ret, frame = cap.read()
            if (ret == True):
                if (cap.get(0) >= ms_start and cap.get(0) < ms_end):
                    out.write(frame)
                elif (cap.get(0) >= ms_end):
                  break
            else:
                break
        cap.release()
        out.release()
        return outfile