import speech_recognition as sr
import pyautogui
from pynput import keyboard

# Recognizer 객체 생성
r = sr.Recognizer()

# 마이크 설정
mic = sr.Microphone()

# 입력 종료 여부
input_finished = False

# 음성 인식 함수
def recognize_speech():
    with mic as source:
        try:
            # 오디오를 수집
            print("말을 시작해주세요. 엔터 키를 누르면 입력이 종료됩니다.")
            audio = r.listen(source)

            # 수집한 오디오를 텍스트로 변환
            text = r.recognize_google(audio, language='ko-KR')

            print("인식된 텍스트:", text)

            # 현재 마우스 커서 위치에 텍스트 입력
            pyautogui.typewrite(text)

            # "꺼져"가 인식되면 프로그램 종료
            if "꺼져" in text:
                print("프로그램을 종료합니다.")
                exit()

        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print("음성 인식 서비스에 오류가 발생했습니다:", e)
        except Exception as e:
            print("오류가 발생했습니다:", e)

# 키보드 입력 이벤트 핸들러
def on_press(key):
    global input_finished
    if key == keyboard.Key.enter:
        input_finished = True
        return False  # 입력 종료


while True:
    # 엔터 키 입력 대기
    print("엔터 키를 누를 때까지 대기합니다.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
    # 음성 인식 실행
    recognize_speech()
    