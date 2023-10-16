import os


#------------------------------------------------------------------------
# Path 
DIR_PATH = os.getcwd()
KNN_PATH = DIR_PATH + '/data/knnData'
SYNC_PATH = DIR_PATH + "/data/syncData"
DANCE_DATA_PATH = DIR_PATH + '/data/danceData'

DANCE_VIDEO_PATH = DANCE_DATA_PATH + '/video'
DANCE_PICKLE_PATH = DANCE_DATA_PATH + '/pickle'
DANCE_IMG_PATH = DANCE_DATA_PATH + '/imgs'
DANCE_AUDIO_PATH = DANCE_DATA_PATH + '/audio'
DANCE_AUDIO_COMMON_PATH = DANCE_AUDIO_PATH + '/common/'

SYNC_STANDARD_PATH = SYNC_PATH + '/Standard'
SYNC_COMPARE_PATH = SYNC_PATH + '/Compare'

SYNC_STANDARD_PICKLE_PATH = SYNC_STANDARD_PATH + '/pickle'
SYNC_STANDARD_IMG_PATH = SYNC_STANDARD_PATH + '/imgs'
SYNC_COMPARE_PICKLE_PATH = SYNC_COMPARE_PATH + '/pickle'
SYNC_COMPARE_IMG_PATH = SYNC_COMPARE_PATH + '/imgs'

AUDIO_JSON_PATH = DIR_PATH + "/audio_info.json"
NAS_PATH = "/Volumes/Multimedia/댄스"
MLP_PATH_DATA = "/Volumes/FrameData/mlp/data"
MLP_PATH = "/Volumes/FrameData/mlp"
LSTM_PATH = "/Volumes/FrameData/lstm"
TRANSFORMER_PATH = "/Volumes/FrameData/transformer"
LINUX_LSTM_PATH = "/home/jinwoo/jinwoo/lstm"

TAEKWONDO_PATH = "/Volumes/FrameData/TaeKwondo"
TAEKWONDO_LINUX_PATH = "/home/jinwoo/jinwoo/frameData/TaeKwondo"

POSE_MEASURE_SAVE_PATH = DIR_PATH + "/poseutil/utils/poseMeasure.py"

KT_LOGIC_COACHING_PATH = DIR_PATH + "/ktLogicCoaching"

NO_COUNTING_PATH = "/Volumes/FrameData/no_counting_data"
APP_LIST = ["pose-test-app", "gymmate-app"]

