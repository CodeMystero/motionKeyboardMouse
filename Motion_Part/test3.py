import cv2
import sys
import mediapipe as mp
import math
import pyautogui

################################# audio
from threading import Thread

from speech_recognition import *
import clipboard
import keyboard
import pyaudio

import time
time_init = True
##rad = 40

audio_flag = False
####################################



screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

class HandTracker:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.points = None
        self.fingers = None
        self.flags = None
        self.dscr_speed = -30
        self.uscr_speed = 30
        self.time_init = True
        self.audio_flag = False

    def distance(self, p1, p2): # 거리 측정
        return math.dist((p1.x, p1.y), (p2.x, p2.y))

    def Angle(self, p1, p2, p3): # 각도 측정
        v1 = (p1.x - p2.x, p1.y - p2.y)
        v2 = (p3.x - p2.x, p3.y - p2.y)
        v1_mag = math.sqrt(v1[0]**2 + v1[1]**2)
        v2_mag = math.sqrt(v2[0]**2 + v2[1]**2)
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        cosine_angle = dot_product / (v1_mag * v2_mag)
        angle_rad = math.acos(cosine_angle)
        return math.degrees(angle_rad)

    def detect_hand(self, frame, image): # 손 인식
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks)
                self.points = hand_landmarks.landmark
        

    def count_finger(self): # 손가락 개수 측정
        if self.points is not None:
            self.fingers = 0
            if self.distance(self.points[4], self.points[9]) > self.distance(self.points[3], self.points[9]):
                self.fingers += 1
            for i in range(8, 21, 4):
                if self.distance(self.points[i], self.points[0]) > self.distance(self.points[i - 1], self.points[0]):
                    self.fingers += 1
        return self.fingers

    def draw_hand_shape(self, frame, fingers):
        if fingers == 0:
            hand_shape = "rock"
            cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                frame,
                hand_shape,
                (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                1
            )
            if audio_flag == False:
                audio_flag = True  # 음성 인식 필요 시 audio_flag를 True로 설정
        elif fingers == 2:
            if self.distance(self.points[8], self.points[0]) > self.distance(self.points[7], self.points[0]):
                if self.distance(self.points[4], self.points[0]) > self.distance(self.points[3], self.points[0]):
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "Default",
                    (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                    x = int(self.points[8].x * screen_width)
                    y = int(self.points[8].y * screen_height)

                    pyautogui.moveTo(x, y)
                
                
                if (self.Angle(self.points[8], self.points[6], self.points[5])) < 150 :
                    print("L_click")
                    pyautogui.click()
                
                if(self.Angle(self.points[4], self.points[0], self.points[8])) > 30:
                    print("R_click")
                    pyautogui.click(button = 'right')

        elif fingers == 3:
            if (self.points[12].y < self.points[11].y and self.points[16].y > self.points[15].y and self.points[20].y > self.points[19].y\
            and self.points[3].y > self.points[4].y):   
                if self.points[4].x < self.points[17].x:
                    pyautogui.scroll(self.uscr_speed)
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "ScrUp",
                    (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                elif self.points[17].x < self.points[4].x:
                    pyautogui.scroll(self.dscr_speed)
                    cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                    frame,
                    "ScrDn",
                    (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1
                    )
                
        elif fingers == 5:
            cv2.putText(  # 인식된 내용을 이미지에 출력한다.
            frame,
            "Process Running",
            (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
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
                (int(self.points[20].x * frame.shape[1]), int(self.points[20].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                1
                )
                cv2.destroyAllWindows()  # 영상 창 닫기
                cap.release()  # 비디오 캡처 객체 해제

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

                
        
tracker = HandTracker()

if not cap.isOpened():
    print("Camera is not opened")
    sys.exit(1)



while True:
    res, frame = cap.read()
    frame_height, frame_width, ch = frame.shape

    if not res:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    tracker.detect_hand(frame, image)
    fingers = tracker.count_finger()

    tracker.draw_hand_shape(frame, fingers)



    cv2.imshow("virtual_mouse", frame)
    cv2.waitKey(1)


