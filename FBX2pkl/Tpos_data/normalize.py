import pickle
import numpy as np

pkl_file = "pkl/T-pos-fullbody.pkl"
save_path = "T-pos-fullbody-normalize.pkl"

joint = {
    "Head":0, "Neck":1, 
    "RightShoulder":2, "RightArm":3, "RightHand":4, 
    "LeftShoulder":5, "LeftArm":6, "LeftHand":7, 
    "Pelvis":8, 
    "RightThigh":9, "RightKnee":10,"RightAnkle":11,
    "LeftThigh":12, "LeftKnee":13, "LeftAnkle":14,
    "LeftToeBase": 15, "RightToeBase": 16,
    "LeftHandThumb1": 17, "LeftHandThumb2": 18, "LeftHandThumb3": 19,
    "LeftHandIndex1": 20, "LeftHandIndex2": 21, "LeftHandIndex3": 22,
    "LeftHandMiddle1": 23, "LeftHandMiddle2": 24, "LeftHandMiddle3": 25,
    "LeftHandRing1": 26, "LeftHandRing2": 27, "LeftHandRing3": 28,
    "LeftHandPinky1": 29, "LeftHandPinky2": 30, "LeftHandPinky3": 31,
    "RightHandThumb1": 32, "RightHandThumb2": 33, "RightHandThumb3": 34,
    "RightHandIndex1": 35, "RightHandIndex2": 36, "RightHandIndex3": 37,
    "RightHandMiddle1": 38, "RightHandMiddle2": 39, "RightHandMiddle3": 40,
    "RightHandRing1": 41, "RightHandRing2": 42, "RightHandRing3": 43,
    "RightHandPinky1": 44, "RightHandPinky2": 45, "RightHandPinky3": 46
}

def data_reader():
    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)
    return data

def save_data(datas):
    with open(save_path, 'wb') as f:
        pickle.dump(datas, f)

def normalize(data):
    data = data.reshape(data.shape[0], int(data.shape[1]/3), 3)
    normal_data = []
    for i, frame in enumerate(data):
        root = (frame[joint['RightThigh']]+frame[joint['LeftThigh']]) / 2
        data[i, joint['Pelvis']] = root
        normal_data.append([])
        for node in frame:
            normal_data[-1].extend(node - root)

    return np.array(normal_data)

save_data(normalize(data_reader()))