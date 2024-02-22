import cv2  # OpenCV 라이브러리 import
import sys  # sys 모듈 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.
import math  # math 모듈 import
import pyautogui
import numpy as np


from threading import Thread

from speech_recognition import *
import clipboard
import keyboard
import pyaudio

import time
time_init = True
time_init_dclick = True
rad = 40

dscr_speed = -30
uscr_speed = 30

points = None
fingers = None

audio_flag = False

screen_width, screen_height = pyautogui.size()

def map_value(value, from_min, from_max, to_min, to_max):
    # 주어진 범위 내의 값(value)을 다른 범위(to_min ~ to_max)로 매핑하는 함수
    # 선형 보간법을 사용하여 값을 변환
    
    # 주어진 범위 내의 값의 비율을 계산
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled_value = (value - from_min) / from_range
    
    # 새로운 범위 내의 값을 계산
    new_value = to_min + (scaled_value * to_range)
    
    return new_value

##################################### 거리 계산 함수 ##########################################################
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))  

##################################### 각도 계산 함수 ###########################################################
def Angle(p1, p2, p3):   
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
    return math.degrees(angle_rad)

#########################################################################################################
def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
 
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
 
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
 
                if draw:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
 
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
 
            if draw:
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)
 
        return self.lmList, bbox
###############################################################################################################
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
    else: 
        return 0
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
                
                
#################### 오디오 인식 관련 메소드 #####################

def read_voice(): # 음성 인식을 하는 함수
    r = Recognizer()
    mic = Microphone() # 마이크 객체
    print("test1")
    try:
        print("test1.5")
        with mic as source:
            audio = r.listen(source) # 음성 읽어오기
        print("test2")
        voice_data = r.recognize_google(audio, language='ko')
        print(voice_data)
        return voice_data # 값 반환  
   
    except TimeoutError:
        print("음성 입력이 타임아웃되었습니다.")  # 타임아웃 메시지 출력
        return None
    
    except UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        return None
    
    except RequestError as e:
        print("음성 인식 서비스에 오류가 발생했습니다:", e)
        return None
    
    except Exception as e:
        print("오류가 발생했습니다:", e)
        return None

def typing(value): # 키보드 입력을 하는 함수
    if value is not None:
        clipboard.copy(value)
        pyautogui.hotkey('ctrl', 'v')
    else:
        print("클립보드에 복사할 수 없습니다.")

# 음성 인식 스레드 함수
def voice_recognition_thread():
    global audio_flag
    while True:
        if audio_flag:
            print("음성인식 준비 완료")
            voice = read_voice()  # 음성 인식
            print("음성 인식 완료")
            audio_flag = False
            time.sleep(0.1) 
            print("타이핑 준비")
            typing(voice) # 타이핑
            # 음성 인식 결과에 대한 처리 (예: 타이핑 등)
            
# 음성 인식 스레드 시작 & 메인 스레드 종료시 서브 스레드 강제종료 코드 
if __name__ == '__main__':
    voice_thread = Thread(target=voice_recognition_thread)
    voice_thread.daemon = True
    voice_thread = Thread(target= voice_recognition_thread, daemon = True)
    voice_thread.start()
#################################################################
         
###################################### MediaPipe 패키지에서 사용할 기능들. ######################################
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands  # 손 인식을 위한 객체

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 비디오 캡처 객체 생성

if not cap.isOpened():  # 연결 확인
    print("Camera is not opened")
    sys.exit(1)  # 프로그램 종료

hands = mp_hands.Hands()  # 손 인식 객체 생성


############################################### MAIN #############################################################

while True:  # 무한 반복

    res, frame = cap.read()  # 카메라 데이터 읽기
    frame_height, frame_width, ch = frame.shape
    # frameR = 100
    output = frame.copy()
    cv2.rectangle(frame, (int(0.3*frame_width), int(0.3*frame_height)), (int(0.7*frame_width), int(0.7*frame_height)), (218, 112, 214), -1)
    frame = cv2.addWeighted(frame, 0.2, output, 1 - .2, 0, output)
    
    if not res:  # 프레임 읽었는지 확인
        print("Camera error")
        break  # 반복문 종료

    frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 미디어파이프에서 인식 가능한 색공간으로 변경
    
        

    res = dect_hand(image)
    dect_finger(points)
    if res != 0:
    ####################################### 손가락 0개 ######################################################
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
            if audio_flag == False:
                audio_flag = True  # 음성 인식 필요 시 audio_flag를 True로 설정
            
    ####################################### 손가락 2개 ######################################################       
        elif fingers == 2:
            time_init = True
            if (points[11].y > points[10].y and points[15].y > points[14].y and points[19].y > points[18].y):
                
            
                
                # if frameR <= points[4].x <= frame_width - frameR:
                #    x3 = np.interp(points[4].x, (frameR, frame_width-frameR), (0, screen_width))
                # if frameR <= points[4].y <= frame_height - frameR:
                #    y3 = np.interp(points[4].y, (frameR, frame_height-frameR), (0, screen_height))
                
                
                
                if (points[4].x > 0.25 and points[4].x <0.75 and points[4].y > 0.25 and points[4].y <0.75):
                    x = int(map_value(points[4].x,0.3,0.7,0,screen_width))
                    y = int(map_value(points[4].y,0.3,0.7,0,screen_height))
                    pyautogui.moveTo(x, y)
                

                # clocX = plocX + (x3 - plocX) / smoothening
                # clocY = plocY + (y3 - plocY) / smoothening
 
 
                
                # 좌클릭
                if Angle(points[4], points[2], points[8]) < 15 and not (points[4].y < points[8].y): 
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "Left once",
                    (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                    pyautogui.click()
                    
                
                # 우클릭
                elif  Angle(points[4], points[2], points[8]) > 60: 
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "Right once",
                    (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                    pyautogui.click(button = 'right')
                    time.sleep(0.1)
    ####################################### 손가락 3개 ######################################################               
        elif fingers == 3:
            if (points[12].y < points[11].y and points[16].y > points[15].y and points[20].y > points[19].y\
                and points[3].y > points[4].y):   
                if points[4].x < points[17].x:
                    pyautogui.scroll(uscr_speed)
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "ScrUp",
                    (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                elif points[17].x < points[4].x:
                    pyautogui.scroll(dscr_speed)
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "ScrDn",
                    (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                    
    ####################################### 손가락 5개 ######################################################               
        elif fingers == 5:
            cv2.putText(  # 인식된 내용을 이미지에 출력한다.
            frame,
            "Process Running",
            (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            1
            )
            
            if time_init:
                ctime = time.time()
                time_init = False
            ptime = time.time()

            if (ptime - ctime) > 5:
                cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                frame,
                "Process ShutDown",
                (int(points[20].x * frame.shape[1]), int(points[20].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                1
                )
                cv2.destroyAllWindows()  # 영상 창 닫기
                cap.release()  # 비디오 캡처 객체 해제
            


    cv2.imshow("MediaPipe Hands", frame)
    cv2.waitKey(1)
   
