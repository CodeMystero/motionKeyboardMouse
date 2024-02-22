import cv2  # OpenCV 라이브러리 import
import sys  # sys 모듈 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.
import math  # math 모듈 import
import pyautogui

from threading import Thread

from speech_recognition import *
import clipboard
import keyboard
import pyaudio

import time
time_init = True
rad = 40

dscr_speed = -30
uscr_speed = 30

points = None
fingers = None

audio_flag = False

# 거리 계산 함수 선언
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))  # 두 점 p1, p2의 x, y 좌표로 거리를 계산한다.

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
        
        
    elif fingers == 2:
        time_init = True
        if distance(points[8], points[0]) > distance(points[7], points[0]) and\
            distance(points[4], points[0]) > distance(points[3], points[0]):
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

            pyautogui.moveTo(x*2, y*2)
                
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
   
