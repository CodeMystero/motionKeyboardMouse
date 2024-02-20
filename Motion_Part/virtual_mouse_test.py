import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

hand_detector = mp.solutions.hands.Hands()

drawing_utils = mp.solutions. drawing_utils

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1) # flip 화면 전환, 양수이면 좌우반전
    frame_height, frame_width, _ = frame.shape # 높이(480), 너비(640), 채널
    #print(frame_height, frame_width) # 480x640
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame) # process()메서드는 주어진 프레임에 손을 감지하고 결과를 반환
    hands = output.multi_hand_landmarks # 감지된 손의 랜드마크 정보를 얻음
    if hands: # 변수가 비어있지 않으면 if문 실행
        for hand in hands: # 감지된 손의 개수만큼 반복
           drawing_utils.draw_landmarks(frame, hand)
           landmarks = hand.landmark
           for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                print(x, y)
                if id == 8:
                  cv2.circle(img = frame, center=(x,y), radius=10, color=(0,0,0))
                  pyautogui.moveTo(x, y)

    #print(hands)
    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
      break

