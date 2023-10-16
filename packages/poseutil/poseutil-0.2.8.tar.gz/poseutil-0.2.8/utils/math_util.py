import numpy as np
from utils.const import *
from utils.pose_util import Coordinate
from math import sin, cos
import math
from sklearn.decomposition import PCA

def cos_sim(list1, list2, equation=COSINE): 
    x_val = math.acos(np.dot(list1, list2) / (np.linalg.norm(list1) * np.linalg.norm(list2)))
    if equation == COSINE:
        y_val = math.cos(x_val)
    elif equation == LINEAR:
        y_val = (-2 * x_val / math.pi) + 1
    elif equation == PARABOLA:
        if x_val > math.pi / 2:
            y_val = -1
        else:
            y_val = (x_val - math.pi / 2) ** 2 * 4 / (math.pi ** 2)
    return max(0, round(y_val * 100, 2))

def cos_sim_list(list1, list2, equation=COSINE):
    result = []
    for i in range(len(list1)):
        result.append(cos_sim(list1[i], list2[i]))
    return result

def get_cos_sim_score(data_a, data_b, iter=DANCE_TARGET_BODY, dimension="xyz", time_line=0):
    score_list = []
    for k, v in iter:
        if data_a[k].visibility < 0.8 or data_a[v].visibility < 0.8 and data_b[k].visibility < 0.8 or data_b[v].visibility < 0.8:
            continue
        vector_a = np.array([data_a[k].x - data_a[v].x, data_a[k].y - data_a[v].y, data_a[k].z*0.3 - data_a[v].z*0.3])
        vector_b = np.array([data_b[k].x - data_b[v].x, data_b[k].y - data_b[v].y, data_b[k].z*0.3 - data_b[v].z*0.3])
        if not vector_a.all() or not vector_b.all():
            score_list.append(0)
        elif dimension == "xyz":
            score_list.append(cos_sim(vector_a, vector_b))
        else:
            score_list.append(cos_sim(vector_a[:-1], vector_b[:-1]))
    if len(score_list) == 0:
        return [100]
    return score_list

def get_cos_score_list_for_weight(trainerPose, userPose, equation=COSINE, body_target=SYNC_TARGET_LOWER):
    score_list = []
    for k, v in body_target:
        if trainerPose[k].visibility < 0.8 or trainerPose[v].visibility < 0.8:
            score_list.append(100)
            continue
        elif userPose[k].visibility < 0.8 or userPose[v].visibility < 0.8:
            score_list.append(0)
            continue
        vector_a = np.array([trainerPose[k].x - trainerPose[v].x, trainerPose[k].y - trainerPose[v].y, trainerPose[k].z * 0.3 - trainerPose[v].z * 0.3])
        vector_b = np.array([userPose[k].x - userPose[v].x, userPose[k].y - userPose[v].y, userPose[k].z * 0.3 - userPose[v].z * 0.3])
        score_list.append(cos_sim(vector_a, vector_b, equation))
    return score_list

