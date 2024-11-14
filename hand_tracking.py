import cv2
import mediapipe as mp
import time

# Initialisiere Mediapipe Handerkennung
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Starte Kamera-Stream
cap = cv2.VideoCapture(0)

# Initialisiere Timer
start_time = time.time()

# Hilfsfunktion zur Bestimmung der Anzahl gestreckter Finger
def count_fingers(hand_landmarks):
    # Finger-Status für jeden Finger (1 = gestreckt, 0 = gebogen)
    fingers = []

    # Prüfe den Daumen (seitliche Bewegung)
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Prüfe die anderen vier Finger (vertikale Bewegung)
    for id in range(1, 5):
        finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark(id * 4)]
        finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 - 2)]
        
        if finger_tip.y < finger_dip.y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Kamera konnte nicht geöffnet werden.")
        break

    # Flippen des Frames für eine natürliche Darstellung
    frame = cv2.flip(frame, 1)
    # Konvertiere das Bild zu RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Erkenne Hände
    results = hands.process(rgb_frame)

    # Wenn Hände erkannt werden
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Zeichne Handlandmarken auf das Bild
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Zähle die gestreckten Finger
            finger_count = count_fingers(hand_landmarks)

            # Überprüfe, ob 3 Sekunden vergangen sind
            current_time = time.time()
            if current_time - start_time >= 3:
                print(f"Anzahl gestreckter Finger: {finger_count}")
                start_time = current_time

    # Zeige das Bild mit Hand-Tracking
    cv2.imshow('Hand Tracking', frame)

    # Beenden bei Tastendruck 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ressourcen freigeben
cap.release()
cv2.destroyAllWindows()
hands.close()
