# MotionData2Lab-skeleton

## About
This project provides basic motion data conversion, primarily intended for later use in our laboratory's [Unity visualization tool](https://github.com/NCKU-SCREAM-Lab/Lab-Skeleton2Unity) and for training dataset formatting.

## Prerequisites
This project is developed using **Python 3.8**, so please ensure that [Python](https://www.python.org/) is installed on your computer.

## Installation
- Cloning this repo on your local machine:
    ```shell
    $ git clone git@github.com:yu-hsiennn/MotionData2Lab-skeleton.git
    ```
    Or download [zip](https://github.com/yu-hsiennn/MotionData2Lab-skeleton/archive/refs/heads/master.zip) file.
    
- change current directory
    ```shell
    $ cd MotionData2Lab-skeleton
    ```


## How to use?

### FBX2pkl
It is used to convert human motion data in FBX format into pickle files.
Before using, please make sure that [Blender](https://www.blender.org/) is installed on your machine.

**step 1.** change current directory.
```shell
$ cd FBX2pkl
```

**step 2.** create a folder then put your fbx datas in it.
```shell
$ mkdir fbx_folder
```

**step 3.** make sure the human joint definitions in the FBX files are the same.
- you can use any application to find level of human joints.([Unity](https://unity.com/), [Blender](https://www.blender.org/), [Unreal Engine](https://www.unrealengine.com/), etc.)

**step 4.** modify **fbx2pkl.py** code.
```python=8
SRC_DATA_DIR = 'YOUR FBX FOLDER'
OUT_DATA_DIR = 'YOUR SAVE FOLDER'

MIN_NR_FRAMES = 64
RESOLUTION = (512, 512)

# according your human joints definition to modify joint name
BASE_JOINT_NAMES = ['Head', 'Neck',
    'RightArm', 'RightForeArm', 'RightHand', 'LeftArm', 'LeftForeArm', 'LeftHand',
    'Hips', 'RightUpLeg', 'RightLeg', 'RightFoot', 'LeftUpLeg', 'LeftLeg', 'LeftFoot',
    'LeftToeBase', 'RightToeBase',
    'LeftHandThumb1', 'LeftHandThumb2', 'LeftHandThumb3', 
    'LeftHandIndex1', 'LeftHandIndex2', 'LeftHandIndex3', 
    'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3', 
    'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 
    'LeftHandPinky1', 'LeftHandPinky2', 'LeftHandPinky3', 
    'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 
    'RightHandIndex1', 'RightHandIndex2', 'RightHandIndex3', 
    'RightHandMiddle1', 'RightHandMiddle2', 'RightHandMiddle3', 
    'RightHandRing1', 'RightHandRing2', 'RightHandRing3', 
    'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3'
    ]
```

**step 5.** running command
```shell
$ blender --background -P fbx2pkl.py
```
----
### pkl2txt
It is used to convert data defined in pickle files into the txt file format required for subsequent use in [Unity visualization tools](https://github.com/NCKU-SCREAM-Lab/Lab-Skeleton2Unity).

**step 1.** change current directory.
```shell
$ cd pkl2txt
```

**step 2.** put your pickle datas in **pkl_file** folder.

**step 3.** running command
```shell
$ python pkl2txt.py
```
---
### Unity2pkl
Used to convert joint coordinates captured from Unity into the data format required for the subsequent model.

**step 1.** change current directory.
```shell
$ cd Unity2pkl
```

**step 2.** put your json datas in **json_files** folder.

**step 3.** running command
```shell
$ python json2pkl.py
```
---
### train_data
Normalize the previously [converted data](#FBX2pkl) or external data, and then divide it into training and testing datasets.
**step 1.** change current directory.
```shell
$ cd train_data
```

**step 2.** modify **data_prepare.py** code.
```python=6
    def __init__(self):

        # Initial joints
        self.Lab_joints = Lab_skeleton()
        self.joint = self.Lab_joints.get_joint()
        self.jointConnect = self.Lab_joints.get_joints_connect()

        # -----TODO-----
        # Initial data path
        self.data_pkl_path = "pickle files folder path" # "../FBX2pkl/Choreomaster_pkl_with_finger"
        self.test_path = "test folder path" #ex. "ChoreoMaster_train/test"
        self.train_path = "train folder path" #ex. "ChoreoMaster_train/train"
        self.angle_train_path = "train angle folder path" #ex. "ChoreoMaster_train/train_angle"
        self.angle_test_path = "test angle folder path" # "ex. ChoreoMaster_train/test_angle"
        self.dataset_folder = "dataset folder name" # "ex. ChoreoMaster_train"
```


**step 3.** running command
```shell
$ python data_prepare.py
```

## License
This project is licensed under the MIT. See the LICENSE.md file for details