def get_cos_score_list_for_dance(dancerPose, dancerHands, userPose, userHands, weights, equation=COSINE, body_target=DANCE_TARGET_BODY, hand_target=DANCE_TARGET_HAND):
    score_list = []
    weights_copy = weights[:]
    for idx, (k, v) in enumerate(body_target):
        if dancerPose[k].visibility < 0.8 or dancerPose[v].visibility < 0.8:
            score_list.append(100)
            weights_copy[idx] = 0
            continue
        elif userPose[k].visibility < 0.8 or userPose[v].visibility < 0.8:
            score_list.append(0)
            continue
        vector_a = np.array([dancerPose[k].x - dancerPose[v].x, dancerPose[k].y - dancerPose[v].y, dancerPose[k].z * 0.3 - dancerPose[v].z * 0.3])
        vector_b = np.array([userPose[k].x - userPose[v].x, userPose[k].y - userPose[v].y, userPose[k].z * 0.3 - userPose[v].z * 0.3])
        score_list.append(cos_sim(vector_a, vector_b, equation))
    
    hand_score_list = []
    for dancerHand, userHand in zip(dancerHands, userHands):
        for k, v in hand_target:
            if type(dancerHand[k].visibility) == int or type(dancerHand[v].visibility) == int:
                hand_score_list.append(100)
                continue
            elif type(userHand[k].visibility) == int or type(userHand[k].visibility) == int:
                hand_score_list.append(0)
                continue
            vector_a = np.array([dancerHand[k].x - dancerHand[v].x, dancerHand[k].y - dancerHand[v].y, dancerHand[k].z * 0.3 - dancerHand[v].z * 0.3])
            vector_b = np.array([userHand[k].x - userHand[v].x, userHand[k].y - userHand[v].y, userHand[k].z * 0.3 - userHand[v].z * 0.3])
            hand_score_list.append(cos_sim(vector_a, vector_b, equation))

    score_list.append(sum(hand_score_list) / len(hand_score_list))
    cosScore = sum([weight * score for weight, score in zip(weights_copy, score_list)]) / sum(weights_copy)
    return cosScore, score_list

def cosine_similarity(v1,v2):
    v1 = np.array(list(map(float, v1)))
    v2 = np.array(list(map(float, v2)))
    return np.dot(v1, v2) / (np.linalg.norm(v2) * np.linalg.norm(v1))
#------------------------------------------------------------------------

def get_distance(list1, list2):
    return math.sqrt((list1.x - list2.x) ** 2 + (list1.y - list2.y) ** 2)

def recommend_vector(coord, distance, slope, direction):
    result = math.sqrt((distance ** 2) / (slope ** 2  + 1))
    if direction:
        x, y = coord.x + result, coord.y + (result * slope)
    else:
        x, y = coord.x - result, coord.y - (result * slope)
    return x, y

#------------------------------------------------------------------------
# eigen
def getEigen(datas):
    X = np.array(datas)
    pca = PCA(n_components=1)
    X_low = pca.fit_transform(X)
    X2 = pca.inverse_transform(X_low)
    return pca.components_[0], pca.explained_variance_[0] * 1e6

def dist(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def getCos(input):
    a = dist([0, -1])
    b = dist([input[0], input[1]])
    ip = -input[1]
    ip2 = a * b
    cost = ip / ip2
    x = math.acos(cost)
    X = math.degrees(x)
    g = (9.81 * (-(cost-1)))/2

#------------------------------------------------------------------------

# coordinate rotate
def get_rotate(body, x_center, y_center, x_degree, y_degree):
    
    center_x = body.x - x_center
    center_y = body.y
    center_z = body.z

    rotate_x_x = center_x * cos(x_degree) + center_z * sin(x_degree)
    rotate_x_y = center_y
    rotate_x_z = center_z * cos(x_degree) - center_x * sin(x_degree)

    center_x = rotate_x_x + x_center
    center_y = rotate_x_y - y_center
    center_z = rotate_x_z

    rotate_y_x = center_x
    rotate_y_y = center_y * cos(y_degree) - center_z * sin(y_degree)
    rotate_y_z = center_y * sin(y_degree) + center_z * cos(y_degree)

    x = rotate_y_x
    y = rotate_y_y + y_center
    z = rotate_y_z

    rotated_body = Coordinate(x, y, z, body.visibility)
    return rotated_body

def get_move_hand_coordinate(hands, move):
    result_hands = []
    for idx, hand in enumerate(hands):
        result_hand = []
        x_margin = move[idx][0] - hand[HAND_WRIST].x
        y_margin = move[idx][1] - hand[HAND_WRIST].y
        for point in hand:
            result_hand.append(Coordinate(point.x + x_margin, point.y + y_margin, point.z, point.visibility))
        result_hands.append(result_hand)
    return result_hands




        
    
        
