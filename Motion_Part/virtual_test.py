import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # BGR을 RGB로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Mediapipe를 이용하여 손 감지
            results = hands.process(frame_rgb)

            # 손이 감지된 경우
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 엄지 손가락의 끝점 좌표 얻기
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])

                    # 엄지 손가락이 수직으로 펴진 경우
                    if thumb_tip_x > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]:
                        # "Thumb Up" 문자열 출력
                        cv2.putText(frame, 'Thumb Up', (thumb_tip_x, thumb_tip_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # 프레임 출력
            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()