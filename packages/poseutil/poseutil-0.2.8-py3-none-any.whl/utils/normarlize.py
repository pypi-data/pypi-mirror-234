import math
import pickle, gzip

from utils.pose_util import *
from utils.const import *
import utils.csvHelper as csvHelper
from utils.const import *

STEP_1 = 'up'
STEP_2 = 'down'

LEFT = "LEFT"
RIGHT = "RIGHT"


def preProcessing(filePath, exerciseType):
    labeling = csvHelper.readCSV(filePath)
    result = []
    for row in labeling:
        embedding = getPoseEmbedding(row[1:], exerciseType)
        roundEmbedding = roundRow(embedding)
        roundEmbedding.insert(0, row[0])
        result.append(roundEmbedding)

    convertPath = filePath.replace("_exerciseState", "").replace(".csv", "")
    if "LEFT" in exerciseType:
        convertPath += "L.csv"
    elif "RIGHT" in exerciseType:
        convertPath += "R.csv"
    else:
        convertPath += ".csv"
    csvHelper.writeCSV(convertPath, result)

def preProcessingNew(exercise, filePath, exerciseType, sideViserblity):
    with gzip.open(filePath, "rb") as f:
        pickle_data = pickle.load(f)
    labels = pickle_data["knn_label"]
    poses = pickle_data["pose"]
    all = embeddingConvert(labels, poses, exerciseType)
    if sideViserblity == LEFT:
        left = embeddingConvert(labels, poses, exerciseType + LEFT)
        right = embeddingConvert(labels, poses, exerciseType + RIGHT)
        print(f'sideViserblity : {sideViserblity}, copy left')
    elif sideViserblity == RIGHT:
        left = embeddingConvert(labels, poses, exerciseType + LEFT)
        right = embeddingConvert(labels, poses, exerciseType + RIGHT)
        print(f'sideViserblity : {sideViserblity}, copy right')
    else:
        left = embeddingConvert(labels, poses, exerciseType + LEFT)
        right = embeddingConvert(labels, poses, exerciseType + RIGHT)
        print(f'sideViserblity : {sideViserblity}')

    
    savePath = f"{KNN_PATH}/{exercise}/{exerciseType}/{exercise}"
    createFile(all, savePath, ".csv")
    createFile(left, savePath, 'L.csv')
    createFile(right, savePath, 'R.csv')
    createFile(left+right, savePath, 'Side.csv')


def embeddingConvert(labels, poses, exerciseType):
    result = []
    for label, pose in zip(labels, poses):
        embedding = getPoseEmbedding(pose, exerciseType)
        roundEmbedding = roundRow(embedding)
        roundEmbedding.insert(0, label)
        result.append(roundEmbedding)
    return result

def createFile(data, convertPath, exerciseTypeDetail):
    convertPath += exerciseTypeDetail
    csvHelper.writeCSV(convertPath, data)

def roundRow(row):
    result = []
    for cell in row:
        result.append(Coordinate(round(cell.x, 3), round(cell.y, 3), round(cell.z, 3)))
    return result


def getPoseEmbedding(landmarks, exerciseType):
    normalizedLandmarks = normalize(landmarks)
    return getEmbedding(normalizedLandmarks, exerciseType)

def getPoseEmbeddingList(landmarks, exerciseType):
    embeddings = getPoseEmbedding(landmarks, exerciseType)
    result = []
    for embedding in embeddings:
        result.append(embedding.x)
        result.append(embedding.y)
        result.append(embedding.z)
    return result


def subtract(b, a):
    return Coordinate(a.x - b.x, a.y - b.y, a.z - b.z)


def multiply(a, multiple):
    return Coordinate(a.x * multiple, a.y * multiple, a.z * multiple)


def subtractAll(p, pointsList):
    result = []
    for data in pointsList:
        result.append(subtract(p, data))
    return result


def multiplyAll(pointsList, multiple):
    result = []
    for data in pointsList:
        result.append((multiply(data, multiple)))
    return result


def normalize(landmarks):
    normalizedLandmarks = landmarks.copy()
    center = average(landmarks[LEFT_HIP], landmarks[RIGHT_HIP])
    normalizedLandmarks = subtractAll(center, normalizedLandmarks)
    normalizedLandmarks = multiplyAll(normalizedLandmarks, (1 / getPoseSize(normalizedLandmarks)))
    normalizedLandmarks = multiplyAll(normalizedLandmarks, 100)
    return normalizedLandmarks

def move_center(landmarks, center):
    copy_landmarks = landmarks.copy()
    center = landmarks[center]
    move_landmarks = subtractAll(center, copy_landmarks)
    return move_landmarks

