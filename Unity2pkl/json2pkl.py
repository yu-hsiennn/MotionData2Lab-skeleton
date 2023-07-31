import json, os, pickle
import numpy as np

skeleton_list = ['head', 'neck', 'R_shoulder', 'R_Elbow', 'R_hand',
                'L_shoulder', 'L_Elbow', 'L_hand', 'hip', 'R_hip',
                'R_knee', 'R_foot', 'L_hip', 'L_knee', 'L_foot',
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
                'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3']

joints_chain = [
    [3, 24], [0,3],  
    [6, 3], [9, 6], [12, 9],
    [27, 24], [30, 27], [33, 30],
    [15, 3], [18, 15], [21, 18], 
    [36, 24], [39, 36], [42, 39],
    [45, 42], [48, 33],
    [51, 21], [54, 51], [57, 54],
    [60, 21], [63, 60], [66, 63],
    [69, 21], [72, 69], [75, 72],
    [78, 21], [81, 78], [84, 81],
    [87, 21], [90, 87], [93, 90],
    [96, 12], [99, 96], [102, 99],
    [105, 12], [108, 105], [111, 108],
    [114, 12], [117, 114], [120, 117],
    [123, 12], [126, 123], [129, 126],
    [132, 12], [135, 132], [138, 135]
]

# set folder path
json_folder = "json_files"
save_folder = "pkl_files"

def read_json(file):
    motion_list  = []
    with open(file, 'rb') as jf:
        for line in jf.readlines():
            data = json.loads(line)
            txt_line = []
            for skeleton in skeleton_list:
                txt_line += [float(data[f"{skeleton}.x"])]
                txt_line += [float(data[f"{skeleton}.y"])]
                txt_line += [float(data[f"{skeleton}.z"])]
            motion_list.append(txt_line)

    return np.array(motion_list)

def calc_angle(data):
    AngleList = np.zeros_like(data)
    for i, frame in enumerate(data):
        for joint in joints_chain:
            v = frame[joint[0]:joint[0]+3] - frame[joint[1]:joint[1]+3]
            AngleList[i][joint[0]:joint[0]+3] = list(get_angle(v))
    return AngleList

def get_angle(v):
    axis_x = np.array([1,0,0])
    axis_y = np.array([0,1,0])
    axis_z = np.array([0,0,1])

    thetax = axis_x.dot(v)/(np.linalg.norm(axis_x) * np.linalg.norm(v))
    thetay = axis_y.dot(v)/(np.linalg.norm(axis_y) * np.linalg.norm(v))
    thetaz = axis_z.dot(v)/(np.linalg.norm(axis_z) * np.linalg.norm(v))

    return thetax, thetay, thetaz

def argument(data):
    argu_data = []
    argu_data.extend(data)
    while len(argu_data) < 100:
        slow = 3 # 內插frame
        for i in range(slow):
            argu_data.append(data[-1] + i*(data[0]-data[-1]) / (slow+1))
        argu_data.extend(data)
    return np.array(argu_data)

def normalize(data):
    data = data.reshape(data.shape[0], int(data.shape[1]/3), 3)
    normal_data = []
    for i, frame in enumerate(data):
        root = (frame[9]+frame[12]) / 2
        data[i, 8] = root
        normal_data.append([])
        for node in frame:
            normal_data[-1].extend(node - root)

    return np.array(normal_data)

def processing():
    all_files = os.listdir(json_folder)
    for file in all_files:
        motion_list = read_json(os.path.join(json_folder, file))
        norm_data = normalize(motion_list)
        angle_data = calc_angle(norm_data)

        # write coordinate information into pkl files
        with open(os.path.join(save_folder, f'coordinates/{file[:-4]}pkl'), 'wb') as f:
            pickle.dump(norm_data, f)

        # write angle information into pkl files
        with open(os.path.join(save_folder, f'angle/{file[:-4]}pkl'), 'wb') as f:
            pickle.dump(angle_data, f)



if __name__ == '__main__':
    processing()