MAPPING_MAP = {
    "Weight/DumbbellBenchPress": ["Weight/BarbellBenchPress"],
    "Weight/DumbbellPullover" : ["Weight/BarbellPullover"],
    "Weight/BentOverLateralRaise" : ["Beginner/BandBentOverLateralRaise", "Beginner/WaterBottleBentOverLateralRaise"],
    "Weight/BentOverDumbbellRow" : ["Beginner/BentOverWaterBottleRow"],
    "Weight/DumbbellConcentrationCurl" : ["Beginner/BandConcentrationCurl", "Beginner/WaterBottleConcentrationCurl"],
    "Weight/DumbbellShoulderPress" : ["Beginner/WaterBottleShoulderPress"],
    "Weight/DumbbellSideBend" : ["Beginner/WaterBottleSideBend"],
    "Weight/FrontLateralRaise" : ["Beginner/BandFrontLateralRaise", "Beginner/WaterBottleFrontLateralRaise"],
    "Weight/OneArmDumbbellTricepsKickback" : ["Beginner/OneArmWaterBottleTricepsKickback"],
    "Weight/OneArmOverheadDumbbellTricepsExtension" : ["Beginner/OneArmOverheadWaterBottleTricepsExtension"],
    "Weight/OneDumbbellFrontRaise" : ["Beginner/BandFrontRaise", "Beginner/WaterBottleFrontRaise"],
    "Weight/ReverseWristCurl" : ["Beginner/WaterBottleReverseWristCurl"],
    "Weight/SideLateralRaise" : ["Beginner/BandSideLateralRaise", "Beginner/WaterBottleSideLateralRaise"],
    "Weight/StandingAlternateDumbbellCurl" : ["Beginner/StandingAlternateBandCurl", "Beginner/StandingAlternateWaterBottleCurl"],
    "Weight/StandingHammerCurl" : ["Beginner/StandingBandHammerCurl", "Beginner/StandingWaterBottleHammerCurl"]
}
#------------------------------------------------------------------------
# list view Setup
EMBEDDINGLIST = ["UPPER", "BODYNOSE", "LOWER","FULL", "HAND", "LOWERYANG", "TAEKWONDO"]
SIDECHECKLIST = ["SIDE", "FRONT"]
CONTENTLIST = ["Weight", "Golf", "Yang", "Beginner", "Test"]
ANGLELIST = [
    "NONE",  
    "getKneeHipAnkleAngle,xyz,avg", "getElbowWristShoulderAngle,xyz,avg",
    "getShoulderHipMinusPlane,xy,x,11", "getHipAnkleShoulderMinusAngle,xy,z,11",
    "getElbowWristShoulderMinusAngle,xy,z,11", "getHipShoulderKneeMinusAngle,xy,z,11",
    "getShoulderWristHipMinusAngle,xy,z,11", "getShoulderElbowHipMinusAngle,xy,z,11",
    "getKneeHipAnkleAngle,xy,avg", "getShoulderElbowHipAngle,xyz,avg",
    "getShoulderElbowHipAngle,xy,avg", "getKneeHipAnkleMinusAngle,xy,z,11",
    "getElbowWristShoulderAngle,xy,avg", "getKneeHipAnkleMinusAngle,xyz,z,25",
    "getElbowWristShoulderPlusAngle,xyz,y,11", "getHipShoulderKneePlusAngle,xy,y,15",
]
#------------------------------------------------------------------------
# Equation
COSINE = 0
LINEAR = 1
PARABOLA = 2
#------------------------------------------------------------------------
OFFSET = 20
CUTLINE = 75
#-------------------------------------------------------------------------
# Body Const
NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
LEFT_MOUTH = 9
RIGHT_MOUTH = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32
CENTER = 33

# Hand Const
HAND_WRIST = 0
HAND_THUMB_CMC = 1
HAND_THUMB_MCP = 2
HAND_THUMB_IP = 3
HAND_THUMB_TIP = 4
HAND_INDEX_FINGER_MCP = 5
HAND_INDEX_FINGER_PIP = 6
HAND_INDEX_FINGER_DIP = 7
HAND_INDEX_FINGER_TIP = 8
HAND_MIDDLE_FINGER_MCP = 9
HAND_MIDDLE_FINGER_PIP = 10
HAND_MIDDLE_FINGER_DIP = 11
HAND_MIDDLE_FINGER_TIP = 12
HAND_RING_FINGER_MCP = 13
HAND_RING_FINGER_PIP = 14
HAND_RING_FINGER_DIP = 15
HAND_RING_FINGER_TIP = 16
HAND_PINKY_MCP = 17
HAND_PINKY_PIP = 18
HAND_PINKY_DIP = 19
HAND_PINKY_TIP = 20


ALL = 33
TORSO_MULTIPLIER = 2.5


# 몸만
def poseConnection_body(frame):
    connectionList = []
    # 왼쪽 어깨 ->
    connectionList.append([frame[LEFT_SHOULDER], frame[RIGHT_SHOULDER]])
    connectionList.append([frame[LEFT_SHOULDER], frame[LEFT_HIP]])
    connectionList.append([frame[LEFT_SHOULDER], frame[LEFT_ELBOW]])
    # 오른쪽 어깨 ->
    connectionList.append([frame[RIGHT_SHOULDER], frame[RIGHT_HIP]])
    connectionList.append([frame[RIGHT_SHOULDER], frame[RIGHT_ELBOW]])
    connectionList.append([frame[RIGHT_ELBOW], frame[RIGHT_WRIST]])

    connectionList.append([frame[LEFT_ELBOW], frame[LEFT_WRIST]])

    connectionList.append([frame[RIGHT_HIP], frame[LEFT_HIP]])

    connectionList.append([frame[LEFT_HIP], frame[LEFT_KNEE]])
    connectionList.append([frame[LEFT_KNEE], frame[LEFT_ANKLE]])

    connectionList.append([frame[RIGHT_HIP], frame[RIGHT_KNEE]])
    connectionList.append([frame[RIGHT_KNEE], frame[RIGHT_ANKLE]])

    return connectionList


