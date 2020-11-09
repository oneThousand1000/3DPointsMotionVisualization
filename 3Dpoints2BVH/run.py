import os
import time

import cv2
from numpy import *
import numpy as np
import smartbody_skeleton
import json

import argparse

parser = argparse.ArgumentParser(description='3Dpoints2BVH')
parser.add_argument('-i', '--input_json', default='./Besame_Mucho.json', type=str,
                        help='input json  file')
parser.add_argument('-o', '--output_bvh', default='./test.bvh', type=str, help='output bvh file')

def smooth(a, WSZ):
    out0 = np.convolve(a, np.ones(WSZ, dtype=int), 'valid') / WSZ
    r = np.arange(1, WSZ - 1, 2)
    start = np.cumsum(a[:WSZ - 1])[::2] / r
    stop = (np.cumsum(a[:-WSZ:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))


def smooth_skeleton(motion):
    WSZ = 7
    skeletons_num = motion.shape[1]
    skeletons = np.hsplit(motion, skeletons_num)
    cur_skeleton = np.reshape(skeletons[0], (-1, 3))
    # print(cur_skeleton.shape)
    x_seq = np.split(cur_skeleton, 3, axis=1)[0]
    x_seq = np.reshape(x_seq, -1)

    y_seq = np.split(cur_skeleton, 3, axis=1)[1]
    y_seq = np.reshape(y_seq, -1)

    z_seq = np.split(cur_skeleton, 3, axis=1)[2]
    z_seq = np.reshape(z_seq, -1)

    x_smooth = smooth(x_seq, WSZ)
    y_smooth = smooth(y_seq, WSZ)
    z_smooth = smooth(z_seq, WSZ)
    x_smooth = np.array(x_smooth)
    smooth_result = np.column_stack((x_smooth, y_smooth, z_smooth))

    for i in range(1, motion.shape[1]):
        cur_skeleton = np.reshape(skeletons[i], (-1, 3))
        # print(cur_skeleton.shape)
        x_seq = np.split(cur_skeleton, 3, axis=1)[0]
        x_seq = np.reshape(x_seq, -1)

        y_seq = np.split(cur_skeleton, 3, axis=1)[1]
        y_seq = np.reshape(y_seq, -1)

        z_seq = np.split(cur_skeleton, 3, axis=1)[2]
        z_seq = np.reshape(z_seq, -1)

        x_smooth = smooth(x_seq, WSZ)
        y_smooth = smooth(y_seq, WSZ)
        z_smooth = smooth(z_seq, WSZ)
        x_smooth = np.array(x_smooth)
        # print(x_smooth.shape)
        x = np.linspace(1, 5050, 5050)  # X轴数据
        tmp = np.column_stack((x_smooth, y_smooth, z_smooth))
        if i == 1:
            smooth_result = np.stack((smooth_result, tmp), axis=1)
        else:
            tmp_ = tmp[:, np.newaxis, :]
            smooth_result = np.concatenate((smooth_result, tmp_), axis=1)

    return smooth_result

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
    args = parser.parse_args()


    with open(args.input_json,'r') as fin:
        data = json.load(fin)

    frames=np.array(data['skeletons'])
    frames = smooth_skeleton(getStandardFrames(frames))
    #frames=smooth_skeleton(frames)
    smartbody_skeleton = smartbody_skeleton.SmartBodySkeleton()
    smartbody_skeleton.poses2bvh(frames, output_file=args.output_bvh)