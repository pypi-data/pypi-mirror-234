import numpy as np
import struct
import gzip, pickle
from utils.pose_util import Coordinate
from utils.const import *
from utils.common_component import load_pickle_path
from enum import Enum
import pandas as pd
from zipfile import ZipFile
import sys

def get_version(class_name):
    return getattr(sys.modules[__name__], class_name)

def get_pickle_version(class_name):
    return getattr(sys.modules[__name__], class_name)

def read_zip_file(zip_file):
    with ZipFile(zip_file, 'r') as zip:
        file_name = zip.filelist[0].filename
        data = zip.read(file_name)
    unpack_data = []
    for cell in range(0, int(len(data)), 4):
        unpack_data.append(struct.unpack('i', data[cell : cell+4])[0])
    return unpack_data

def read_bin_file(bin_file):
    unpack_data = []
    with open(bin_file, "rb") as f:
        data = f.read()
    for cell in range(0, int(len(data)), 4):
        unpack_data.append(struct.unpack('i', data[cell : cell+4])[0])
    return unpack_data

def pop_header(data):
    casting_data = []
    header = data.pop(0)
    if header > 2213:    
        width = data.pop(0)
        height = data.pop(0)
    else:
        width = 480
        height = 640
    version = get_version(f"Version{header}")()
    line = version.row_len
    for line_cnt in range(0, len(data), line):
        casting_data.append(data[line_cnt : line_cnt + line])
    return casting_data, header, width, height

def bin_to_dataframe(bin_data):
    df = pd.DataFrame(bin_data)
    return df

def process_zip(file):
    bin_data = read_zip_file(file)
    data, header, width, height = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header, width, height

def process_bin(file):
    bin_data = read_bin_file(file)
    data, header, width, height = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header, width, height

def process_csv(file):
    df = pd.read_csv(file)
    return df

def get_header_data(file):
    if FileType.BIN.value in file:
        data, header, _, _ = process_bin(file)
    elif FileType.ZIP.value in file:
        data, header, _, _ = process_zip(file)
    elif FileType.CSV.value in file:
        header = 0
        data = process_csv(file)
    else:
        print('not defind file type')
        data = pd.DataFrame
        header = 0
    return header, data

class FileType(Enum):
    PICKLE = '.pickle'
    ZIP = '.zip'
    BIN = '.bin'
    CSV = '.csv'

class VersionCaster:
    def __init__(self, file):
        if FileType.PICKLE.value in file:
            frame_data = load_pickle_path(file)
            if 'header' in frame_data:
                header = frame_data["header"]
            else :
                header = 2113
            print(f"header : {header}")
            self.pickle_version = get_version(f"Version{header}")()
            self.use_data = self.pickle_version.get_data(frame_data)
        else:
            data, header, width, height = process_bin(file)
            print(f"header : {header}")
            header, frame_data = get_header_data(file)
            self.bin_version = get_version(f"Version{header}")()
            self.bin_version.setScale(width, height)
            self.use_data = self.bin_version.get_data(frame_data)
    
    def make_pickle(self, path):
        pickle_data = self.use_data.copy()
        with gzip.open(f"{path}.pickle", "wb") as f:
            pickle.dump(pickle_data, f)
    
    # labeling data 추가해서 저장 Pickle Type에 따라서 

