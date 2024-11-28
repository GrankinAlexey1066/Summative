import cv2
import mediapipe as mp
import numpy as np
import pygame


def get_points(landmark, shape):
    points = []
    for mark in landmark:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    return np.array(points, dtype=np.int32)


def palm_size(landmark, shape):
    x1, y1 = landmark[0].x * shape[1], landmark[0].y * shape[0]
    x2, y2 = landmark[5].x * shape[1], landmark[5].y * shape[0]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
count = 0
prev_fist = False

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700


class PygameFacade:
    def __init__(self, screen_size, caption='Helltaker'):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def draw_circle(self, x, y, color, radius):
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def update_screen(self):
        pygame.display.flip()

    def clear_screen(self, colour=(0, 0, 0)):
        self.screen.fill(colour)

    def handle_events(self):
        # Если вы хотите использовать возможности событийного управления Pygame
        # (например, обработку нажатий клавиш, мыши и т.д.),
        # то так делать не рекомендуется!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


pygame_facade = PygameFacade((SCREEN_WIDTH, SCREEN_HEIGHT), "Helltaker")

x, y, x1, y1=0, 0, 0, 0
Player = [0, 0]
Level1=[[[8, 8, 8, 8, 0, 0, 8], [8, 0, 0, 2, 0, 0, 8], [8, 0, 2, 0, 2, 8, 8], [0, 0, 8, 8, 8, 8, 8], [0, 1, 0, 0, 1, 0, 8], [0, 1, 0, 1, 0, 9, 9]]]
Level1Img="helltaker1.png"
def check_move():
    global cap
    global count
    global prev_fist
    global x1
    global y1
    global x
    global y
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        cv2.drawContours(flippedRGB, [get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)], 0,
                         (255, 0, 0), 2)
        (x, y), r = cv2.minEnclosingCircle(get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape))
        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        if 2 * r / ws > 1.3:
            cv2.circle(flippedRGB, (int(x), int(y)), int(r), (0, 0, 255), 2)
            prev_fist = False
        else:
            cv2.circle(flippedRGB, (int(x), int(y)), int(r), (0, 255, 0), 2)
            if not prev_fist:
                count += 1
                prev_fist = True
        if prev_fist==True and (abs(int(x)-int(x1))>=150 or abs(int(y)-int(y1))>=150):
            print(int(x)-int(x1), int(y)-int(y1))
        x1=x
        y1=y


def move_player():
    return


while (cap.isOpened()):
    check_move()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    pygame_facade.handle_events()
    pygame_facade.clear_screen()
    pygame_facade.update_screen()
    pygame_facade.clock.tick(30)
handsDetector.close()
