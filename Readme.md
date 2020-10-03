# Readme

这是一个将人体骨骼序列转化为bvh并进行可视化的工具

## 人体骨骼序列转化为bvh动作文件

`3Dpoints2BVH`文件夹

转化方法参考了：https://github.com/HW140701/VideoTo3dPoseAndBvh

请注意，如果需要直接使用我的代码，请将骨骼存储格式改为大小为[length,19,3]的三维数组，其中，length为骨骼序列长度

而每个动作包含19个骨骼点三维坐标，顺序如下：

```
'Hips': 0,
'RightUpLeg': 1,
'RightLeg': 2,
'RightFoot': 3,
'LeftUpLeg': 4,
'LeftLeg': 5,
'LeftFoot': 6,
'Spine': 7,
'Spine3': 8,
'Neck': 9,
'Head': 10,
'LeftArm': 11,
'LeftForeArm': 12,
'LeftHand': 13,
'RightArm': 14,
'RightForeArm': 15,
'RightHand': 16,
'LeftWristEndSite': 17,
'RightWristEndSite': 18,
'LeftToe': 19,
'RightToe': 20
```

修改`./3Dpoints2BVH/run.py`中的输入输出路径并运行，就能得到`.bvh`文件

## 简易的.bvh文件查看器：

`BvhViewer`文件夹，可以将`.bvh`文件进行简单的可视化，用于调试

下载来源：https://download.csdn.net/detail/dxth06/3508439

![2](./images/2.png)

你也可以使用https://github.com/mrzli/bvhviewer  中的bvh查看器

## 模型和动作示例：

`model`文件夹，存储pmx模型和`.bvh`文件示例

## 导入模型和动作的可视化工具：

`liveAnimation`文件夹，需要按照说明进行安装，然后才能运行`liveAnimation.exe`进行可视化，首先导入pmx模型，随后导入`.bvh`动作文件

![1](./images/1.png)