# 손, 발 포함
def poseConnection(frame):
    connectionList = []
    # 왼쪽 어깨 ->
    connectionList.append([frame[LEFT_SHOULDER], frame[RIGHT_SHOULDER]])
    connectionList.append([frame[LEFT_SHOULDER], frame[LEFT_HIP]])
    connectionList.append([frame[LEFT_SHOULDER], frame[LEFT_ELBOW]])
    # 오른쪽 어깨 ->
    connectionList.append([frame[RIGHT_SHOULDER], frame[RIGHT_HIP]])
    connectionList.append([frame[RIGHT_SHOULDER], frame[RIGHT_ELBOW]])
    connectionList.append([frame[RIGHT_ELBOW], frame[RIGHT_WRIST]])

    connectionList.append([frame[LEFT_ELBOW], frame[LEFT_WRIST]])

    connectionList.append([frame[RIGHT_HIP], frame[LEFT_HIP]])

    connectionList.append([frame[LEFT_HIP], frame[LEFT_KNEE]])
    connectionList.append([frame[LEFT_KNEE], frame[LEFT_ANKLE]])

    connectionList.append([frame[RIGHT_HIP], frame[RIGHT_KNEE]])
    connectionList.append([frame[RIGHT_KNEE], frame[RIGHT_ANKLE]])

    connectionList.append([frame[LEFT_ANKLE], frame[LEFT_FOOT_INDEX]])
    connectionList.append([frame[LEFT_ANKLE], frame[LEFT_HEEL]])
    connectionList.append([frame[LEFT_HEEL], frame[LEFT_FOOT_INDEX]])

    connectionList.append([frame[RIGHT_ANKLE], frame[RIGHT_FOOT_INDEX]])
    connectionList.append([frame[RIGHT_ANKLE], frame[RIGHT_HEEL]])
    connectionList.append([frame[RIGHT_HEEL], frame[RIGHT_FOOT_INDEX]])

    # 손 ->
    connectionList.append([frame[LEFT_WRIST], frame[LEFT_THUMB]])
    connectionList.append([frame[RIGHT_WRIST], frame[RIGHT_THUMB]])

    connectionList.append([frame[LEFT_WRIST], frame[LEFT_INDEX]])
    connectionList.append([frame[LEFT_WRIST], frame[LEFT_PINKY]])
    connectionList.append([frame[LEFT_PINKY], frame[LEFT_INDEX]])

    connectionList.append([frame[RIGHT_WRIST], frame[RIGHT_INDEX]])
    connectionList.append([frame[RIGHT_WRIST], frame[RIGHT_PINKY]])
    connectionList.append([frame[RIGHT_PINKY], frame[RIGHT_INDEX]])

    return connectionList


ALL_BODY_STR_LIST = [
    "NOSE", "LEFT_EYE_INNER","LEFT_EYE", "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER", "LEFT_EAR",
    "RIGHT_EAR", "LEFT_MOUTH", "RIGHT_MOUTH", "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY",
    "RIGHT_PINKY", "LEFT_INDEX", "RIGHT_INDEX", "LEFT_THUMB", "RIGHT_THUMB",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE",
    "LEFT_HEEL", "RIGHT_HEEL", "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"
]

