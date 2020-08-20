import numpy as np
import cv2

import json
import subprocess
import math
from moviepy.editor import *
from moviepy.video import VideoClip



audio = AudioFileClip('F:/srtp/$RTP/Music-to-Dance-Motion-Synthesis/DANCE_W_1/audio.mp3')
print('Analyzed the audio, found a period of %.02f seconds' % audio.duration)
video2 = VideoFileClip('./DANCE_W_1.mp4', audio=False)
video2 = video2.set_audio(audio)
video2.write_videofile('./DANCE_W_1_music.mp4')