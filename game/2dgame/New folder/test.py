import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize Mediapipe for hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Naruto Hand Signs Game")
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Function to detect hand sign (example: shadow clone sign)
def detect_shadow_clone_sign(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    return distance < 0.05

# Start video capture
cap = cv2.VideoCapture(0)

# List to store shadow clones
shadow_clones = []

running = True
while running:
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results_hands = hands.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            if detect_shadow_clone_sign(hand_landmarks.landmark):
                # Capture current frame for shadow clone
                clone_image = image.copy()
                clone_image = cv2.resize(clone_image, (200, 150))  # Resize clone image
                shadow_clones.append(clone_image)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display the original image
    cv2.imshow('Hand Detection', image)

    # Pygame game logic
    screen.fill(BLACK)

    # Display shadow clones
    for i, clone in enumerate(shadow_clones):
        clone_surface = pygame.surfarray.make_surface(cv2.flip(clone, 1))
        x_position = 100 + i * 220  # Adjust x position for each clone
        y_position = 200
        screen.blit(clone_surface, (x_position, y_position))

    pygame.display.flip()
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
