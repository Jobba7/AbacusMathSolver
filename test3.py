import cv2
import numpy as np

# Variablen für die ausgewählten Farbgrenzen
selected_color_lower = None
selected_color_upper = None

# Mouse-Callback-Funktion für die Auswahl der Farbe
def select_color(event, x, y, flags, param):
    global selected_color_lower, selected_color_upper, hsv_image
    if event == cv2.EVENT_LBUTTONDOWN:
        # Farbwert am Klickpunkt in HSV ermitteln
        selected_color = hsv_image[y, x]
        hue = selected_color[0]
        saturation = selected_color[1]
        value = selected_color[2]

        # Erstelle eine kleine Toleranz um den Farbwert herum
        tolerance = 20
        selected_color_lower = np.array([max(0, hue - tolerance), max(50, saturation - 50), max(50, value - 50)])
        selected_color_upper = np.array([min(179, hue + tolerance), min(255, saturation + 50), min(255, value + 50)])

        print(f"Ausgewählte Farbe (HSV): {selected_color}")
        print(f"Unterer Bereich: {selected_color_lower}")
        print(f"Oberer Bereich: {selected_color_upper}")

# Starte die Webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Bild")
cv2.setMouseCallback("Bild", select_color)

while True:
    # Lese den aktuellen Frame der Webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Konvertiere den Frame in den HSV-Farbraum
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Falls eine Farbe ausgewählt wurde, Maskiere den Bereich im Frame
    if selected_color_lower is not None and selected_color_upper is not None:
        mask = cv2.inRange(hsv_image, selected_color_lower, selected_color_upper)

        # Finde die Konturen der ausgewählten Farbe
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)  # Zeichne grüne Umrandung

        # Zeige die Maske zur Überprüfung an
        cv2.imshow("Maske der ausgewählten Farbe", mask)

    # Zeige das Ergebnis im Live-Bild
    cv2.imshow("Bild", frame)

    # Beenden mit der 'q'-Taste
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release der Webcam und Schließen aller Fenster
cap.release()
cv2.destroyAllWindows()
