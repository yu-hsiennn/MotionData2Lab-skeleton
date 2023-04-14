import pickle, os, random
import numpy as np
from Lab_skeleton_def import Lab_skeleton

class prepare:
    def __init__(self):

        # Initial joints
        self.Lab_joints = Lab_skeleton()
        self.joint = self.Lab_joints.get_joint()
        self.jointConnect = self.Lab_joints.get_joints_connect()

        # Initial data path
        self.data_pkl_path = "../FBX2pkl/Choreomaster_pkl_with_finger"
        self.test_path = "ChoreoMaster_train/test"
        self.train_path = "ChoreoMaster_train/train"
        self.angle_train_path = "ChoreoMaster_train/train_angle"
        self.angle_test_path = "ChoreoMaster_train/test_angle"
        self.dataset_folder = "ChoreoMaster_train"

        self.path_check(self.dataset_folder)

        # get all of pkl files
        self.all_file = os.listdir(self.data_pkl_path)

    def path_check(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        
    def name_mapping(self):
        self.file_name_table = {}
        for idx, file in enumerate(self.all_file):
            new_name = f'choreo_all_{idx+1}_ca_01.pkl'
            self.file_name_table[file] = new_name

    def normalize(self, data):
        data = data.reshape(data.shape[0], int(data.shape[1]/3), 3)
        normal_data = []
        for i, frame in enumerate(data):
            root = (frame[self.joint['RightThigh']]+frame[self.joint['LeftThigh']]) / 2
            data[i, self.joint['Pelvis']] = root
            normal_data.append([])
            for node in frame:
                normal_data[-1].extend(node - root)

        return np.array(normal_data)

    def argument(self, data):
        argu_data = []
        argu_data.extend(data)
        while len(argu_data) < 100:
            slow = 3 # 內插frame
            for i in range(slow):
                argu_data.append(data[-1] + i*(data[0]-data[-1]) / (slow+1))
            argu_data.extend(data)
        return np.array(argu_data)

    def divide(self):
        self.path_check(self.train_path)
        self.path_check(self.test_path)

        test_file = random.sample(self.all_file, int(len(self.all_file)*0.2))

        for file in self.all_file:
            with open(os.path.join(self.data_pkl_path, file), "rb") as f_pkl:
                data = pickle.load(f_pkl)

            normal_data = self.normalize(data)
            if len(normal_data) < 100:
                print("argument!")
                normal_data = self.argument(normal_data)

            if file in test_file:
                with open(os.path.join(self.test_path, self.file_name_table[file]), "wb") as f:
                    pickle.dump(normal_data, f)
            else:
                with open(os.path.join(self.train_path, self.file_name_table[file]), "wb") as f:
                    pickle.dump(normal_data, f)
        print("success")
    
    def convertAngle(self):
        self.path_check(self.angle_train_path)
        self.path_check(self.angle_test_path)

        source_path = {"train": self.train_path, "test": self.test_path}
        angle_save = {"train": self.angle_train_path, "test": self.angle_test_path}
        folders = os.listdir(self.dataset_folder)

        for folder in folders:
            if folder == "train_angle" or folder == "test_angle":
                continue
            print(f"loading folder {folder}...")
            folder_files = os.listdir(os.path.join(self.dataset_folder, folder))
            for file in folder_files:
                with open(os.path.join(source_path[folder], file), "rb") as f_pkl:
                    data = pickle.load(f_pkl)
                angle_data = self.calc_angle(data)

                with open(os.path.join(angle_save[folder], (f"angle_{file}")), "wb") as f:
                    pickle.dump(angle_data, f)

        print("finished")
        
    def calc_angle(self, data):
        AngleList = np.zeros_like(data)
        for i, frame in enumerate(data):
            for joint in self.jointConnect:
                v = frame[joint[0]:joint[0]+3] - frame[joint[1]:joint[1]+3]
                AngleList[i][joint[0]:joint[0]+3] = list(self.get_angle(v))
        return AngleList

    def get_angle(self, v):
        axis_x = np.array([1,0,0])
        axis_y = np.array([0,1,0])
        axis_z = np.array([0,0,1])

        thetax = axis_x.dot(v)/(np.linalg.norm(axis_x) * np.linalg.norm(v))
        thetay = axis_y.dot(v)/(np.linalg.norm(axis_y) * np.linalg.norm(v))
        thetaz = axis_z.dot(v)/(np.linalg.norm(axis_z) * np.linalg.norm(v))

        return thetax, thetay, thetaz
    
    def name_mapping_txt(self):
        with open(f"{self.dataset_folder}/name_mapping.txt", "w") as f:
            for old, new in self.file_name_table.items():
                f.write(f"{old} >>> {new}")
                f.write("\n")

if __name__ == '__main__':
    p = prepare()
    p.name_mapping()
    p.divide()
    p.convertAngle()
    p.name_mapping_txt()