ALLBODY_CONST_DICTIONARY = {
    "NOSE": NOSE, 
    "LEFT_EYE_INNER": LEFT_EYE_INNER,
    "LEFT_EYE": LEFT_EYE,
    "LEFT_EYE_OUTER": LEFT_EYE_OUTER,
    "RIGHT_EYE_INNER": RIGHT_EYE_INNER,
    "RIGHT_EYE": RIGHT_EYE,
    "RIGHT_EYE_OUTER": RIGHT_EYE_OUTER,
    "LEFT_EAR": LEFT_EAR,
    "RIGHT_EAR": RIGHT_EAR,
    "LEFT_MOUTH": LEFT_MOUTH,
    "RIGHT_MOUTH" : RIGHT_MOUTH ,
    "LEFT_SHOULDER" : LEFT_SHOULDER ,
    "RIGHT_SHOULDER" : RIGHT_SHOULDER ,
    "LEFT_ELBOW" : LEFT_ELBOW ,
    "RIGHT_ELBOW" : RIGHT_ELBOW ,
    "LEFT_WRIST" : LEFT_WRIST ,
    "RIGHT_WRIST" : RIGHT_WRIST ,
    "LEFT_PINKY" : LEFT_PINKY ,
    "RIGHT_PINKY" : RIGHT_PINKY ,
    "LEFT_INDEX" : LEFT_INDEX ,
    "RIGHT_INDEX" : RIGHT_INDEX ,
    "LEFT_THUMB" : LEFT_THUMB ,
    "RIGHT_THUMB" : RIGHT_THUMB ,
    "LEFT_HIP" : LEFT_HIP ,
    "RIGHT_HIP" : RIGHT_HIP ,
    "LEFT_KNEE" : LEFT_KNEE ,
    "RIGHT_KNEE" : RIGHT_KNEE ,
    "LEFT_ANKLE" : LEFT_ANKLE ,
    "RIGHT_ANKLE" : RIGHT_ANKLE ,
    "LEFT_HEEL" : LEFT_HEEL ,
    "RIGHT_HEEL" : RIGHT_HEEL ,
    "LEFT_FOOT_INDEX" : LEFT_FOOT_INDEX ,
    "RIGHT_FOOT_INDEX" : RIGHT_FOOT_INDEX
}

#------------------------------------------------------------------------
# Color Const RGB
RED = (200, 50, 50)
ORANGE = (255, 153, 50)
YELLOW = (255, 255, 50)
GREEN = (153, 255, 50)
SKY = (100, 255, 255)
DARK_SKY = (102, 178, 255)
PURPLE = (178, 102, 255)
BLUE = (51, 51, 255)
PINK = (255, 102, 255)
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR = [BLUE, BLACK, PINK, YELLOW, GREEN, SKY, DARK_SKY, ORANGE, RED, PURPLE, GRAY]

# Color Const BGR
BGR_RED = (50, 50, 200)
BGR_YELLOW = (50, 255, 255)
BGR_GREEN = (50, 255, 153)

#------------------------------------------------------------------------
RESOLUTION = (480, 640)

body_setting_id = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_KNEE, RIGHT_KNEE,
                   LEFT_ELBOW, LEFT_WRIST, LEFT_ANKLE,  
                   RIGHT_ELBOW, RIGHT_WRIST, RIGHT_ANKLE,
                   RIGHT_HIP, LEFT_HIP]

body_setting_id_right = [RIGHT_SHOULDER, RIGHT_KNEE,
                         RIGHT_ELBOW, RIGHT_WRIST, RIGHT_ANKLE,
                         RIGHT_HIP]

body_setting_id_left = [LEFT_SHOULDER, LEFT_KNEE,
                        LEFT_ELBOW, LEFT_WRIST, LEFT_ANKLE,
                        LEFT_HIP]

foot_setting_id = [LEFT_FOOT_INDEX, LEFT_HEEL, RIGHT_FOOT_INDEX, RIGHT_HEEL]
foot_setting_id_left = [LEFT_FOOT_INDEX, LEFT_HEEL]
foot_setting_id_right = [RIGHT_FOOT_INDEX, RIGHT_HEEL]
hand_setting_id_left = [LEFT_THUMB, LEFT_PINKY, LEFT_INDEX]
hand_setting_id_right = [RIGHT_THUMB, RIGHT_PINKY, RIGHT_INDEX]

VECTORS = [
    (LEFT_SHOULDER, RIGHT_SHOULDER),
    (LEFT_SHOULDER, LEFT_HIP),
    (RIGHT_SHOULDER, RIGHT_HIP),
    (LEFT_HIP, RIGHT_HIP),
    (LEFT_HIP, LEFT_KNEE),
    (RIGHT_HIP, RIGHT_KNEE),
    (LEFT_KNEE, LEFT_ANKLE),
    (RIGHT_KNEE, RIGHT_ANKLE),
    (LEFT_ANKLE, RIGHT_ANKLE),
]

