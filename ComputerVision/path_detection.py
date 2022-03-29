from cmath import inf
import numpy as np
import cv2

class Walle:
    def __init__(self, width=640, height=480, debug=False, vis=False):
        self.width = width
        self.height = height
        self.debug = debug
        self.vis = vis
        self.mid = int(self.width/2)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

    def detect(self):
        ret, frame = self.cap.read()
        cv2.imshow('Edges', frame)


        frame_blur = cv2.GaussianBlur(frame, (3,3), sigmaX=0, sigmaY=0)
        edges = cv2.Canny(image=frame_blur, threshold1=100, threshold2=200)
        detected_lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=200)

        if type(detected_lines) != type(None):
            left_m = []
            left_n = []
            right_m = []
            right_n = []

            # Iterate over points
            for points in detected_lines:
                # Extracted points nested in the list
                x1,y1,x2,y2=points[0]
                # Calculate the slope
                m = (y2-y1)/(x2-x1)
                if m == inf or m == -inf:
                    m = 100000
                # Calculate the displacement 
                # y = mx + n => n = y - mx
                n = y1 - m * x1
                if m > 0:
                    left_m.append(m)
                    left_n.append(n)

                else:
                    right_m.append(m)
                    right_n.append(n)

                # Draw the lines joing the points
                # On the original image
                if self.vis:
                    cv2.line(frame, (x1,y1),(x2,y2),(0,255,0),2)

            m_right_avg = np.median(right_m)
            m_left_avg = np.median(left_m)

            n_right_avg = np.median(right_n)
            n_left_avg = np.median(left_n)

            # y = m1x+n1
            # y = m2x+n2

            # m2x + n2 = m1x+n1 => m2x - m1x = n1 -n2 => x = (n1 - n2)/(m2 - m1)
            # right => 1, left => 2

            # Point where they meet
            x = (n_right_avg - n_left_avg) / (m_left_avg - m_right_avg)
            y = m_left_avg * x + n_left_avg
            fuge_point = [x, y]

            if self.debug:
                if fuge_point[0] < 0 or fuge_point[1] < 0:
                    print(fuge_point)
            
            try:
                if self.vis:
                    cv2.circle(frame, (int(fuge_point[0]), int(fuge_point[1])), radius=5, thickness=-1, color=(255,0,0))
            except:
                pass
            
            if self.vis:
                cv2.imshow('Edges', edges)
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)


            x = fuge_point[0]
            center = 640 / 2
            tolerance = 50

            if abs(x - center) > tolerance:
                if x < center:
                    return "LEFT"
                else:
                    return "RIGHT"
            else:
                return "GO AHEAD"

        if self.vis:
            cv2.imshow('Edges', edges)
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        return "GO AHEAD"

if __name__== "__main__":
    wall = Walle(vis=True)
    while True:
        result = wall.detect()
        print(result)