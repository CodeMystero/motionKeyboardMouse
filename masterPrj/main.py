import cv2  # OpenCV 라이브러리 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.
import math  # math 모듈 import
import pyautogui
import numpy as np
from threading import Thread
from speech_recognition import *
import clipboard
import time
#import os

                #+++++++++++++++++++++++++++ PyQT ++++++++++++++++++++++++++++
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,  QDesktopWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer 


class MainWindow(QWidget):
    def __init__(self, gif_path, delay_time):
        super().__init__()
        self.gif_path = gif_path
        self.delay_time = delay_time
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(self)
        layout.addWidget(label)

        movie = QMovie(self.gif_path)  # 사용자로부터 받은 GIF 파일 경로
        label.setMovie(movie)
        movie.start()
        
        # 타이머 설정
        timer = QTimer(self)
        timer.singleShot(self.delay_time, self.close)  # 사용자로부터 받은 딜레이 시간

        # Title bar 제거
        self.setWindowFlag(Qt.FramelessWindowHint)

        # 항상 최상위로 유지
        self.setWindowFlag(Qt.WindowStaysOnTopHint)


        # 화면 중앙에 윈도우 배치
        #self.center()
        
        self.setGeometry(400, 200, 400, 400)
        
        self.setWindowTitle('GIF Viewer')
        self.show()

        
                #+++++++++++++++++++++++++++ 글로벌 변수 선언 ++++++++++++++++++++++++++++

# 마우스의 커서가 (0,0)으로 가면 자동으로 프로세스가 종료되는 FAILSAFE기능 False로 변환
pyautogui.FAILSAFE = False

time_init = True
time_init_dclick = True
#rad = 40

# 스크롤 업다운 스피드 설정
dscr_speed = -120
uscr_speed = 120

points = None
fingers = None

audio_flag = False

x, y = pyautogui.position()


screen_width, screen_height = pyautogui.size()
                #+++++++++++++++++++++++++++ 디스플레이 맵핑 ++++++++++++++++++++++++++++
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

                #+++++++++++++++++++++++++++ 두 점 사이의 거리를 구하는 함수 ++++++++++++++++++++++++++++
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))  

#                #+++++++++++++++++++++++++++ 두 점 사이의 각도를 구하는 함수 ++++++++++++++++++++++++++++
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

                #+++++++++++++++++++++++++++ 손 좌표 인식 함수 ++++++++++++++++++++++++++++

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
                

                #+++++++++++++++++++++++++++ 로딩 페이지 ++++++++++++++++++++++++++++
def main():
    app = QApplication(sys.argv)
    window = MainWindow("loadingPage.gif",8000)
    app.exec_()

if __name__ == '__main__':
    main()



                
                #+++++++++++++++++++++++++++ 음성 인식 ++++++++++++++++++++++++++++

def read_voice(): # 음성 인식을 하는 함수
    r = Recognizer()
    mic = Microphone() # 마이크 객체
    try:
        with mic as source:
            audio = r.listen(source) # 음성 읽어오기
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

         
                #+++++++++++++++++++++++++++ 마우스 커서 결정 함수 ++++++++++++++++++++++++++++
         
def mouse_loc_thread():
    global x, y
    
    plocX, plocY = 0, 0
    smoothening = 3
    
    while True:
        
        clocX = plocX + (x - plocX) / smoothening
        clocY = plocY + (y - plocY) / smoothening
        
        pyautogui.moveTo(clocX, clocY)
        
        plocX, plocY = clocX, clocY
        
         
if __name__ == '__main__':
    mouse_thread = Thread(target=mouse_loc_thread)
    mouse_thread.daemon = True
    mouse_thread = Thread(target=mouse_loc_thread, daemon = True)
    mouse_thread.start()


         
                #+++++++++++++++++++++++++++ Mediapipe ++++++++++++++++++++++++++++
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands  # 손 인식을 위한 객체

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 비디오 캡처 객체 생성

if not cap.isOpened():  # 연결 확인
    print("Camera is not opened")
    
