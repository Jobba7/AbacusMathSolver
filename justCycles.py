import cv2
import numpy as np

# Starte die Webcam
cap = cv2.VideoCapture(1)  # '0' bedeutet die Standard-Webcam, ggf. anpassen, falls mehrere Kameras vorhanden sind

if not cap.isOpened():
    print("Fehler beim Zugriff auf die Webcam")
    exit()

while True:
    # Lese den aktuellen Frame der Webcam
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Lesen des Frames")
        break
    
    # Bildschirmgröße ermitteln und Bild auf Bildschirmgröße skalieren
    screen_res = 1280, 720  # Zielauflösung
    scale_width = screen_res[0] / frame.shape[1]
    scale_height = screen_res[1] / frame.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)
    frame = cv2.resize(frame, (window_width, window_height))
    
    # Konvertiere den Frame in den HSV-Farbraum, um Farben leichter zu erkennen
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Erster Bereich für Rottöne (von 0 bis 10)
    lower_red_1 = np.array([0, 150, 50])
    upper_red_1 = np.array([10, 255, 255])
    mask_red_1 = cv2.inRange(hsv_image, lower_red_1, upper_red_1)

    # Zweiter Bereich für Rottöne (von 170 bis 179)
    lower_red_2 = np.array([170, 150, 50])
    upper_red_2 = np.array([179, 255, 255])
    mask_red_2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)

    # Masken für Rot kombinieren
    mask_red = cv2.bitwise_or(mask_red_1, mask_red_2)

    # Blaue Kugeln mit begrenzter Helligkeit und hoher Sättigung
    lower_blue = np.array([90, 150, 50])  # Untere Grenze für Blautöne
    upper_blue = np.array([130, 255, 255])  # Obere Grenze für Blautöne
    mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Finde die Konturen der roten Kugeln
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_dots_count = 0
    for contour in contours_red:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter > 0:
            circularity = 4 * np.pi * (area / (perimeter ** 2))  # Rundheitsberechnung
            
            # Filter für Rundheit und Größe, um nur Kugeln zu erkennen
            if 0.7 < circularity < 1.2 and 100 < area < 2000:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                if radius > 5:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)  # Zeichne rote Umrandung für rote Kugeln
                    red_dots_count += 1

    # Finde die Konturen der blauen Kugeln
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_dots_count = 0
    for contour in contours_blue:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)  # Zeichne blaue Umrandung für blaue Kugeln
            blue_dots_count += 1

    # Zeige die Anzahl der erkannten Kugeln im Fenster
    cv2.putText(frame, f"Rote Punkte: {red_dots_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Blaue Punkte: {blue_dots_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, f"Insgesamt: {red_dots_count + blue_dots_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Zeige das Ergebnis im Live-Bild
    cv2.imshow("Erkannte Kugeln (Live)", frame)

    # Beenden mit der 'q'-Taste
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release der Webcam und Schließen aller Fenster
cap.release()
cv2.destroyAllWindows()
