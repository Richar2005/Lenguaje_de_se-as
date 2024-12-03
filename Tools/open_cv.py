import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    # Captura fotograma a fotograma
    ret, frame = cap.read()

    if ret:
        # Captura fotograma a fotograma
        cv2.imshow('frame', frame)
    
        # Exit?
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()