DEFAULT_LOWER_BODY_SET = [
    (LEFT_KNEE, 'left_knee'), 
    (RIGHT_KNEE, 'right_knee'), 
    (LEFT_ANKLE, 'left_ankle'), 
    (RIGHT_ANKLE,'right_ankle'), 
    (LEFT_SHOULDER, 'left_shoulder'), 
    (RIGHT_SHOULDER, 'right_shoulder')
    ]

NAME = [
    "shoulder-shoulder",
    "leftShoulder-leftHip",
    "rightShoulder-rightHip",
    "leftHip-rightHip",
    "leftHip-leftKnee",
    "rightHip-rightKnee",
    "leftKnee-leftAnkle",
    "rightKnee-rightAnkle",
    "leftAnkle-rightAnkle"
]

UPPER = "UPPER"
UPPERLEFT = "UPPERLEFT"
UPPERRIGHT = "UPPERRIGHT"
LOWER = "LOWER"
LOWERLEFT = "LOWERLEFT"
LOWERRIGHT = "LOWERRIGHT"
FULL = "FULL"
FULLLEFT = "FULLLEFT"
FULLRIGHT = "FULLRIGHT"
HAND = "HAND"
HANDLEFT = "HANDLEFT"
HANDRIGHT = "HANDRIGHT"
BODYNOSE = "BODYNOSE"
BODYNOSELEFT = "BDOYNOSELEFT"
BODYNOSERIGHT = "BODYNOSERIGHT"
LOWERYANG = "LOWERYANG"
LOWERYANGLEFT = "LOWERYANGLEFT"
LOWERYANGRIGHT = "LOWERYANGRIGHT"


TAEKWONDO_EMBEDDING = [
    LEFT_SHOULDER, RIGHT_SHOULDER,
    LEFT_HIP, RIGHT_HIP,
    LEFT_KNEE, RIGHT_KNEE,
    LEFT_ANKLE, RIGHT_ANKLE,
    LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,
    LEFT_HEEL, RIGHT_HEEL
]

SYNC_TARGET_LOWER = [
    [LEFT_SHOULDER, RIGHT_SHOULDER],
    [LEFT_SHOULDER, LEFT_HIP],
    [RIGHT_SHOULDER, RIGHT_HIP],
    [LEFT_HIP, RIGHT_HIP],
    [LEFT_HIP, LEFT_KNEE],
    [RIGHT_HIP, RIGHT_KNEE],
    [LEFT_KNEE, LEFT_ANKLE],
    [RIGHT_KNEE, RIGHT_ANKLE],
]

DANCE_TARGET_BODY = [
    [NOSE, LEFT_SHOULDER],
    [NOSE, RIGHT_SHOULDER],
    [LEFT_SHOULDER, LEFT_ELBOW],
    [LEFT_ELBOW, LEFT_WRIST],
    [LEFT_SHOULDER, LEFT_WRIST],
    [RIGHT_SHOULDER, RIGHT_ELBOW],
    [RIGHT_ELBOW, RIGHT_WRIST],
    [RIGHT_SHOULDER, RIGHT_WRIST],
    [LEFT_HIP, LEFT_KNEE],
    [LEFT_HIP, LEFT_ANKLE],
    [LEFT_HIP, RIGHT_HIP],
    [RIGHT_HIP, RIGHT_KNEE],
    [RIGHT_HIP, RIGHT_ANKLE],
    [LEFT_KNEE, LEFT_ANKLE],
    [LEFT_KNEE, RIGHT_ANKLE],
    [LEFT_KNEE, RIGHT_KNEE],
    [RIGHT_KNEE, LEFT_ANKLE],
    [RIGHT_KNEE, RIGHT_ANKLE],
    [LEFT_ANKLE, RIGHT_ANKLE],
]

