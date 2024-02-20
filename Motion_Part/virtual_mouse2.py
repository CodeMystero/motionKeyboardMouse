# 원본 코드 https://google.github.io/mediapipe/solutions/hands.html
# 마우스 제어 참고 https://blankspace-dev.tistory.com/416

"""The 21 hand landmarks."""
# 손가락 위치 정의 참고 https://mediapipe.dev/images/mobile/hand_landmarks.png
#
# WRIST = 0
# THUMB_CMC = 1
# THUMB_MCP = 2
# THUMB_IP = 3
# THUMB_TIP = 4    엄지
# INDEX_FINGER_MCP = 5
# INDEX_FINGER_PIP = 6
# INDEX_FINGER_DIP = 7
# INDEX_FINGER_TIP = 8  검지
# MIDDLE_FINGER_MCP = 9
# MIDDLE_FINGER_PIP = 10
# MIDDLE_FINGER_DIP = 11
# MIDDLE_FINGER_TIP = 12  중지
# RING_FINGER_MCP = 13
# RING_FINGER_PIP = 14
# RING_FINGER_DIP = 15
# RING_FINGER_TIP = 16  약지
# PINKY_MCP = 17
# PINKY_PIP = 18
# PINKY_DIP = 19
# PINKY_TIP = 20  새끼


# 필요한 라이브러리
# pip install opencv-python mediapipe pillow numpy pyautogui

import cv2 
import mediapipe as mp  
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import pyautogui  


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles


screen_width, screen_height = pyautogui.size()
print(screen_width, screen_height)


pre = ''
offset = 150

# For webcam input:
cap = cv2.VideoCapture(0)


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

 
  while cap.isOpened():
    success, image = cap.read()

    h,w,c = image.shape

    if not success:
      print("Ignoring empty camera frame.")

      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # screen_height : y_ = image_height : y
    # y_ = y*screen_height/image_height

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape


    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:


        # 엄지를 제외한 나머지 4개 손가락의 마디 위치 관계를 확인하여 플래그 변수를 설정합니다. 손가락을 일자로 편 상태인지 확인합니다.
        thumb_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height:
          if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height:
              thumb_finger_state = 1

        index_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
          if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
              index_finger_state = 1

        middle_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
          if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
              middle_finger_state = 1

        ring_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
          if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
              ring_finger_state = 1

        pinky_finger_state = 0
        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height:
          if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height:
            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height:
              pinky_finger_state = 1


        # 주먹을 쥐었다면
        if  index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
          # WRIST 좌표를 사용하여 마우스를 이동시킵니다.
          image_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*image_width
          image_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*image_height

          if image_x > offset and image_x < w-offset and image_y > offset and image_y < h - offset:
            image_x = image_x - offset
            image_y = image_y - offset
            new_image_height = image_height - offset*2
            new_image_width = image_width - offset*2

            screen_y = image_y*screen_height/new_image_height
            screen_x = image_x*screen_width/new_image_width

            pyautogui.moveTo(screen_x, screen_y)

            pre = 'move'

        # 손가락을 모두 폈다면
        elif thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
          pyautogui.mouseDown()
          pyautogui.mouseUp()

          pre = 'left click'

        # 가위라면
        elif thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:

          if pre != 'right click':
            pyautogui.mouseDown(button='right')
            pyautogui.mouseUp(button='right')

            pre = 'right click'

        '''
        # 손가락 위치 확인한 값을 사용하여 가위,바위,보 중 하나를 출력 해줍니다.
        font = ImageFont.truetype("gulim.ttc", 80)
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)


        w, h = font.getlength(pre)
    
        x = 50
        y = 50

        draw.rectangle((x, y, x + w, y + h), fill='black')
        draw.text((x, y),  pre, font=font, fill=(255, 255, 255))
        image = np.array(image)

        cv2.rectangle(image, (offset, offset), (image_width-offset, image_height-offset), (255,0,0), 2)
        '''
        
        # 손가락 뼈대를 그려줍니다.
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()