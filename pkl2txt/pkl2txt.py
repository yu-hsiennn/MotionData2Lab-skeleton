import os, pickle

file_name = "take004_chr01"

pkl_folder = "pkl_file"
saved_path = "unity_txt_file"

def read(file):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data

def print_list(data):
    print(data[1])
    print(data[2])

def Data_processing(data):
    world_positions_list = []
    for frame in data:
        temp_str = ""
        for idx, skeletons in enumerate(frame):
            # if idx == 24:
            #     temp_str += (str((frame[27]+frame[36])/2) + " ")
            # elif idx == 25:
            #     temp_str += (str((frame[28]+frame[37])/2) + " ")
            # elif idx == 26:
            #     temp_str += (str((frame[29]+frame[38])/2) + ",")
            if idx % 3 == 2:
                temp_str += (str((skeletons)) + ",")
            else:
                temp_str += (str(skeletons) + " ")
        temp_str = temp_str[:len(temp_str)-1]
        world_positions_list.append(temp_str)
    return world_positions_list

def list2txt(save_path, data_list):
    with open(save_path, 'w') as f:
        for coordinates in data_list:
            f.write(coordinates)
            f.write("\n")

def batch_processing(source):
    all_pkl_files = os.listdir(source)
    for file in all_pkl_files:
        new_file_name = file[:-3] + "txt"
        list2txt(os.path.join(saved_path, new_file_name), Data_processing(read(os.path.join(source, file))))
    print("done!")

# GT_data = read(f"{file_name}_ori.pkl")
# model_data = read(f"{file_name}.pkl")

# print("---------GT data---------")
# print_list(GT_data)
# print("---------model data----------")
# print_list(model_data)

# list2txt(f"{save_path}/{file_name}.txt", Data_processing(model_data))

# batch processing
batch_processing(pkl_folder)
