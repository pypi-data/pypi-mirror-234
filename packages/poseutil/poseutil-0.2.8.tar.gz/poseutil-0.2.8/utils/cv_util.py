import cv2
import numpy as np
from utils.const import *
from utils.math_util import get_rotate, get_move_hand_coordinate

#cv component
def draw_landmarks(image, origin_poses, origin_hands, width, height, x_degree=0, y_degree=0):
    poses = []
    x_center = (origin_poses[LEFT_HIP].x + origin_poses[RIGHT_HIP].x)/2
    y_center = (origin_poses[LEFT_HIP].y + origin_poses[RIGHT_HIP].y)/2
    for body in origin_poses:
        poses.append(get_rotate(body, x_center, y_center, x_degree, y_degree))

    hands = []
    for hand in origin_hands:
        result = []
        x_center = hand[HAND_WRIST].x
        y_center = hand[HAND_WRIST].y
        for point in hand:
            result.append(get_rotate(point, x_center, y_center, x_degree, y_degree))
        hands.append(result)

    move = [[poses[LEFT_WRIST].x, poses[LEFT_WRIST].y], [poses[RIGHT_WRIST].x, poses[RIGHT_WRIST].y]]
    hands = get_move_hand_coordinate(hands, move)
    

    try:
        if poses[11].z < poses[12].z:
            for k, v in RIGHT_LINK:
                cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), (0, 255, 0), 4)
            for k, v in LEFT_LINK:
                cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), (255, 0, 0), 4)
        else:
            for k, v in LEFT_LINK:
                cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), (255, 0, 0), 4)
            for k, v in RIGHT_LINK:
                cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), (0, 255, 0), 4)

        
        for k, v in CENTER_LINK:
            cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), (255, 255, 255), 4)
        for k in BODY_DOT:
            cv2.circle(image, list(map(int, (poses[k].x * width, poses[k].y * height))), 4, (0, 0, 255), -1)
        
        for hand in hands:
            for k, v in HAND:
                cv2.line(image, list(map(int, (hand[k].x * width, hand[k].y * height))), list(map(int, (hand[v].x * width, hand[v].y * height))), (0, 255, 255), 4)
            for k in HAND_DOT:
                cv2.circle(image, list(map(int, (hand[k].x * width, hand[k].y * height))), 4, (0, 0, 255), -1)
    except Exception as e:
        print(e)
        pass

def draw_landmarks_with_cos(image, poses, hands, score_list, cutline, width, height, target=DANCE_TARGET_BODY):
    score_list = np.array(score_list)
    low_score_idx = np.where(score_list[:-1] < cutline)[0]
    error_target = [target[i] for i in low_score_idx]
    for k, v in LEFT_LINK + RIGHT_LINK + CENTER_LINK:
        color = (0, 0, 255) if [k, v] in error_target or [v, k] in error_target else (255, 255, 255)
        cv2.line(image, list(map(int, (poses[k].x * width, poses[k].y * height))), list(map(int, (poses[v].x * width, poses[v].y * height))), color, 10)
    for k in BODY_DOT:
        cv2.circle(image, list(map(int, (poses[k].x * width, poses[k].y * height))), 4, (0, 0, 0), -1)

    hand_color = (0, 0, 255) if score_list[-1] < cutline else (255, 255, 255)
    for hand in hands:
        for k, v in HAND:
            cv2.line(image, list(map(int, (hand[k].x * width, hand[k].y * height))), list(map(int, (hand[v].x * width, hand[v].y * height))), hand_color, 10)
        for k in HAND_DOT:
            cv2.circle(image, list(map(int, (hand[k].x * width, hand[k].y * height))), 6, (0, 0, 255), -1)


def draw_text(img, text, pos, color, scale=2):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, 3, cv2.LINE_AA)

def draw_progressbar(frame, progress):
    ptLeftTop = (0, 0)
    ptRightBottom = (progress, 8)
    point_color = (173, 119, 137) 
    thickness = 8
    lineType = 8
    result = cv2.rectangle(frame, ptLeftTop, ptRightBottom, point_color, thickness, lineType)
    return result

def draw_score_progressbar(frame, score):
    img_shape = frame.shape
    if score > 80:
        color = BGR_GREEN
    elif score > 60:
        color = BGR_YELLOW
    else:
        color = BGR_RED
    ratio = 0.1
    pt_start = (int(img_shape[0]*ratio), int(img_shape[0]*(1-ratio)))
    pt_end = (int(img_shape[0]*ratio), int(img_shape[0]*(1-ratio) - img_shape[0]*(0.9-ratio)*(score/100)))
    thickness = 30
    lineType = 8
    result = cv2.rectangle(frame, pt_start, pt_end, color, thickness, lineType)
    return result

def add_infomation_circle(img, text):
    mask = img.copy()
    cv2.circle(mask, (150,150), 150, (0, 0, 0), -1)
    cv2.putText(mask, text, (60, 220), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 255), 5)
    return cv2.addWeighted(img, 0.3, mask, 0.7, 0)

def get_pause_view(text, img_shape):
    margin = 100
    center = (int(img_shape[1]/2), int(img_shape[0]/2))
    radius = int(img_shape[0]/2)
    count_center = (int(center[0]), int(center[1]))
    view = np.zeros((img_shape[0], img_shape[1], 3), np.uint8)
    cv2.circle(view, center, radius, (0, 0, 0), -1)
    cv2.putText(view, text, count_center, cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 255), 5)
    cv2.putText(view, "READY", (margin, img_shape[0]-margin), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 255), 5)
    return view

def get_score_view(score, img_shape):
    score = round(score)
    margin = 100
    view = np.zeros((img_shape[0], img_shape[1], 3), np.uint8)
    center = (margin, int(img_shape[0]/2))
    if score > 80:
        text = f"Score : {score} Congratulations"
    else:
        text = f"Score : {score} T T Try Again"
    cv2.putText(view, "Score View", (margin, margin), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)
    cv2.putText(view, text, center, cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)
    cv2.putText(view, "Plase Press Enter", (margin, img_shape[0]-margin), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)

    return view

def get_end_view(text, img_shape):
    margin = (int(img_shape[0]/100), int(img_shape[1]/2))
    view = np.zeros((img_shape[0], img_shape[1], 3), np.uint8)
    cv2.putText(view, text, margin, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    return view

def draw_lstm_input(poses):
    cols = len(poses) // 2
    first_row = np.zeros((0, 0, 0))
    second_row = np.zeros((0, 0, 0))
    idx = 0
    for i in range(2):
        for j in range(cols):
            image = np.zeros((640, 480, 3), dtype=np.uint8)
            draw_landmarks(image, poses[idx], [], 1, 1)
            if i == 0:
                if j == 0:
                    first_row = image
                else:
                    first_row = cv2.hconcat([first_row, image])
            else:
                if j == 0:
                    second_row = image
                else:
                    second_row = cv2.hconcat([second_row, image])
            idx += 1
    view_image = cv2.vconcat([first_row, second_row])
    return view_image
            




#------------------------------------------------------------------------
