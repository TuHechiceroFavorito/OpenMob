from cmath import inf
import numpy as np
import cv2

# Walle follows trays. This thing follows a path
class Walle:
    def __init__(self, width=640, height=480, debug=False, vis=False):
        # Frame dimensions
        self.width = width
        self.height = height
        self.debug = debug              # Debugging output is true
        self.vis = vis                  # Shows the processed frames if true
        self.mid = int(self.width/2)    # Defines mid point of the frame

        # Set the camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

    # Detects the path. Returns which direction to follow
    def detect(self):
        # Read frame from the camera
        ret, frame = self.cap.read()
        cv2.imshow('Edges', frame)

        frame_blur = cv2.GaussianBlur(frame, (3,3), sigmaX=0, sigmaY=0)             # Blur the image
        edges = cv2.Canny(image=frame_blur, threshold1=100, threshold2=200)         # Detect edges on the image
        detected_lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=200)  # Detect lines on the image

        # Don't run the algorithm if no lines were detected
        if type(detected_lines) != type(None):
            # Lists to hold parameters for the lines on left and right sides
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

            # Get the median for the parameters of each line from all the calculated ones
            # Using the median instead of the average means that outliers don't generate big errors in calculations
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

            # If debug variable true, print the point
            if self.debug:
                if fuge_point[0] < 0 or fuge_point[1] < 0:
                    print(fuge_point)
            
            try:    # Try statement. Cant remember why
                # If vis true, draw a point indicating the fuge point
                if self.vis:
                    cv2.circle(frame, (int(fuge_point[0]), int(fuge_point[1])), radius=5, thickness=-1, color=(255,0,0))
            except:
                pass
            
            # Show frames only if vis is true
            if self.vis:
                cv2.imshow('Edges', edges)
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)


            x = fuge_point[0]
            center = 640 / 2
            tolerance = 50
            # From the diviation of the fuge point from the middle of the frame, calculate what action to take
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

# Testing
if __name__== "__main__":
    wall = Walle(vis=True)
    while True:
        result = wall.detect()
        print(result)