def normalize_target(landmarks, center_target):
    normalizedLandmarks = landmarks.copy()
    center = landmarks[center_target]
    normalizedLandmarks = subtractAll(center, normalizedLandmarks)
    normalizedLandmarks = multiplyAll(normalizedLandmarks, (1 / getPoseSize(normalizedLandmarks)))
    normalizedLandmarks = multiplyAll(normalizedLandmarks, 100)
    return normalizedLandmarks

def average(a, b):
    return Coordinate((a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2)


def l2Norm2D(point):
    return math.hypot(point.x, point.y)


def subtract(a, b):
    return Coordinate(a.x - b.x, a.y - b.y, a.z - b.z)


def getPoseSize(landmarks):
    hipsCenter = average(landmarks[LEFT_HIP], landmarks[RIGHT_HIP])
    shouldersCenter = average(landmarks[LEFT_SHOULDER], landmarks[RIGHT_SHOULDER])

    torsoSize = l2Norm2D(subtract(hipsCenter, shouldersCenter))

    maxDistance = torsoSize * TORSO_MULTIPLIER
    for landmark in landmarks:
        distance = l2Norm2D(subtract(hipsCenter, landmark))
        if distance > maxDistance:
            maxDistance = distance
    return maxDistance


def getEmbedding(lm, exerciseType):
    if exerciseType == FULL:
        embedding = [subtract(average(lm[LEFT_HIP], lm[RIGHT_HIP]), average(lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER])),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ELBOW]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ELBOW]), 
                     subtract(lm[LEFT_ELBOW], lm[LEFT_WRIST]), subtract(lm[RIGHT_ELBOW], lm[RIGHT_WRIST]), 
                     subtract(lm[LEFT_HIP], lm[LEFT_KNEE]), subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]), 
                     subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]), subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]), 
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_WRIST]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_WRIST]), 
                     subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]), subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]), subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]), 
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]), subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]), 
                     subtract(lm[LEFT_ELBOW], lm[RIGHT_ELBOW]),
                     subtract(lm[LEFT_KNEE], lm[RIGHT_KNEE]), 
                     subtract(lm[LEFT_WRIST], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_ANKLE], lm[RIGHT_ANKLE])]
    elif exerciseType == BODYNOSE:
        embedding = [subtract(average(lm[LEFT_HIP], lm[RIGHT_HIP]),average(lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER])),
                    subtract(average(lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER]), lm[NOSE]),
                    subtract(lm[NOSE], lm[LEFT_SHOULDER]), subtract(lm[NOSE], lm[RIGHT_SHOULDER]),
                    subtract(lm[NOSE], lm[LEFT_HIP]), subtract(lm[NOSE], lm[RIGHT_HIP]),
                    subtract(lm[LEFT_SHOULDER], lm[LEFT_HIP]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_HIP]),
                    subtract(lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER]), subtract(lm[LEFT_HIP], lm[RIGHT_HIP]),
                    subtract(lm[LEFT_SHOULDER, RIGHT_HIP]), subtract(lm[RIGHT_SHOULDER, LEFT_HIP])]

    elif exerciseType == BODYNOSELEFT:
        embedding = [subtract(lm[LEFT_HIP], lm[LEFT_SHOULDER]),
                    subtract(lm[NOSE], lm[LEFT_SHOULDER]),
                    subtract(lm[NOSE], lm[LEFT_HIP])]
    elif exerciseType == BODYNOSERIGHT:
        embedding = [subtract(lm[RIGHT_HIP], lm[RIGHT_SHOULDER]),
                    subtract(lm[NOSE], lm[RIGHT_SHOULDER]),
                    subtract(lm[NOSE], lm[RIGHT_HIP])]
    elif exerciseType == UPPER:
        embedding = [subtract(average(lm[LEFT_HIP], lm[RIGHT_HIP]),average(lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER])),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ELBOW]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ELBOW]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_WRIST]), subtract(lm[RIGHT_SHOULDER], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_ELBOW], lm[LEFT_WRIST]), subtract(lm[RIGHT_ELBOW], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]), subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_ELBOW]), subtract(lm[RIGHT_HIP], lm[RIGHT_ELBOW]),
                     subtract(lm[LEFT_PINKY], lm[RIGHT_PINKY]), subtract(lm[LEFT_ELBOW], lm[RIGHT_ELBOW]),
                     subtract(lm[LEFT_WRIST], lm[RIGHT_WRIST]), 
                     subtract(lm[LEFT_PINKY], lm[RIGHT_PINKY]),
                     subtract(lm[LEFT_ELBOW], lm[RIGHT_ELBOW]), 
                     subtract(lm[LEFT_WRIST], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_ELBOW], lm[RIGHT_WRIST]),
                     subtract(lm[LEFT_WRIST], lm[RIGHT_ELBOW]),
                     subtract(lm[LEFT_SHOULDER], lm[RIGHT_WRIST]), 
                     subtract(lm[RIGHT_SHOULDER], lm[LEFT_WRIST])]
    elif exerciseType == LOWER:
        embedding = [
            subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]),
            subtract(lm[LEFT_KNEE], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_FOOT_INDEX]),
            subtract(lm[LEFT_KNEE], lm[LEFT_HEEL]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_HEEL]),
            subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
            subtract(lm[LEFT_SHOULDER], lm[LEFT_KNEE]), 
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_KNEE]),
            subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
            subtract(lm[LEFT_HIP], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_FOOT_INDEX]), 
            subtract(lm[LEFT_HIP], lm[LEFT_HEEL]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_HEEL]), 
            subtract(lm[LEFT_HIP], lm[LEFT_KNEE]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]),
            subtract(lm[LEFT_KNEE], lm[RIGHT_KNEE]), 
            subtract(lm[LEFT_ANKLE], lm[RIGHT_ANKLE])]
    elif exerciseType == FULLLEFT:
        embedding = [subtract(lm[LEFT_HIP], lm[LEFT_SHOULDER]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ELBOW]),
                     subtract(lm[LEFT_ELBOW], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_KNEE]),
                     subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]),
                    ]
    elif exerciseType == FULLRIGHT:
        embedding = [subtract(lm[RIGHT_HIP], lm[RIGHT_SHOULDER]),
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ELBOW]), 
                     subtract(lm[RIGHT_ELBOW], lm[RIGHT_WRIST]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]), 
                     subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]), 
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_WRIST]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]), 
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
                     subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]), 
                     ]
    elif exerciseType == UPPERLEFT:
        embedding = [subtract(lm[LEFT_HIP], lm[LEFT_SHOULDER]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ELBOW]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_ELBOW], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_WRIST]),
                     subtract(lm[LEFT_HIP], lm[LEFT_ELBOW]),
                     ]
    elif exerciseType == UPPERRIGHT:
        embedding = [subtract(lm[RIGHT_HIP], lm[RIGHT_SHOULDER]),
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ELBOW]),
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_WRIST]),
                     subtract(lm[RIGHT_ELBOW], lm[RIGHT_WRIST]),
                     subtract(lm[RIGHT_HIP], lm[RIGHT_WRIST]),
                     subtract(lm[RIGHT_HIP], lm[RIGHT_ELBOW]),
                     ]
    
    elif exerciseType == LOWERLEFT:
        embedding = [subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_KNEE], lm[LEFT_FOOT_INDEX]),
                     subtract(lm[LEFT_KNEE], lm[LEFT_HEEL]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_SHOULDER], lm[LEFT_KNEE]),
                     subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]),
                     subtract(lm[LEFT_HIP], lm[LEFT_FOOT_INDEX]),
                     subtract(lm[LEFT_HIP], lm[LEFT_HEEL]),
                     subtract(lm[LEFT_HIP], lm[LEFT_KNEE]), 
                     ]
    elif exerciseType == LOWERRIGHT:
        embedding = [subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]),
                     subtract(lm[RIGHT_KNEE], lm[RIGHT_FOOT_INDEX]),
                     subtract(lm[RIGHT_KNEE], lm[RIGHT_HEEL]),
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
                     subtract(lm[RIGHT_SHOULDER], lm[RIGHT_KNEE]),
                     subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_FOOT_INDEX]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_HEEL]), 
                     subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]), 
                     ]
    elif exerciseType == HAND:
        embedding = [subtract(lm[LEFT_WRIST], lm[LEFT_PINKY]), subtract(lm[LEFT_WRIST], lm[LEFT_INDEX]),
                     subtract(lm[LEFT_WRIST], lm[LEFT_ELBOW]), subtract(lm[LEFT_ELBOW], lm[LEFT_PINKY]),
                     subtract(lm[LEFT_ELBOW], lm[LEFT_THUMB]), subtract(lm[RIGHT_WRIST], lm[RIGHT_PINKY]),
                     subtract(lm[RIGHT_WRIST], lm[RIGHT_INDEX]), subtract(lm[RIGHT_WRIST], lm[RIGHT_ELBOW]),
                     subtract(lm[RIGHT_ELBOW], lm[RIGHT_PINKY]), subtract(lm[RIGHT_ELBOW], lm[RIGHT_THUMB])]
    elif exerciseType == HANDLEFT:
        embedding = [subtract(lm[LEFT_WRIST], lm[LEFT_PINKY]), subtract(lm[LEFT_WRIST], lm[LEFT_INDEX]),
                     subtract(lm[LEFT_WRIST], lm[LEFT_ELBOW]), subtract(lm[LEFT_ELBOW], lm[LEFT_PINKY]),
                     subtract(lm[LEFT_ELBOW], lm[LEFT_THUMB]),]
    elif exerciseType == HANDRIGHT:
        embedding = [subtract(lm[RIGHT_WRIST], lm[RIGHT_PINKY]),
                     subtract(lm[RIGHT_WRIST], lm[RIGHT_INDEX]), subtract(lm[RIGHT_WRIST], lm[RIGHT_ELBOW]),
                     subtract(lm[RIGHT_ELBOW], lm[RIGHT_PINKY]), subtract(lm[RIGHT_ELBOW], lm[RIGHT_THUMB])]
    elif exerciseType == LOWERYANG:
        embedding = [
            subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]),
            subtract(lm[LEFT_KNEE], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_FOOT_INDEX]),
            subtract(lm[LEFT_KNEE], lm[LEFT_HEEL]), 
            subtract(lm[RIGHT_KNEE], lm[RIGHT_HEEL]),
            subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
            subtract(lm[LEFT_SHOULDER], lm[LEFT_KNEE]), 
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_KNEE]),
            subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
            subtract(lm[LEFT_HIP], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_FOOT_INDEX]), 
            subtract(lm[LEFT_HIP], lm[LEFT_HEEL]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_HEEL]), 
            subtract(lm[LEFT_HIP], lm[LEFT_KNEE]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]),
            subtract(lm[LEFT_KNEE], lm[RIGHT_KNEE]), 
            subtract(lm[LEFT_ANKLE], lm[RIGHT_ANKLE]),
            subtract(lm[LEFT_ANKLE], lm[LEFT_FOOT_INDEX]),
            subtract(lm[LEFT_ANKLE], lm[LEFT_HEEL]),
            subtract(lm[LEFT_FOOT_INDEX], lm[LEFT_HEEL]),
            subtract(lm[RIGHT_ANKLE], lm[RIGHT_FOOT_INDEX]),
            subtract(lm[RIGHT_ANKLE], lm[RIGHT_HEEL]),
            subtract(lm[RIGHT_FOOT_INDEX], lm[RIGHT_HEEL])]
    elif exerciseType == LOWERYANGLEFT:
         embedding = [
            subtract(lm[LEFT_KNEE], lm[LEFT_ANKLE]), 
            subtract(lm[LEFT_KNEE], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[LEFT_KNEE], lm[LEFT_HEEL]), 
            subtract(lm[LEFT_SHOULDER], lm[LEFT_ANKLE]), 
            subtract(lm[LEFT_SHOULDER], lm[LEFT_KNEE]), 
            subtract(lm[LEFT_HIP], lm[LEFT_ANKLE]), 
            subtract(lm[LEFT_HIP], lm[LEFT_FOOT_INDEX]), 
            subtract(lm[LEFT_HIP], lm[LEFT_HEEL]), 
            subtract(lm[LEFT_HIP], lm[LEFT_KNEE]),  
            subtract(lm[LEFT_ANKLE], lm[LEFT_FOOT_INDEX]),
            subtract(lm[LEFT_ANKLE], lm[LEFT_HEEL]),
            subtract(lm[LEFT_FOOT_INDEX], lm[LEFT_HEEL]),
        ]

    elif exerciseType == LOWERYANGRIGHT:
         embedding = [
            subtract(lm[RIGHT_KNEE], lm[RIGHT_ANKLE]),
            subtract(lm[RIGHT_KNEE], lm[RIGHT_FOOT_INDEX]),
            subtract(lm[RIGHT_KNEE], lm[RIGHT_HEEL]),
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_ANKLE]),
            subtract(lm[RIGHT_SHOULDER], lm[RIGHT_KNEE]),
            subtract(lm[RIGHT_HIP], lm[RIGHT_ANKLE]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_FOOT_INDEX]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_HEEL]), 
            subtract(lm[RIGHT_HIP], lm[RIGHT_KNEE]),
            subtract(lm[RIGHT_ANKLE], lm[RIGHT_FOOT_INDEX]),
            subtract(lm[RIGHT_ANKLE], lm[RIGHT_HEEL]),
            subtract(lm[RIGHT_FOOT_INDEX], lm[RIGHT_HEEL])]
    return embedding