class Version:
    def __init__(self):
        self.header = 1010
        self.row_len = 42
        self.status_kind = ["UP", "DOWN"]
        self.info_index = {"time": 0, "status": 1, "pose": (2, 41), "reps": 41}
        self.width = 480
        self.height = 640
        self.body_list = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, 
                LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
                LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
    
    def setScale(self, width, height):
        self.width = width
        self.height = height

    def make_pickle(self, path, frame_data):
        data = self.get_data(frame_data)
        with gzip.open(path, "wb") as f:
            pickle.dump(data, f)

    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "pose":
                    zip_pose = frame[info_index[key][0]: info_index[key][1]]
                    zip_idx = 0
                    pose = []
                    for idx in range(33):
                        if idx in self.body_list:
                            pose.append(Coordinate(zip_pose[zip_idx * 3], zip_pose[zip_idx * 3 + 1], zip_pose[zip_idx * 3 + 2]))
                            zip_idx += 1
                        else:
                            pose.append(Coordinate(0, 0, 0))
                    info_data[key].append(pose)
                elif key == "status":
                    info_data[key].append(self.status_kind[frame[info_index[key]]])
                else:
                    info_data[key].append(frame[info_index[key]])
        info_data['header'] = self.header
        info_data['width'] = self.width
        info_data['height'] = self.height
        return info_data

# CSV
class Version0(Version):
    def __init__(self):
        super().__init__()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)    
    
class Version1000(Version):
    def __init__(self):
        super().__init__()
        self.header = 1000
        self.info_index = {"time": 0, "status": 1, "reps": 2, "pose": (3, 102)}
        self.row_len = 102
        self.status_kind = ["UP", "MIDDLE", "DOWN", "RESTING"]
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version1010(Version):
    def __init__(self):
        super().__init__()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version1110(Version):
    def __init__(self):
        super().__init__()
        self.header = 1110
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version1111(Version):
    def __init__(self):
        super().__init__()
        self.header = 1111
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version2113(Version):
    def __init__(self):
        super().__init__()
        self.header = 2113
        self.info_index = {"time": 0, "status": 1, "reps": 2, "pose": (3, 69)}
        self.row_len = 69
        self.status_kind = ["UP", "MIDDLE", "DOWN", "RESTING"]
        self.body_list = [
            LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_PINKY, RIGHT_PINKY, LEFT_INDEX, RIGHT_INDEX, LEFT_THUMB, RIGHT_THUMB, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE,
            LEFT_HEEL, RIGHT_HEEL, LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,]
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version2213(Version):
    def __init__(self):
        super().__init__()
        self.header = 2213
        self.info_index = {"time": 0, "status": 1, "reps": 2, "pose": (3, 69)}
        self.row_len = 69
        self.status_kind = ["UP", "MIDDLE", "DOWN", "RESTING"]
        self.body_list = [
            LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_PINKY, RIGHT_PINKY, LEFT_INDEX, RIGHT_INDEX, LEFT_THUMB, RIGHT_THUMB, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE,
            LEFT_HEEL, RIGHT_HEEL, LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,]
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        return super().get_data(frame_data)

class Version2314(Version):
    def __init__(self):
        super().__init__()
        self.header = 2314
        self.width = 480
        self.height = 640
        self.info_index = {"time": 0, "mlp_label": 1, "lstm_label": 2, "reps": 3, "pose": (4, 73)}
        self.row_len = 73
        self.mlp_kind = ["UP", "MIDDLE", "DOWN"]
        self.lstm_kind = ["EXERCISING", "RESTING"]
        self.body_list = [
            NOSE,
            LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_PINKY, RIGHT_PINKY, LEFT_INDEX, RIGHT_INDEX, LEFT_THUMB, RIGHT_THUMB, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE,
            LEFT_HEEL, RIGHT_HEEL, LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,]
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "pose":
                    zip_pose = frame[info_index[key][0]: info_index[key][1]]
                    zip_idx = 0
                    pose = []
                    for idx in range(33):
                        if idx in self.body_list:
                            pose.append(Coordinate(zip_pose[zip_idx * 3], zip_pose[zip_idx * 3 + 1], zip_pose[zip_idx * 3 + 2]))
                            zip_idx += 1
                        else:
                            pose.append(Coordinate(0, 0, 0))
                    info_data[key].append(pose)
                elif key == "mlp_label":
                    info_data[key].append(self.mlp_kind[frame[info_index[key]]])
                elif key == "lstm_label":
                    info_data[key].append(self.lstm_kind[frame[info_index[key]]])
                else:
                    info_data[key].append(frame[info_index[key]])
        info_data['header'] = self.header
        info_data['width'] = self.width
        info_data['height'] = self.height
        return info_data

