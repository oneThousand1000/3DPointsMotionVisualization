import os
import time

import cv2
from numpy import *
import numpy as np
import smartbody_skeleton
import json


def getStandardFrames(frames):
    new_frames = np.zeros([len(frames), 21, 3])
    for i in range(len(frames)):
        # Hips
        new_frames[i][0][0] = frames[i][2][0] * -1
        new_frames[i][0][1] = frames[i][2][1]
        new_frames[i][0][2] = frames[i][2][2]


        # RightUpLeg
        new_frames[i][1][0] = frames[i][16][0] * -1
        new_frames[i][1][1] = frames[i][16][1]
        new_frames[i][1][2] = frames[i][16][2]

        # RightLeg
        new_frames[i][2][0] = frames[i][17][0] * -1
        new_frames[i][2][1] = frames[i][17][1]
        new_frames[i][2][2] = frames[i][17][2]
        # RightFoot
        new_frames[i][3][0] = frames[i][18][0] * -1
        new_frames[i][3][1] = frames[i][18][1]
        new_frames[i][3][2] = frames[i][18][2]

        # LeftHip
        new_frames[i][4][0] = frames[i][7][0] * -1
        new_frames[i][4][1] = frames[i][7][1]
        new_frames[i][4][2] = frames[i][7][2]
        # LeftKnee
        new_frames[i][5][0] = frames[i][8][0] * -1
        new_frames[i][5][1] = frames[i][8][1]
        new_frames[i][5][2] = frames[i][8][2]
        # LeftAnkle
        new_frames[i][6][0] = frames[i][9][0] * -1
        new_frames[i][6][1] = frames[i][9][1]
        new_frames[i][6][2] = frames[i][9][2]

        temp1 = [(frames[i][12][0] + frames[i][3][0]) / 2, (frames[i][12][1] + frames[i][3][1]) / 2,
                 (frames[i][12][2] + frames[i][3][2]) / 2]
        temp2 = [(frames[i][1][0] + frames[i][0][0]) / 2, (frames[i][1][1] + frames[i][0][1]) / 2,
                 (frames[i][1][2] + frames[i][0][2]) / 2]

        # Spine
        new_frames[i][7][0] = (temp1[0] + frames[i][2][0]) / 2 * -1
        new_frames[i][7][1] = (temp1[1] + frames[i][2][1]) / 2
        new_frames[i][7][2] = (temp1[2] + frames[i][2][2]) / 2
        # Thorax
        new_frames[i][8][0] = temp1[0] * -1
        new_frames[i][8][1] = temp1[1]
        new_frames[i][8][2] = temp1[2]

        # Neck
        new_frames[i][9][0] = (temp1[0] + (temp2[0] - temp1[0]) * 0.5) * -1
        new_frames[i][9][1] = (temp1[1] + (temp2[1] - temp1[1]) * 0.5)
        new_frames[i][9][2] = (temp1[2] + (temp2[2] - temp1[2]) * 0.5)
        # Head
        new_frames[i][10][0] = (temp1[0] + (temp2[0] - temp1[0]) * 1.3) * -1
        new_frames[i][10][1] = (temp1[1] + (temp2[1] - temp1[1]) * 1.3)
        new_frames[i][10][2] = (temp1[2] - (temp2[2] - temp1[2]) * 0.5)

        # LeftShoulder
        new_frames[i][11][0] = frames[i][3][0] * -1
        new_frames[i][11][1] = frames[i][3][1]
        new_frames[i][11][2] = frames[i][3][2]

        # LeftElbow
        new_frames[i][12][0] = frames[i][4][0] * -1
        new_frames[i][12][1] = frames[i][4][1]
        new_frames[i][12][2] = frames[i][4][2]
        # LeftWrist
        new_frames[i][13][0] = frames[i][5][0] * -1
        new_frames[i][13][1] = frames[i][5][1]
        new_frames[i][13][2] = frames[i][5][2]

        # RightShoulder
        new_frames[i][14][0] = frames[i][12][0] * -1
        new_frames[i][14][1] = frames[i][12][1]
        new_frames[i][14][2] = frames[i][12][2]
        # RightElbow
        new_frames[i][15][0] = frames[i][13][0] * -1
        new_frames[i][15][1] = frames[i][13][1]
        new_frames[i][15][2] = frames[i][13][2]

        # RightWrist
        new_frames[i][16][0] = frames[i][14][0] * -1
        new_frames[i][16][1] = frames[i][14][1]
        new_frames[i][16][2] = frames[i][14][2]

        # LeftWristEndSite
        new_frames[i][17][0] = frames[i][6][0] * -1
        new_frames[i][17][1] = frames[i][6][1]
        new_frames[i][17][2] = frames[i][6][2]

        # RightWristEndSite
        new_frames[i][18][0] = frames[i][15][0] * -1
        new_frames[i][18][1] = frames[i][15][1]
        new_frames[i][18][2] = frames[i][15][2]

        # LeftToe
        new_frames[i][19][0] = (frames[i][11][0] + frames[i][10][0]) / 2 * -1
        new_frames[i][19][1] = (frames[i][11][1] + frames[i][10][1]) / 2
        new_frames[i][19][2] = (frames[i][11][2] + frames[i][10][2]) / 2

        # RightToe
        new_frames[i][20][0] = (frames[i][20][0] + frames[i][19][0]) / 2 * -1
        new_frames[i][20][1] = (frames[i][20][1] + frames[i][19][1]) / 2
        new_frames[i][20][2] = (frames[i][20][2] + frames[i][19][2]) / 2


        foot_z=min(new_frames[i][19][2],new_frames[i][20][2])
        for j in range(21):
            new_frames[i][j][2]-=foot_z

    return new_frames


if __name__ == '__main__':
    # dance_type='T'
    # music_name='Assassins Tango'
    # input_json_path='F:/srtp/$RTP/git_files/SRTP/result/%s/%s.json'%(dance_type,music_name)
    # output_bvh_path='%s.bvh'%music_name


    with open('./skeletons.json','r') as fin:
        data = json.load(fin)

    frames=np.array(data['skeletons'])
    frames=getStandardFrames(frames)
    smartbody_skeleton = smartbody_skeleton.SmartBodySkeleton()
    smartbody_skeleton.poses2bvh(frames, output_file='./test.bvh')