DANCE_TARGET_BODY_STR = [
    "[NOSE, LEFT_SHOULDER]",
    "[NOSE, RIGHT_SHOULDER]",
    "[LEFT_SHOULDER, LEFT_ELBOW]",
    "[LEFT_ELBOW, LEFT_WRIST]",
    "[LEFT_SHOULDER, LEFT_WRIST]",
    "[RIGHT_SHOULDER, RIGHT_ELBOW]",
    "[RIGHT_ELBOW, RIGHT_WRIST]",
    "[RIGHT_SHOULDER, RIGHT_WRIST]",
    "[LEFT_HIP, LEFT_KNEE]",
    "[LEFT_HIP, LEFT_ANKLE]",
    '[LEFT_HIP, RIGHT_HIP]',
    "[RIGHT_HIP, RIGHT_KNEE]",
    "[RIGHT_HIP, RIGHT_ANKLE]",
    "[LEFT_KNEE, LEFT_ANKLE]",
    "[LEFT_KNEE, RIGHT_ANKLE]",
    "[LEFT_KNEE, RIGHT_KNEE]",
    "[RIGHT_KNEE, LEFT_ANKLE]",
    "[RIGHT_KNEE, RIGHT_ANKLE]",
    "[LEFT_ANKLE, RIGHT_ANKLE]",
    "TOTAL HAND"
]

DANCE_TARGET_HAND = [
    [HAND_WRIST, HAND_THUMB_TIP],
    [HAND_WRIST, HAND_INDEX_FINGER_MCP],
    [HAND_WRIST, HAND_PINKY_MCP],
    [HAND_INDEX_FINGER_MCP, HAND_INDEX_FINGER_TIP],
    [HAND_MIDDLE_FINGER_MCP, HAND_MIDDLE_FINGER_TIP],
    [HAND_RING_FINGER_MCP, HAND_RING_FINGER_TIP],
    [HAND_PINKY_MCP, HAND_PINKY_TIP]
]

DANCE_TARGET_HIP = [
    [LEFT_HIP, RIGHT_HIP]
]

DANCE_TARGET_ARM = [
    [LEFT_SHOULDER, LEFT_ELBOW],
    [LEFT_SHOULDER, LEFT_WRIST],
    [LEFT_SHOULDER, RIGHT_SHOULDER],
    [RIGHT_SHOULDER, RIGHT_ELBOW],
    [RIGHT_SHOULDER, RIGHT_WRIST],
    [LEFT_ELBOW, LEFT_WRIST],
    [LEFT_ELBOW, RIGHT_ELBOW],
    [RIGHT_ELBOW, RIGHT_WRIST],
]

DANCE_TARGET_BODY_RESULT = [
    "LEFT_SHOULDER, LEFT_ELBOW",
    "LEFT_ELBOW, LEFT_WRIST",
    "LEFT_SHOULDER, LEFT_WRIST",
    "RIGHT_SHOULDER, RIGHT_ELBOW",
    "RIGHT_ELBOW, RIGHT_WRIST",
    "RIGHT_SHOULDER, RIGHT_WRIST",
    "LEFT_HIP, LEFT_KNEE",
    "LEFT_KNEE, LEFT_ANKLE",
    "LEFT_HIP, LEFT_ANKLE",
    "RIGHT_HIP, RIGHT_KNEE",
    "RIGHT_KNEE, RIGHT_ANKLE",
    "RIGHT_HIP, RIGHT_ANKLE"
]

DANCE_TARGET_UPPER_BODY = [
    [LEFT_SHOULDER, RIGHT_SHOULDER],
    [LEFT_SHOULDER, LEFT_HIP],
    [LEFT_SHOULDER, RIGHT_HIP],
    [RIGHT_SHOULDER, LEFT_SHOULDER]
]

DANCE_TARGET_UPPER_BODY_RESULT = [
    "LEFT_SHOULDER, RIGHT_SHOULDER",
    "LEFT_SHOULDER, LEFT_HIP",
    "LEFT_SHOULDER, RIGHT_HIP",
    "RIGHT_SHOULDER, LEFT_SHOULDER"
]

