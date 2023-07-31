import bpy
import os
from mathutils import Vector
import numpy as np
import pickle 

HOME_FILE_PATH = os.path.abspath('homefile.blend')
SRC_DATA_DIR ='Tpos_fbx'
OUT_DATA_DIR ='Tpos_data'

MIN_NR_FRAMES = 64
RESOLUTION = (512, 512)

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

# BASE_JOINT_NAMES = ['Head', 'Neck',
#                     'RightArm', 'RightForeArm', 'RightHand', 'LeftArm', 'LeftForeArm', 'LeftHand',
#                     'Hips', 'RightUpLeg', 'RightLeg', 'RightFoot', 'LeftUpLeg', 'LeftLeg', 'LeftFoot',
#                     'LeftFoot_End', 'RightFoot_End',
#                     'LeftHandThumb1', 'LeftHandThumb2', 'LeftHandThumb3', 
#                     'LeftHandIndex1', 'LeftHandIndex2', 'LeftHandIndex3', 
#                     'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3', 
#                     'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 
#                     'LeftHandPinky1', 'LeftHandPinky2', 'LeftHandPinky3', 
#                     'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 
#                     'RightHandIndex1', 'RightHandIndex2', 'RightHandIndex3', 
#                     'RightHandMiddle1', 'RightHandMiddle2', 'RightHandMiddle3', 
#                     'RightHandRing1', 'RightHandRing2', 'RightHandRing3', 
#                     'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3'
#                     ]

# BASE_JOINT_NAMES = ['Head_01', 'Nack_01',
#                     'R_Arm01', 'R_Elbow01', 'R_Wrist', 'L_Arm01', 'L_Elbow01', 'L_Wrist',
#                     'Root_01', 'R_Leg', 'R_Knee', 'R_Ankle_01', 'L_Leg', 'L_Knee', 'L_Ankle_01',
#                     'L_Index_01', 'L_Pinky_01', 'R_Index_01', 'R_Pinky_01',
#                     'L_Toe_01', 'R_Toe_01'
#                     ]

#Number of joints to be used from MixamoRig
joint_names = ['mixamorig:' + x for x in BASE_JOINT_NAMES]

def fbx2joint():
    
    #Remove 'Cube' object if exists in the scene
    if bpy.data.objects.get('Cube') is not None:
        cube = bpy.data.objects['Cube']
        bpy.data.objects.remove(cube)
    
    #Intensify Light Point in the scene
    if bpy.data.objects.get('Light') is not None:
        bpy.data.objects['Light'].data.energy = 2
        bpy.data.objects['Light'].data.type = 'POINT'
    
    #Set resolution and it's rendering percentage
    bpy.data.scenes['Scene'].render.resolution_x = RESOLUTION[0]
    bpy.data.scenes['Scene'].render.resolution_y = RESOLUTION[1]
    bpy.data.scenes['Scene'].render.resolution_percentage = 100
    
    #Base file for blender
    bpy.ops.wm.save_as_mainfile(filepath=HOME_FILE_PATH)
    
    #Get animation(.fbx) file paths
    anims_path = os.listdir(SRC_DATA_DIR)
    
    #Make OUT_DATA_DIR
    if not os.path.exists(OUT_DATA_DIR):
        os.makedirs(OUT_DATA_DIR)    

    for anim_name in anims_path:
        anim_file_path = os.path.join(SRC_DATA_DIR,anim_name)
        save_npy_dir = os.path.join(OUT_DATA_DIR,'npy')
        save_pkl_dir = os.path.join(OUT_DATA_DIR,'pkl')
        #Make save_dir
        if not os.path.exists(save_npy_dir):
            os.makedirs(save_npy_dir)
        if not os.path.exists(save_pkl_dir):
            os.makedirs(save_pkl_dir)
        
        #Load HOME_FILE and .fbx file
        bpy.ops.wm.read_homefile(filepath=HOME_FILE_PATH)
        bpy.ops.import_scene.fbx(filepath=anim_file_path)
        
        #End Frame Index for .fbx file
        frame_end = bpy.data.actions[0].frame_range[1]
        
        motion = []
        for i in range(int(frame_end)+1):
            
            bpy.context.scene.frame_set(i)
            
            bone_struct = bpy.data.objects['Armature'].pose.bones
            armature = bpy.data.objects['Armature']

            # print(bpy.data.objects.keys())
            # bone_struct = bpy.data.objects['mixamorig:Hips'].pose.bones
            # armature = bpy.data.objects['mixamorig:Hips']

            # bone_struct = bpy.data.objects['People'].pose.bones
            # armature = bpy.data.objects['People']

            # bone_list = [pBone for pBone in bone_struct]
            # print(f"Bones name: {bone_list}")

            out_dict = {'pose_keypoints_3d': []}
            for name in BASE_JOINT_NAMES:
            # for name in joint_names:
                global_location = armature.matrix_world @ bone_struct[name].matrix @ Vector((0, 0, 0))
                l = [-global_location[0], global_location[2], global_location[1]]
                out_dict['pose_keypoints_3d'].extend(l)
            motion.append(out_dict['pose_keypoints_3d'])
            
        if not os.path.exists(save_npy_dir):
            os.makedirs(save_npy_dir)
        if not os.path.exists(save_pkl_dir):
            os.makedirs(save_pkl_dir)
        
        np.save(save_npy_dir+'/'+'{i}.npy'.format(i=anim_name.split('.')[0].replace(" ", "")),motion)
        file_name = anim_name.split('.')[0].replace(" ", "")
        motion = np.array(motion)
        with open(f'{save_pkl_dir}/{file_name}.pkl', 'wb')as fpick:
            pickle.dump(motion, fpick)
        
if __name__ == '__main__':
    fbx2joint()