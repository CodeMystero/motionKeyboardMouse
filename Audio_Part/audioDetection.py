from speech_recognition import *
from pyautogui import *
import clipboard
import keyboard
import pyaudio
import time

# def read_voice(): # 음성 인식을 하는 함수
#     r = Recognizer()
#     mic = Microphone() # 마이크 객체
    
#     with mic as source:
#         audio = r.listen(source) # 음성 읽어오기
        
#     voice_data = r.recognize_google(audio, language='ko')
#     print(voice_data)
#     return voice_data # 값 반환

def read_voice(): # 음성 인식을 하는 함수
    r = Recognizer()
    mic = Microphone() # 마이크 객체
    
    try:
        with mic as source:
            audio = r.listen(source) # 음성 읽어오기
            
        voice_data = r.recognize_google(audio, language='ko')
        print(voice_data)
        return voice_data # 값 반환  
    
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        return None
    
    except sr.RequestError as e:
        print("음성 인식 서비스에 오류가 발생했습니다:", e)
        return None
    
    except Exception as e:
        print("오류가 발생했습니다:", e)
        return None

def typing(value): # 키보드 입력을 하는 함수
    clipboard.copy(value)
    hotkey('ctrl', 'v')
    
while True:
    if keyboard.is_pressed('ctrl+alt'): # ctrl+alt를 눌렀을 때에 실행 
        voice = read_voice() # 음성 인식
        time.sleep(0.1) 
        typing(voice) # 타이핑
        #press('enter') # 줄바꿈 하기