DANCE_BODY = [LEFT_ANKLE,LEFT_KNEE,LEFT_HIP,LEFT_SHOULDER, LEFT_ELBOW,LEFT_WRIST,NOSE,
              RIGHT_ANKLE,RIGHT_KNEE,RIGHT_HIP,RIGHT_SHOULDER,RIGHT_ELBOW,RIGHT_WRIST]
DANCE_BODY_RESULT = ["LEFT_ANKLE","LEFT_KNEE","LEFT_HIP","LEFT_SHOULDER", "LEFT_ELBOW",'LEFT_WRIST','NOSE',
              "RIGHT_ANKLE","RIGHT_KNEE","RIGHT_HIP","RIGHT_SHOULDER","RIGHT_ELBOW","RIGHT_WRIST"]

BODY_SET = [LEFT_SHOULDER, RIGHT_SHOULDER,LEFT_HIP, RIGHT_HIP]

BODY_DOT = [
    0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28,
]
HAND_DOT = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
]
LEFT_LINK = [
    [12, 14], [14, 16], [12, 24], [24, 26], [26, 28], 
]
RIGHT_LINK = [
    [11, 13], [13, 15], [11, 23], [23, 25], [25, 27],
]
CENTER_LINK = [
    [11, 12], [23, 24]
]
HAND = [
    [0, 1], [1, 2], [2, 3], [3, 4], 
    [0, 5], [5, 6], [6, 7], [7, 8],
    [9, 10], [10, 11], [11, 12],
    [13, 14], [14, 15], [15, 16],
    [0, 17], [17, 18], [18, 19], [19, 20],
    [5, 9], [9, 13], [13, 17]
]

KEY_INFO_CAPTURE_LIVE_HEADER = [""]
KEY_INFO_CAPTURE_LIVE_HEADER = [""]
STATIC_HEADER = ["Width", "Height", "Origin", "Compare"]
DYNAMIC_HEADER = ["Total Score", "Frame Num", "Time"]
AUDIO_JSON_HEADER = ["name", "startPos", "interval"]

X = 'x'
Y = 'y'
Z = 'z'
XY = 'xy'
YZ = 'yz'
XZ = 'xz'
XYZ = 'xyz'

LEFT = 'left'
RIGHT = 'right'
AVG = 'avg'

COORD_LIST = [X, Y, Z]
EQUATION_LIST = ["MINUS", "PLUS"]
STANDARD_JOINT_LIST = [
    "LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE", "LEFT_ELBOW", "LEFT_WRIST", "LEFT_ANKLE"
]
STANDARD_JOINT_MAP = {
    LEFT_SHOULDER: "LEFT_SHOULDER",
    LEFT_HIP: "LEFT_HIP",
    LEFT_KNEE: "LEFT_KNEE",
    LEFT_ELBOW: "LEFT_ELBOW",
    LEFT_WRIST: "LEFT_WRIST",
    LEFT_ANKLE: "LEFT_ANKLE"
}

CONTENTS = ["Weight", "Yang", "Beginner"]

TAEKWONDO_LSTM_MAP = {
    "STANDBY" : 0 ,
    "SIDE_KICK" : 1 , 
    "FRONT_KICK" : 2 ,
    "DOWNWARD_KICK" : 3 ,
    "ROUND_KICK" : 4 ,
    "BACK_KICK" : 5 ,
    "BACK_ROUND_KICK" : 6 ,
    "TURN_ROUND_KICK" : 7 ,
}

TAEKWONDO_LSTM_MAP_REVERSE = {
    0 : "STANDBY" ,
    1 : "SIDE_KICK", 
    2 : "FRONT_KICK"  ,
    3 : "DOWNWARD_KICK" ,
    4 : "ROUND_KICK" ,
    5 : "BACK_KICK" ,
    6 : "BACK_ROUND_KICK" ,
    7 : "TURN_ROUND_KICK" ,
}
TAEKWONDO_LABEL = [
            "STANDBY",
            "SIDE_KICK", 
            "FRONT_KICK",
            "DOWNWARD_KICK",
            "ROUND_KICK",
            "BACK_KICK",
            "BACK_ROUND_KICK",
            "TURN_ROUND_KICK",
            "NONE"
            ]

MODEL_TRANSFORMER = 'transformer'
MODEL_LSTM = 'lstm'