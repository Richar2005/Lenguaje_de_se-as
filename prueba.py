import cv2
import mediapipe as mp
import math

# Inicializar soluciones de Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4, 1080)
def calculate_distance(point1, point2):
    """Calcula la distancia entre dos puntos."""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def is_perfect_gesture(hand_landmarks):
    """Verifica si la mano muestra el gesto 'perfecto'."""
    # Coordenadas del pulgar y del índice
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    # Coordenadas de los demás dedos
    fingers_tips = [hand_landmarks.landmark[i] for i in [12, 16, 20]]
    wrist = hand_landmarks.landmark[0]

    # Condición: Pulgar e índice forman un círculo
    thumb_index_distance = calculate_distance(thumb_tip, index_tip)
    thumb_index_close = thumb_index_distance < 0.05  # Ajusta el umbral según sea necesario

    # Condición: Los demás dedos están extendidos
    fingers_extended = all(finger_tip.y < wrist.y for finger_tip in fingers_tips)

    return thumb_index_close and fingers_extended

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir BGR a RGB para Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detección de manos
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Dibujar los puntos clave de las manos detectadas
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Verificar si el gesto es "perfecto"
                if is_perfect_gesture(hand_landmarks):
                    cv2.putText(image, "Perfecto!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar imagen con puntos clave
        cv2.imshow('Mediapipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Presiona 'ESC' para salir
            break

cap.release()
cv2.destroyAllWindows()
