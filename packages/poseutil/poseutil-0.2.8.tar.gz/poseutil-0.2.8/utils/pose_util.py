import copy
import math
import numpy as np
import mediapipe as mp
import cv2
from tqdm import tqdm


class data:
    def __init__(self, poseState, successCount, failCount):
        self.poseState = poseState
        self.successCount = successCount
        self.failCount = failCount


class metaData:
    userData = []
    def addData(self, poseState, successCount, failCount):
        self.userData.append(data(poseState=poseState,
                                  successCount=successCount,
                                  failCount=failCount))
    def clear(self):
        self.userData.clear()


class Coordinate:
    def __init__(self, x, y, z, visibility=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility
        self.array = np.array([x, y, z])

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
        
    def get_distance_2d(self, coord):
        return math.sqrt((self.x - coord.x) ** 2 + (self.y - coord.y) ** 2)
    
    def get_distance_3d(self, coord):
        return math.sqrt((self.x - coord.x) ** 2 + (self.y - coord.y) ** 2 + (self.z - coord.z) ** 2)

    def cos_sim(self, coord):
        return round(np.dot(self.array, coord.array) / (np.linalg.norm(self.array) * np.linalg.norm(coord.array)) * 100, 2)
    
    def get_center_coord(self, coord):
        x = (self.x + coord.x) / 2
        y = (self.x + coord.y) / 2
        z = (self.z + coord.z) / 2
        return Coordinate(x, y, z)


class position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __int__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class CustomPoseData:
    poseLandmarksDataFrame = []
    poseLandmarks = []
    poseLandmark = []

    def setzerosLandmark(self):
        if len(self.poseLandmark) > 33:
            self.poseLandmark.clear()
        for i in range(33):
            self.poseLandmark.append(position(0.0, 0.0, 0.0))

    def addLandmark(self, lm):
        self.poseLandmarks.append(position(lm.x, lm.y, lm.z))

    def addDataFrame(self):
        frameData = copy.deepcopy(self.poseLandmarks)
        self.poseLandmarksDataFrame.append(frameData)

    def clear(self):
        self.poseLandmark.clear()
        self.poseLandmarks.clear()


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_pose_data(img):
    img.flags.writeable = False
    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img.flags.writeable = True
    mp_drawing.draw_landmarks(
        img,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style()
    )
    height, width, _ = img.shape
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        pose_landmark = [Coordinate(landmark.x * width, landmark.y * height, landmark.z * (width + height) * 0.1, landmark.visibility) for landmark in landmarks]
    else:
        pose_landmark = [Coordinate(0, 0, 0, 0) for _ in range(33)]

    return pose_landmark

def get_holistic_data(img):
    img.flags.writeable = False
    results = holistic.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img.flags.writeable = True
    mp_drawing.draw_landmarks(
        img,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style()
    )
    
    mp_drawing.draw_landmarks(
        img,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style()
    )
    
    mp_drawing.draw_landmarks(
        img,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

    mp_drawing.draw_landmarks(
        img,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        pose_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        pose_landmark = [Coordinate(0, 0, 0, 0) for _ in range(33)]

    if results.face_landmarks:
        landmarks = results.face_landmarks.landmark
        face_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        face_landmark = [Coordinate(0, 0, 0, 0) for _ in range(468)]

    if results.left_hand_landmarks:
        landmarks = results.left_hand_landmarks.landmark
        left_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        left_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    if results.right_hand_landmarks:
        landmarks = results.right_hand_landmarks.landmark
        right_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        right_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    return pose_landmark, face_landmark, left_hand_landmark, right_hand_landmark

def get_user_coordinate(results):
    user_coordinate = []
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        pose_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        pose_landmark = [Coordinate(0, 0, 0, 0) for _ in range(33)]

    if results.left_hand_landmarks:
        landmarks = results.left_hand_landmarks.landmark
        left_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        left_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    if results.right_hand_landmarks:
        landmarks = results.right_hand_landmarks.landmark
        right_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        right_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    return pose_landmark, [left_hand_landmark, right_hand_landmark]

def convert_pose(poses, width, height):
    pose_data = []
    zWeight = (width + height) * 0.1
    for pose in poses:
        pose_data.append([Coordinate(i.x * width, i.y * height, i.z * zWeight) for i in pose])
    return pose_data

def sync_pose(poses, width, height, target_width, target_height):
    pose_data = []
    zWeight = (width + height) * 0.1
    target_zWeight = (target_width + target_height) * 0.1
    for pose in poses:
        pose_data.append([Coordinate(i.x / width * target_width, i.y / height * target_height, i.z / zWeight * target_zWeight) for i in pose])
    return pose_data
            
    
def get_video_to_pickle_data(args):
    frame_num = 0
    time_list = []
    pose_list = []
    face_list = []
    left_hand_list = []
    right_hand_list = []
    cap = cv2.VideoCapture(args.videoPath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=length * 2 if args.hflip else length)
    while True:
        ret, img = cap.read()
        if args.vflip:
            img = cv2.flip(img, 0)
        if not cap.isOpened() or not ret:
            break
        height, width, _ = img.shape
        
        time_ms = round(cap.get(cv2.CAP_PROP_POS_MSEC))
        time_list.append(time_ms)
        pose_landmark, face_landmark, left_hand_landmark, right_hand_landmark = get_holistic_data(img)
        pose_list.append(pose_landmark)
        face_list.append(face_landmark)
        left_hand_list.append(left_hand_landmark)
        right_hand_list.append(right_hand_landmark)
        pbar.update(1)
        cv2.imshow("viewImg", img)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.destroyAllWindows()
    pose_list = convert_pose(pose_list, width, height)
    status = [None for i in range(len(pose_list))]
    reps = [None for i in range(len(pose_list))]
    pickle_data = {
            "time": time_list, 
            "status": status,
            "reps": reps,
            "width": width,
            "height": height,
            "pose": pose_list
        }
    return pickle_data