hands = mp_hands.Hands()  # 손 인식 객체 생성

                #+++++++++++++++++++++++++++ Main 함수 ++++++++++++++++++++++++++++
while True: 

    ret, frame = cap.read()  # 카메라 데이터 읽기
    
    if not ret:  # 프레임 읽었는지 확인
        print("Camera error")
        break  # 반복문 종료
    
    frame_height, frame_width, ch = frame.shape
    
    output = frame.copy()
    cv2.rectangle(frame, (int(0.3*frame_width), int(0.5*frame_height)), (int(0.7*frame_width), int(0.9*frame_height)), (218, 112, 214), -1)
    frame = cv2.addWeighted(frame, 0.2, output, 1 - .2, 0, output)

    frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 미디어파이프에서 인식 가능한 색공간으로 변경
    
    res = dect_hand(image)
    dect_finger(points)
    if res != 0:
                    #+++++++++++++++++++++++++++ 손가락 0 ++++++++++++++++++++++++++++
        if fingers == 0:
            if audio_flag == False:
                audio_flag = True  # 음성 인식 필요 시 audio_flag를 True로 설정
                
                    #+++++++++++++++++++++++++++ 손가락 1 ++++++++++++++++++++++++++++
        if fingers == 1:
           if(distance(points[8], points[0]) > distance(points[7], points[0])):
                print("backspace")     
                pyautogui.press('backspace')  
                time.sleep(0.5)
            
                    #+++++++++++++++++++++++++++ 손가락 2 ++++++++++++++++++++++++++++       
        elif fingers == 2:
            time_init = True
            if (points[11].y > points[10].y and points[15].y > points[14].y and points[19].y > points[18].y):

                
                if (points[4].x > 0.25 and points[4].x <0.75 and points[4].y > 0.45 and points[4].y <0.95):
                    x = int(map_value(points[4].x,0.3,0.7,0,screen_width))
                    y = int(map_value(points[4].y,0.5,0.9,0,screen_height))
                    
                print("default")
                # 좌클릭
                if Angle(points[4], points[2], points[8]) < 15:
                    if(points[2].y > points[13].y):
                        print("left")
                        pyautogui.click()
                    
                
                # 우클릭
                elif  Angle(points[4], points[2], points[8]) > 60: 
                    print("right")
                    pyautogui.click(button = 'right')
                    #+++++++++++++++++++++++++++ 손가락 3 ++++++++++++++++++++++++++++              
        elif fingers == 3:
            if (points[12].y < points[11].y and points[16].y > points[15].y and points[20].y > points[19].y\
                and points[3].y > points[4].y):   
                if points[4].x < points[17].x:
                    pyautogui.scroll(uscr_speed)
                    print("Scr Up")
                elif points[17].x < points[4].x:
                    pyautogui.scroll(dscr_speed)
                    print("Scr Down")
                    #+++++++++++++++++++++++++++ 손가락 4 ++++++++++++++++++++++++++++    
        elif fingers == 4:
            if Angle(points[16], points[14], points[13]) > 170:
                    print("enter")
                    pyautogui.press('enter')
                    time.sleep
            
                    #+++++++++++++++++++++++++++ 손가락 5 ++++++++++++++++++++++++++++            
        elif fingers == 5:
            if time_init:
                ctime = time.time()
                time_init = False
            ptime = time.time()

            if (ptime - ctime) > 5:
                
                cv2.destroyAllWindows()  # 영상 창 닫기
                cap.release()  # 비디오 캡처 객체 해제
                
                    #+++++++++++++++++++++++++++ 엔딩페이지  ++++++++++++++++++++++++++++
                
                def main():
                    app = QApplication(sys.argv)
                    window = MainWindow("endingPage.gif",3000)
                    sys.exit(app.exec_())

                if __name__ == '__main__':
                    main()

                #############################################################
    
                #cv2.destroyAllWindows()  # 영상 창 닫기
                #cap.release()  # 비디오 캡처 객체 해제
            

    # cv2.imshow("MediaPipe Hands", frame)
    # cv2.waitKey(1)
   