# 태권도 헤더

class Version9999(Version):
    def __init__(self):
        super().__init__()
        self.header = 9999
        self.info_index = {"time": 0, "red": (1, 100), "blue": (101, 200), "width": 201, "height": 202}
        self.row_len = 202
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                info_data[key].append(frame[info_index[key]])
        return info_data

class Version9998(Version):
    def __init__(self):
        super().__init__()
        self.header = 9998
        self.info_index = {"time": 0,"pose": (1, 100), "red": (101, 200), "blue": (201, 300), "width": 301, "height": 302, "lstm_label": 303}
        self.row_len = 303
        self.lstm_kind = [
            "STANDBY"
            "SIDE_KICK_MIDDLE", 
            "SIDE_KICK_UPPER",
            "FRONT_KICK_MIDDLE",
            "FRONT_KICK_UPPER",
            "DOWNWARD_KICK",
            "ROUND_KICK_MIDDLE",
            "ROUND_KICK_UPPER",
            "BACK_KICK_MIDDLE",
            "BACK_KICK_UPPER",
            "BACK_ROUND_KICK_MIDDLE",
            "BACK_ROUND_KICK_UPPER",
            "TURN_ROUND_KICK_MIDDLE",
            "TURN_ROUND_KICK_UPPER"
            ]
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "lstm_label":
                    info_data[key].append(self.lstm_kind[frame[info_index[key]]])
                info_data[key].append(frame[info_index[key]])
        return info_data
    
class Version9997(Version):
    def __init__(self):
        super().__init__()
        self.header = 9997
        self.info_index = {"time": 0, "pose": (1, 100), "width": 101, "height": 102}
        self.row_len = 102
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                info_data[key].append(frame[info_index[key]])
        return info_data
    
class Version9996(Version):
    def __init__(self):
        super().__init__()
        self.header = 9996
        self.info_index = {"time": 0,"pose": (1, 100), "width": 101, "height": 102, "label": 103}
        self.row_len = 103
        self.lstm_kind = [
            "STANDBY"
            "SIDE_KICK_MIDDLE", 
            "SIDE_KICK_UPPER",
            "FRONT_KICK_MIDDLE",
            "FRONT_KICK_UPPER",
            "DOWNWARD_KICK",
            "ROUND_KICK_MIDDLE",
            "ROUND_KICK_UPPER",
            "BACK_KICK_MIDDLE",
            "BACK_KICK_UPPER",
            "BACK_ROUND_KICK_MIDDLE",
            "BACK_ROUND_KICK_UPPER",
            "TURN_ROUND_KICK_MIDDLE",
            "TURN_ROUND_KICK_UPPER",
            "NONE"
            ]
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "lstm_label":
                    info_data[key].append(self.lstm_kind[frame[info_index[key]]])
                info_data[key].append(frame[info_index[key]])
        return info_data
    
class Version9995(Version):
    def __init__(self):
        super().__init__()
        self.header = 9995
        self.info_index = {"time": 0,"pose": (1, 100), "width": 101, "height": 102, "label": 103}
        self.row_len = 103
        self.lstm_kind = TAEKWONDO_LABEL
        self.body_list = ALLBODY_CONST_DICTIONARY.values()
    def setScale(self, width, height):
        return super().setScale(width, height)
    def get_data(self, frame_data):
        if type(frame_data) is dict:
            return frame_data
        frame_data = frame_data.to_numpy()
        frame_data = np.reshape(frame_data, (-1, self.row_len))
        info_index = self.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "lstm_label":
                    info_data[key].append(self.lstm_kind[frame[info_index[key]]])
                info_data[key].append(frame[info_index[key]])
        return info_data