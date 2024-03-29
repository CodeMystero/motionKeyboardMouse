import cv2  # OpenCV 라이브러리 import
import sys  # sys 모듈 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.
import math  # math 모듈 import
import pyautogui

points = None
fingers = None

# 거리 계산 함수 선언
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))  # 두 점 p1, p2의 x, y 좌표로 거리를 계산한다.

# 세 점 사이의 각도 계산 함수 선언
def calculate_angle(p1, p2, p3):   
# 벡터 계산
    v1 = (p1.x - p2.x, p1.y - p2.y)
    v2 = (p3.x - p2.x, p3.y - p2.y)

# 벡터의 크기 계산
    v1_mag = math.sqrt(v1[0]**2 + v1[1]**2)
    v2_mag = math.sqrt(v2[0]**2 + v2[1]**2)

# 내적 계산
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]

# 코사인 값 계산
    cosine_angle = dot_product / (v1_mag * v2_mag)

# 각도 계산 (라디안)
    angle_rad = math.acos(cosine_angle)

# 라디안 값을 각도로 변환하여 반환
    angle =math.degrees(angle_rad)

# 손 좌표 인식 함수 선언
def dect_hand(image):
    global points

    results = hands.process(image)  # 이미지에서 손을 찾고 결과를 반환

    if results.multi_hand_landmarks:  # 손이 인식되었는지 확인
        for hand_landmarks in results.multi_hand_landmarks:  # 반복문을 활용해 인식된 손의 주요 부분을 그림으로 그려 표현
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            points = hand_landmarks.landmark  #  landmark 좌표 정보들을 points라는 변수로 활용
    
# 손가락 인식 함수 선언
def dect_finger(points):
    global fingers
    if points is not None: # points가 None이 아닌 경우에만 인덱싱 작업을 수행
        fingers = 0
        if distance(points[4], points[9]) > distance(points[3], points[9]):
            fingers += 1  # 폈으면 fingers에 1을 더한다.

    # 나머지 손가락 확인하기
        for i in range(8, 21, 4):
            if distance(points[i], points[0]) > distance(points[i - 1], points[0]):
                fingers += 1  # 폈으면 fingers에 1을 더한다.
         
# MediaPipe 패키지에서 사용할 기능들.
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands  # 손 인식을 위한 객체

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 비디오 캡처 객체 생성

if not cap.isOpened():  # 연결 확인
    print("Camera is not opened")
    sys.exit(1)  # 프로그램 종료

hands = mp_hands.Hands()  # 손 인식 객체 생성

while True:  # 무한 반복
    res, frame = cap.read()  # 카메라 데이터 읽기
    frame_height, frame_width, _ = frame.shape

    if not res:  # 프레임 읽었는지 확인
        print("Camera error")
        break  # 반복문 종료

    frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 미디어파이프에서 인식 가능한 색공간으로 변경
    

    dect_hand(image)
    dect_finger(points)

    if points is not None:
        print(calculate_angle(points[6], points[7], points[5]))
        


    # 주먹 인식
    if fingers == 0:
        hand_shape = "rock"
        cv2.putText(  # 인식된 내용을 이미지에 출력한다.
            frame,
            hand_shape,
            (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            1
        )

    # 마우스 움직이기 & 클릭
    elif fingers == 2:
        if distance(points[8], points[0]) > distance(points[7], points[0]):
            if distance(points[4], points[0]) > distance(points[3], points[0]):
                cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                frame,
                "Default",
                (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                1
                )
                x = int(points[8].x * frame_width)
                y = int(points[8].y * frame_height)

                pyautogui.moveTo(x, y)
                
                print(distance(points[8], points[4])*100)
                if distance(points[8], points[4]) < 10:
                    pyautogui.click()
                
        

    cv2.imshow("MediaPipe Hands", frame)

    key = cv2.waitKey(1) & 0xFF  # 키보드 입력받기
    if key == 27:  # ESC를 눌렀을 경우
        break  # 반복문 종료

cv2.destroyAllWindows()  # 영상 창 닫기
cap.release()  # 비디오 캡처 객체 해제
