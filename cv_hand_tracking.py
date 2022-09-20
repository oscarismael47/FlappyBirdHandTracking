import cv2 # pip install opencv-contrib-python
import mediapipe as mp # pip install mediapipe
import numpy as np

class Hand_tracking:
    def __init__(self,max_num_hands=1):
        self.max_num_hands = max_num_hands
        # For webcam input
        self.cap = cv2.VideoCapture(1)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def close_camera(self):
        self.cap.release()

    def process_frame(self):
        image,hands_data = 0, []
        success,image = self.cap.read()
        if success :
            h,w,_ = image.shape
            color_line = (0, 0, 255)
            thickness_line = 1
            with self.mp_hands.Hands(max_num_hands=self.max_num_hands, min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
                # the BGR image to RGB.qqq
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = hands.process(image)
                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                hands_data = []
                if results.multi_hand_landmarks:
                    for hand_landmarks,hand_class in zip(results.multi_hand_landmarks,results.multi_handedness):
                        hand_class = hand_class.classification[0].label
                        keypoints = []
                        for data_point in hand_landmarks.landmark:
                            # X,Y,Z
                            keypoints.append([data_point.x,data_point.y,data_point.z])
                        keypoints = np.asarray(keypoints)    
                        hands_data.append([hand_class,keypoints])                         
                        hands_data = hands_data

                        self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())
                
            image = cv2.line(image, (0,int(h/2)), (w,int(h/2)), color_line, thickness_line)
            return  success,image,hands_data

   
if __name__ == "__main__":
    hand_tracking = Hand_tracking( max_num_hands=1)
    state = False
    i = 0
    while True:
        success,image,hands_data = hand_tracking.process_frame()
        if success is False: continue
        try:
            point = hands_data[0][1][9]
            point_y = point[1]
            if point_y <0.5:
                state = True
            if point_y >0.5 and state is True:
                state = False
                i=1
            else:
                i=0
        except:
            pass

        cv2.imshow('hand tracking images',image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    hand_tracking.close_camera()
    cv2.destroyAllWindows()