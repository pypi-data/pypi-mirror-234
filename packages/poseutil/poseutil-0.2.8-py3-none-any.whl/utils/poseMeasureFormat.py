import re

  

"""

여기 변경사항은 테스트 후, poseutil/utils/poseMeasureFormat.py에 반영한 다음에 영재님께 말씀드릴 것!!!!

"""

  

def writeKt(fun_body, path):
    with open(path, 'w') as file:
        file.write(PoseMeasure())
        for i in fun_body:
            file.write(i)
        

def writePy(fun_body, path):
    with open(path, 'a') as file:
        for i in fun_body:
            file.write(i)


def PoseMeasure():
    fun_body = '''\
import math
from utils.const import *
from utils.pose_util import Coordinate


class PoseMeasure:
    def __init__(self, pose):
        self.pose = pose
        self.leftNose = pose[NOSE]
        self.rightNose = pose[NOSE]
        self.leftEyeInner = pose[LEFT_EYE_INNER]
        self.leftEye = pose[LEFT_EYE]
        self.leftEyeOuter = pose[LEFT_EYE_OUTER]
        self.rightEyeInner = pose[RIGHT_EYE_INNER]
        self.rightEye = pose[RIGHT_EYE]
        self.rightEyeOuter = pose[RIGHT_EYE_OUTER]
        self.leftEar = pose[LEFT_EAR]
        self.rightEar = pose[RIGHT_EAR]
        self.leftMouth = pose[LEFT_MOUTH]
        self.rightMouth = pose[RIGHT_MOUTH]
        self.leftShoulder = pose[LEFT_SHOULDER]
        self.rightShoulder = pose[RIGHT_SHOULDER]
        self.leftElbow = pose[LEFT_ELBOW]
        self.rightElbow = pose[RIGHT_ELBOW]
        self.leftWrist = pose[LEFT_WRIST]
        self.rightWrist = pose[RIGHT_WRIST]
        self.leftPinky = pose[LEFT_PINKY]
        self.rightPinky = pose[RIGHT_PINKY]
        self.leftIndex = pose[LEFT_INDEX]
        self.rightIndex = pose[RIGHT_INDEX]
        self.leftThumb = pose[LEFT_THUMB]
        self.rightThumb = pose[RIGHT_THUMB]
        self.leftHip = pose[LEFT_HIP]
        self.rightHip = pose[RIGHT_HIP]
        self.leftKnee = pose[LEFT_KNEE]
        self.rightKnee = pose[RIGHT_KNEE]
        self.leftAnkle = pose[LEFT_ANKLE]
        self.rightAnkle = pose[RIGHT_ANKLE]
        self.leftHeel = pose[LEFT_HEEL]
        self.rightHeel = pose[RIGHT_HEEL]
        self.leftFootIndex = pose[LEFT_FOOT_INDEX]
        self.rightFootIndex = pose[RIGHT_FOOT_INDEX]

    def getCoord(self, a, dimension):
        if dimension == X:
            return a.x
        elif dimension == Y:
            return a.y
        elif dimension == Z:
            return a.z

    def getDistance(self, a, b, dimension):
        aX = abs(a.x - b.x)
        aY = abs(a.y - b.y)
        aZ = abs(a.z - b.z)
        distance = 0
        if dimension == X:
            distance = aX
        elif dimension == Y:
            distance = aY
        elif dimension == Z:
            distance = aZ
        elif dimension == XY:
            distance = math.sqrt(aX ** 2 + aY ** 2)
        elif dimension == YZ:
            distance = math.sqrt(aY ** 2 + aZ ** 2)
        elif dimension == XZ:
            distance = math.sqrt(aX ** 2 + aZ ** 2)
        else:
            distance = math.sqrt(aX ** 2 + aY ** 2 + aZ ** 2)
        return distance

    def calAngle(self, a, b, c):
        if b == 0 or c == 0:
            return 0
        cosineValue = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        cosineValue = max(-1, cosineValue)
        cosineValue = min(1, cosineValue)
        degree = math.acos(cosineValue)
        return math.degrees(degree)

    def getAngle(self, targetPoint, insidePoint, lastPoint, dimension):
        a = self.getDistance(insidePoint, lastPoint, dimension)
        b = self.getDistance(targetPoint, insidePoint, dimension)
        c = self.getDistance(targetPoint, lastPoint, dimension)
        return self.calAngle(a, b, c)
       
    def getPlane(self, a, b, dimension):
        if dimension == XY:
            distanceA = self.getDistance(a, b, Z)
        elif dimension == YZ:
            distanceA = self.getDistance(a, b, X)
        elif dimension == XZ:
            distanceA = self.getDistance(a, b, Y)
        
        distanceB = self.getDistance(a, b, XYZ)
        distanceC = self.getDistance(a, b, dimension)
        return self.calAngle(distanceA, distanceB, distanceC)
    
    def getLine(self, a, b, dimension, line):
        if line == X:
            if dimension == XY:
                distanceA = self.getDistance(a, b, Y)
            elif dimension == XZ:
                distanceA = self.getDistance(a, b, Z)        
        elif line == Y:
            if dimension == XY:
                distanceA = self.getDistance(a, b, X)
            elif dimension == YZ:
                distanceA = self.getDistance(a, b, Z)
        elif line == Z:
            if dimension == YZ:
                distanceA = self.getDistance(a, b, Y)
            elif dimension == XZ:
                distanceA = self.getDistance(a, b, X)
        distanceB = self.getDistance(a, b, dimension)
        distanceC = self.getDistance(a, b, line)
        return self.calAngle(distanceA, distanceB, distanceC)
        
    def getCenterPoint(self, firstPoint, secondPoint):
        x = (firstPoint.x + secondPoint.x) / 2
        y = (firstPoint.y + secondPoint.y) / 2
        z = (firstPoint.z + secondPoint.z) / 2
        return Coordinate(x, y, z)'''
    
    return fun_body
    


