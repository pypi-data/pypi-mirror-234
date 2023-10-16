from zipfile import ZipFile
import struct
import pandas as pd
from enum import Enum
from utils.version import VersionCaster

class Type(Enum):
    ZIP = '.zip'
    BIN = '.bin'
    CSV = '.csv'

class ExerciseType(Enum):
    CENTER = '.csv'
    LEFT = 'left.csv'
    RIGHT = 'right.csv'

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
    version = VersionCaster(header)
    line = version.get_version_casting_line()
    for line_cnt in range(0, len(data), line):
        casting_data.append(data[line_cnt : line_cnt + line])
    return casting_data, header

def bin_to_dataframe(bin_data):
    df = pd.DataFrame(bin_data)
    return df

def process_zip(file):
    bin_data = read_zip_file(file)
    data, header = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header

def process_bin(file):
    bin_data = read_bin_file(file)
    data, header = pop_header(bin_data)
    df = bin_to_dataframe(data)
    return df, header

def process_csv(file):
    df = pd.read_csv(file)
    return df


def process(file, z_weight=None, frame_weight = 1, direct = None):
    if Type.BIN.value in file:
        data, header = process_bin(file)
    elif Type.ZIP.value in file:
        data, header = process_zip(file)
    elif Type.CSV.value in file:
        header = 0
        data = process_csv(file)
    else:
        data = pd.DataFrame
        header = 0
    version = VersionCaster(header, direct=direct)   
    df_to_list = data.to_numpy().tolist()
    convert_data = version.get_version_casting_convert_pose_data(df_to_list, z_weight, frame_weight)
    info_data = version.get_data(df_to_list)
    # print("* --------------------- * Frame data * --------------------- * ")
    # print(data)
    # print("* --------------------- * ---------- * --------------------- * ")
    return convert_data, info_data, header

def get_side_visibility(file):
    if ExerciseType.LEFT.value in file:
        return 'LEFT'
    elif ExerciseType.RIGHT.value in file:
        return 'RIGHT'
    else:
        return 'CENTER'