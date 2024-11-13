import cv2
import numpy as np

# Lade das Bild des Abacus
image = cv2.imread("abacus.jpg")

# Bildschirmgröße ermitteln
screen_res = 1280, 720  # Beispielwert für FullHD oder eine kleinere Größe wählen
scale_width = screen_res[0] / image.shape[1]
scale_height = screen_res[1] / image.shape[0]
scale = min(scale_width, scale_height)
window_width = int(image.shape[1] * scale)
window_height = int(image.shape[0] * scale)

# Bild auf Bildschirmgröße skalieren
image = cv2.resize(image, (window_width, window_height))


# Konvertiere das Bild in den HSV-Farbraum, um Farben leichter zu erkennen
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Rote Kugeln - zwei Bereiche definieren, um das ganze Rot-Spektrum abzudecken

# Höherer Bereich für Rot
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])
mask_red = cv2.inRange(hsv_image, lower_red2, upper_red2)

# Blaue Kugeln mit begrenzter Helligkeit und hoher Sättigung
lower_blue = np.array([100, 200, 50])
upper_blue = np.array([140, 255, 200])
mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

# Finde die Konturen der roten Kugeln
contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
red_dots_count = 0
for contour in contours_red:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    if radius > 10:  # Filtere kleine Objekte aus
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 0, 255), 2)  # Zeichne rote Umrandung für rote Kugeln
        red_dots_count += 1

# Finde die Konturen der blauen Kugeln
contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
blue_dots_count = 0
for contour in contours_blue:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    if radius > 10:
        cv2.circle(image, (int(x), int(y)), int(radius), (255, 0, 0), 2)  # Zeichne blaue Umrandung für blaue Kugeln
        blue_dots_count += 1

print("Rote Punkte: ", red_dots_count)
print("Blaue Punkte: ", blue_dots_count)
print("Insgesamt: ", red_dots_count + blue_dots_count)

# Zeige das Ergebnisbild
cv2.imshow("Erkannte Kugeln", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