def Point(name, landmark:list, sign, what, dimension, direction, sDimension):

    if dimension != None:
        dimension = f'dimension={dimension}'
    else:
        dimension = 'dimension'
    
    if direction != None:
        direction = f'direction={direction}'
    else:
        direction = 'direction'
    
    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'

    if sign is None:
        fun_body = f'''\
        


    def {name}(self, {dimension}, {direction}):
        left = self.getCoord(self.left{landmark[0]}, dimension)
        right = self.getCoord(self.right{landmark[0]}, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
    else:
        fun_name = "get" + "".join(landmark) + what
        if(sign == 'Minus'):
            sign = '<'
        elif(sign == 'Plus'):
            sign = '>'
        fun_body = f'''\
        


    def {name}(self, {dimension}, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) {sign} self.getCoord(right, sDimension):
            return self.{fun_name}(dimension, LEFT)
        else:
            return self.{fun_name}(dimension, RIGHT)'''
        

    return fun_body


def Distance(name, landmark:list, sign, what, dimension, direction, sDimension):

    if dimension != None:
        dimension = f'dimension={dimension}'
    else:
        dimension = 'dimension'
    
    if direction != None:
        direction = f'direction={direction}'
    else:
        direction = 'direction'
    
    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'

    if sign is None:
        if len(landmark) == 1:
            fun_body = f'''\
    
    
    
    def {name}(self, {dimension}):
        return self.getDistance(self.left{landmark[0]}, self.right{landmark[0]}, dimension)'''
        elif len(landmark) == 2:
            fun_body = f'''\
        


    def {name}(self, {dimension}, {direction}):
        left = self.getDistance(self.left{landmark[0]}, self.left{landmark[1]}, dimension)
        right = self.getDistance(self.right{landmark[0]}, self.right{landmark[1]}, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
    elif sign == 'Center':
        fun_body = f'''\
            
            
            
    def {name}(self, {dimension}):
        return self.getDistance(self.left{landmark[0]}, self.getCenterPoint(self.left{landmark[1]}, self.right{landmark[1]}), dimension)'''
    else:
        fun_name = "get" + "".join(landmark) + what
        if(sign == 'Minus'):
            sign = '<'
        elif(sign == 'Plus'):
            sign = '>'
        fun_body = f'''\
        


    def {name}(self, {dimension}, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) {sign} self.getCoord(right, sDimension):
            return self.{fun_name}(dimension, LEFT)
        else:
            return self.{fun_name}(dimension, RIGHT)'''
        
    return fun_body


def Angle(name, landmark:list, sign, what, dimension, direction, sDimension):

    if dimension != None:
        dimension = f'dimension={dimension}'
    else:
        dimension = 'dimension'
    
    if direction != None:
        direction = f'direction={direction}'
    else:
        direction = 'direction'
    
    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'

    if sign is None:
        if len(landmark) != len(set(landmark)):
            fun_body = f'''\
    
    
    
    def {name}(self, {dimension}, {direction}):
        left = self.getAngle(self.left{landmark[0]}, self.left{landmark[1]}, self.right{landmark[2]}, dimension)
        right = self.getAngle(self.right{landmark[0]}, self.right{landmark[1]}, self.left{landmark[2]}, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
        else:
            fun_body = f'''\
        


    def {name}(self, {dimension}, {direction}):
        left = self.getAngle(self.left{landmark[0]}, self.left{landmark[1]}, self.left{landmark[2]}, dimension)
        right = self.getAngle(self.right{landmark[0]}, self.right{landmark[1]}, self.right{landmark[2]}, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
    else:
        fun_name = "get" + "".join(landmark) + what
        if(sign == 'Minus'):
            sign = '<'
        elif(sign == 'Plus'):
            sign = '>'
        fun_body = f'''\
        


    def {name}(self, {dimension}, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) {sign} self.getCoord(right, sDimension):
            return self.{fun_name}(dimension, LEFT)
        else:
            return self.{fun_name}(dimension, RIGHT)'''
        
    return fun_body
    


def Plane(name, landmark:list, sign, what, dimension, direction, sDimension):

    if dimension != None:
        dimension = f'dimension={dimension}'
    else:
        dimension = 'dimension'
    
    if direction != None:
        direction = f'direction={direction}'
    else:
        direction = 'direction'
    
    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'


    if sign is None:
        if len(landmark) == 1:
            fun_body = f'''\
            


    def {name}(self, {dimension}):
        return self.getPlane(self.left{landmark[0]}, self.right{landmark[0]}, dimension)'''
        elif len(landmark) == 2:
            fun_body = f'''\
            


    def {name}(self, {dimension}, {direction}):
        left = self.getPlane(self.left{landmark[0]}, self.left{landmark[1]}, dimension)
        right = self.getPlane(self.right{landmark[0]}, self.right{landmark[1]}, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
    elif sign == 'Center':
        fun_body = f'''\
    
    
    
    def {name}(self, {dimension}):
        return self.getPlane(self.left{landmark[0]}, self.getCenterPoint(self.left{landmark[1]}, self.right{landmark[1]}), dimension)'''
    else:
        fun_name = "get" + "".join(landmark) + what
        if(sign == 'Minus'):
            sign = '<'
        elif(sign == 'Plus'):
            sign = '>'
        fun_body = f'''\
        


    def {name}(self, {dimension}, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) {sign} self.getCoord(right, sDimension):
            return self.{fun_name}(dimension, LEFT)
        else:
            return self.{fun_name}(dimension, RIGHT)'''
        
    return fun_body


def Line(name, landmark:list, sign, what, dimension, direction, sDimension):

    if dimension != None:
        dimension = f'dimension={dimension}'
    else:
        dimension = 'dimension'
    
    if direction != None:
        direction = f'direction={direction}'
    else:
        direction = 'direction'
    
    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'

    if sign is None:
        if len(landmark) == 1:
            fun_body = f'''\
            


    def {name}(self, {dimension}):
        return self.getLine(self.left{landmark[0]}, self.right{landmark[0]}, dimension)'''
        elif len(landmark) == 2:
            fun_body = f'''\
            


    def {name}(self, {dimension}, line, {direction}):
        left = self.getLine(self.left{landmark[0]}, self.left{landmark[1]}, dimension, line)
        right = self.getLine(self.right{landmark[0]}, self.right{landmark[1]}, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg'''
    else:
        fun_name = "get" + "".join(landmark) + what
        if(sign == 'Minus'):
            sign = '<'
        elif(sign == 'Plus'):
            sign = '>'
        fun_body = f'''\
        


    def {name}(self, {dimension}, line, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) {sign} self.getCoord(right, sDimension):
            return self.{fun_name}(dimension, line, LEFT)
        else:
            return self.{fun_name}(dimension, line, RIGHT)'''
        
    return fun_body


def Number(name, landmark:list, sign, sDimension):
    leftRight = []
    if(sign == 'Minus'):
        leftRight.append('left')
        leftRight.append('right')
    elif(sign == 'Plus'):
        leftRight.append('right')
        leftRight.append('left')

    if sDimension != None:
        sDimension = f'sDimension={sDimension}'
    else:
        sDimension = 'sDimension'
    
    fun_body = f'''\
    


    def {name}(self, {sDimension}, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.{leftRight[0]}{landmark[0]}
        else:
            return self.{leftRight[1]}{landmark[0]}'''
    
    return fun_body


def OnlyGetShoulderCenterHipCenterLine():
    fun_body = f'''\
    

    def getShoulderCenterHipCenterLine(self, dimension, line):
        shoulderCenter = self.getCenterPoint(self.leftShoulder, self.rightShoulder)
        hipCenter = self.getCenterPoint(self.leftHip, self.rightHip)
        return self.getLine(shoulderCenter, hipCenter, dimension, line)'''
    
    return fun_body


if __name__ == '__main__':

    # text = "getShoulderHipKneeAngle"
    # text = "getNoseShoulderPlusLine"
    # text = "getShoulderCenterHipCenterLine"
    text = "getAnkleKneeFootIndexAngle"
    # text = "getNosePoint"
    capitalized_words = re.findall(r'[A-Z][a-z]*', text)

    if any(x in capitalized_words for x in ['Minus', 'Plus', 'Center']):
        print(f"부위 : {capitalized_words[:-2]}")
        landmark = capitalized_words[:-2]
        print(f"방향 : {capitalized_words[-2]}")
        direction = capitalized_words[-2]
        print(f"구하는 것 : {capitalized_words[-1]}")
        what = capitalized_words[-1]
    else:
        print(f"부위 : {capitalized_words[:-1]}")
        landmark = capitalized_words[:-1]
        direction = None
        print(f"구하는 것 : {capitalized_words[-1]}")
        what = capitalized_words[-1]

    if what == 'Point':
        Point(text, landmark, direction)
    elif what == 'Distance':
        Distance(text, landmark, direction)
    elif what == 'Angle':
        Angle(text, landmark, direction)
    elif what == 'Plane':
        Plane(text, landmark, direction)
    elif what == 'Line':
        Line(text, landmark, direction)
    elif what == 'Number':
        Number(text, landmark, direction)