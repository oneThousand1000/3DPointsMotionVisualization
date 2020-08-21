import numpy as np
import cv2

import json
import subprocess
import math
from moviepy.editor import *
from moviepy.video import VideoClip



audio = AudioFileClip('F:/srtp/$RTP/git_files/SRTP/music/T/Assassins Tango.mp3')
print('Analyzed the audio, found a period of %.02f seconds' % audio.duration)
video2 = VideoFileClip('./Assassins Tango.mp4', audio=False)
video2 = video2.set_audio(audio)
video2.write_videofile('./Assassins Tango_output.mp4')