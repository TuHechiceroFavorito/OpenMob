from pydoc import classname
import cv2
import numpy as np

class Detector:
    def __init__(self, width=640, height=480, debug=False, vis=False):
        self.width = width
        self.height = height
        self.debug = debug
        self.vis = vis
        self.mid = int(self.width/2)

        path = "ComputerVision/Object_Detection_Files/"

        classFile = path + "coco.names"
        with open(classFile, "r") as f:
            classNames = f.read().rstrip("\n").split('\n')

        configPath = path + "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = path + "frozen_inference_graph.pb"

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def sort_array(self, array):
        ind = np.lexsort((array[:,1],array[:,0]))
        return array[ind]

    def get_clean_boxes(self, coordinates):
        for a in range(len(coordinates) - 1):
            b = a + 1
            try:
                while coordinates[b] < coordinates[a]:
                    c = b + 1
                    if coordinates[c] < coordinates[a]:
                        del coordinates[c]
                        del coordinates[b]
                    else:
                        del coordinates[b]
                        del coordinates[a]

            except IndexError:
                break

        return coordinates

    def detect(self):
        debug = self.debug
        vis = self.vis

        success, img = self.cap.read()
        classIds, confs, bbox = self.net.detect(img, confThreshold=0.5)

        if len(bbox) > 0:
            if debug: print("Original boxes:", bbox)
            bbox = self.sort_array(bbox)
            if debug: print("Sorted boxes:", bbox)

            coordinates = [0]

            for box in bbox:
                coordinates.append(box[0])
                coordinates.append(box[0] + box[2])
        
            coordinates.append(self.width)
            if debug: print("Coordinates:", coordinates)
            coordinates = self.get_clean_boxes(coordinates)

            i = 0
            free_path = [0, [0, 0, self.width, self.height]]
            while i < len(coordinates):
                s = coordinates[i]
                e = coordinates[i + 1]
                start_point = (s, 0)
                end_point = (e, self.height)

                if e - s > free_path[0]:
                    free_path[0] = e - s
                    free_path[1] = start_point + end_point

                if debug: print("Start and end point:", start_point, end_point)
                if vis: cv2.rectangle(img, start_point + end_point, color=(0,0,255), thickness=2)
                i += 2

            if vis: cv2.rectangle(img, free_path[1], color=(0,255,0), thickness=2)

            midpoint = int((free_path[1][2] - free_path[1][0]) / 2) + free_path[1][0]
            if midpoint < self.mid:
                if vis: cv2.putText(img, "LEFT", [50, int(self.height/2)], cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)
                result = "LEFT"
            else:
                if vis: cv2.putText(img, "RIGHT", [400, int(self.height/2)], cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)
                result = "RIGHT"

        else:
            if vis: cv2.putText(img, "GO AHEAD", [150, int(self.height/2)], cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)
            result = "FREE"

        if vis: 
            cv2.imshow("Output", img)
            cv2.waitKey(1)

        return result

if __name__ == "__main__":
    det = Detector(vis=True)
    while True:
        result = det.detect()
        print(result)