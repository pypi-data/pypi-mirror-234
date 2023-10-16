import csv
from utils.pose_util import Coordinate


def readCSV(filename, preifx =1):
    resultList = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            newList = [line[0]]
            for i in range(preifx, preifx+99, 3):
                newList.append(Coordinate(x=float(line[i]), y=float(line[i + 1]), z=float(line[i + 2])))
            resultList.append(newList)
    return resultList


def writeCSV(filename, data):
    print(filename)
    with open(filename, 'w', encoding="utf-8") as f:
        wr = csv.writer(f)
        for poseList in data:
            rowData = [poseList[0]]
            for k in poseList[1:]:
                rowData.append(k.x)
                rowData.append(k.y)
                rowData.append(k.z)
            # print(rowData)
            wr.writerow(rowData)


def mergeCSV(file_1, file_2):
    fr_1 = readCSV(file_1, 0)
    fr_2 = readCSV(file_2, 0)
    fr_1.extend(fr_2)
    output_path = file_1.split('.csv')[0] + "_merge.csv"
    writeCSV(output_path, fr_1)

