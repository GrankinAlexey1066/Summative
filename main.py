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

x, y, x1, y1 = 0, 0, 0, 0
Player = [2, 10, 24]
Level1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0, 0, 1, 1],
          [1, 1, 0, 0, 0, 0, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]
Level1Img = pygame.image.load("helltaker1.png")
Level1Offset = [1, 4]
Rocks = [[6, 6], [7, 6], [7, 8], [6, 9]]
Enemies = [[4, 7], [3, 8], [4, 9]]
PlayerImg = pygame.image.load("ht_passive.png")
EnemyImg = pygame.image.load("enemy_ht.png")
RockImg = pygame.image.load("rock_ht.png")
PlayerImg = pygame.transform.scale(PlayerImg, (70, 70))
EnemyImg = pygame.transform.scale(EnemyImg, (70, 70))
RockImg = pygame.transform.scale(RockImg, (70, 70))
TimeSinceMovement = 0
TimeUntilSelection = 300
sensitivity=100
font = pygame.font.Font('freesansbold.ttf', 32)


def write_text(text_string, x, y):
    text = font.render(text_string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (x, y)
    pygame_facade.screen.blit(text, textRect)

def Move_Object(ObjectInfo, LevelData, LevelOffset):
    global Rocks
    global Enemies
    if ObjectInfo[1] == 3:
        if LevelData[ObjectInfo[2][0] - LevelOffset[0]][ObjectInfo[2][1] - 1 - LevelOffset[1]] == 0:
            for rock in Rocks:
                if ObjectInfo[2][0] == rock[0] and ObjectInfo[2][1] - 1 == rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0] == enemy[0] and ObjectInfo[2][1] - 1 == enemy[1]:
                    return
            if ObjectInfo[0] == 1:
                Rocks[ObjectInfo[-1]] = [ObjectInfo[2][0], ObjectInfo[2][1] - 1]
            else:
                Enemies[ObjectInfo[-1]] = [ObjectInfo[2][0], ObjectInfo[2][1] - 1]
        elif ObjectInfo[0] == 2:
            Enemies = Enemies[:ObjectInfo[-1]] + Enemies[ObjectInfo[-1] + 1:]
    if ObjectInfo[1] == 1:
        if LevelData[ObjectInfo[2][0] - LevelOffset[0]][ObjectInfo[2][1] + 1 - LevelOffset[1]] == 0:
            for rock in Rocks:
                if ObjectInfo[2][0] == rock[0] and ObjectInfo[2][1] + 1 == rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0] == enemy[0] and ObjectInfo[2][1] + 1 == enemy[1]:
                    return
            if ObjectInfo[0] == 1:
                Rocks[ObjectInfo[-1]] = [ObjectInfo[2][0], ObjectInfo[2][1] + 1]
            else:
                Enemies[ObjectInfo[-1]] = [ObjectInfo[2][0], ObjectInfo[2][1] + 1]
        elif ObjectInfo[0] == 2:
            Enemies = Enemies[:ObjectInfo[-1]] + Enemies[ObjectInfo[-1] + 1:]
    if ObjectInfo[1] == 0:
        if LevelData[ObjectInfo[2][0] - 1 - LevelOffset[0]][ObjectInfo[2][1] - LevelOffset[1]] == 0:
            for rock in Rocks:
                if ObjectInfo[2][0] - 1 == rock[0] and ObjectInfo[2][1] == rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0] - 1 == enemy[0] and ObjectInfo[2][1] == enemy[1]:
                    return
            if ObjectInfo[0] == 1:
                Rocks[ObjectInfo[-1]] = [ObjectInfo[2][0] - 1, ObjectInfo[2][1]]
            else:
                Enemies[ObjectInfo[-1]] = [ObjectInfo[2][0] - 1, ObjectInfo[2][1]]
        elif ObjectInfo[0] == 2:
            Enemies = Enemies[:ObjectInfo[-1]] + Enemies[ObjectInfo[-1] + 1:]
    if ObjectInfo[1] == 2:
        if LevelData[ObjectInfo[2][0] + 1 - LevelOffset[0]][ObjectInfo[2][1] - LevelOffset[1]] == 0:
            for rock in Rocks:
                if ObjectInfo[2][0] + 1 == rock[0] and ObjectInfo[2][1] == rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0] + 1 == enemy[0] and ObjectInfo[2][1] == enemy[1]:
                    return
            if ObjectInfo[0] == 1:
                Rocks[ObjectInfo[-1]] = [ObjectInfo[2][0] + 1, ObjectInfo[2][1]]
            else:
                Enemies[ObjectInfo[-1]] = [ObjectInfo[2][0] + 1, ObjectInfo[2][1]]
        elif ObjectInfo[0] == 2:
            Enemies = Enemies[:ObjectInfo[-1]] + Enemies[ObjectInfo[-1] + 1:]


def Check_Clean(k):
    global Rocks
    global Enemies
    number = 0
    if k == 3:
        for rock in Rocks:
            if Player[0] == rock[0] and Player[1] - 1 == rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0] == enemy[0] and Player[1] - 1 == enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k == 1:
        for rock in Rocks:
            if Player[0] == rock[0] and Player[1] + 1 == rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0] == enemy[0] and Player[1] + 1 == enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k == 0:
        for rock in Rocks:
            if Player[0] - 1 == rock[0] and Player[1] == rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0] - 1 == enemy[0] and Player[1] == enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k == 2:
        for rock in Rocks:
            if Player[0] + 1 == rock[0] and Player[1] == rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0] + 1 == enemy[0] and Player[1] == enemy[1]:
                return (2, k, enemy, number)
            number += 1
    return 0


def PlayerMove(k, LevelData, LevelOffset):
    global Player
    global TimeSinceMovement
    TimeSinceMovement = 30
    if k == 3 and LevelData[Player[0] - LevelOffset[0]][Player[1] - 1 - LevelOffset[1]] != 1 and Check_Clean(k) == 0:
        Player[1] -= 1
        return
    elif k == 1 and LevelData[Player[0] - LevelOffset[0]][Player[1] + 1 - LevelOffset[1]] != 1 and Check_Clean(k) == 0:
        Player[1] += 1
        return
    elif k == 0 and LevelData[Player[0] - 1 - LevelOffset[0]][Player[1] - LevelOffset[1]] != 1 and Check_Clean(k) == 0:
        Player[0] -= 1
        return
    elif k == 2 and LevelData[Player[0] + 1 - LevelOffset[0]][Player[1] - LevelOffset[1]] != 1 and Check_Clean(k) == 0:
        Player[0] += 1
        return
    elif Check_Clean(k) != 0:
        Move_Object(Check_Clean(k), LevelData, LevelOffset)


def check_move():
    global cap
    global count
    global prev_fist
    global x1
    global y1
    global x
    global y
    global TimeSinceMovement
    global sensitivity
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        cv2.drawContours(flippedRGB, [get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)], 0,
                         (255, 0, 0), 2)
        (x, y), r = cv2.minEnclosingCircle(get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape))
        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        prev_fist = not (2 * r / ws > 1.3)
        if prev_fist == True and (abs(int(x) - int(x1)) >= sensitivity or abs(int(y) - int(y1)) >= (sensitivity / 2)):
            if int(x) - int(x1) <= -sensitivity:
                return 3
            elif int(x) - int(x1) >= sensitivity:
                return 1
            elif int(y) - int(y1) <= -(sensitivity / 2):
                return 0
            elif int(y) - int(y1) >= sensitivity / 2:
                return 2
            else:
                return
        res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
        cv2.imshow("Hands", res_image)


MenuSelection = 0
SensitivitySelection = 2
pygame_facade.clear_screen((63, 0, 0))


# menu and settings
def menu(TimeUntilSelection, TimeSinceMovement):
    global MenuSelection
    global pygame_facade
    global x1
    global y1
    global x
    global y
    while True:
        k = check_move()
        x1 = x
        y1 = y
        if MenuSelection <= 1 and k == 2 and TimeSinceMovement<=0:
            MenuSelection += 1
            TimeSinceMovement = 30
            TimeUntilSelection = 300
        elif MenuSelection >= 1 and k == 0 and TimeSinceMovement<=0:
            MenuSelection -= 1
            TimeSinceMovement = 30
            TimeUntilSelection = 300
        if MenuSelection == 0:
            pygame_facade.draw_rectangle(550, 175, 300, 75, (255, 0, 0))
            pygame_facade.draw_rectangle(550, 300, 300, 75, (127, 0, 0))
            pygame_facade.draw_rectangle(550, 425, 300, 75, (127, 0, 0))
        elif MenuSelection == 1:
            pygame_facade.draw_rectangle(550, 175, 300, 75, (127, 0, 0))
            pygame_facade.draw_rectangle(550, 300, 300, 75, (255, 0, 0))
            pygame_facade.draw_rectangle(550, 425, 300, 75, (127, 0, 0))
        else:
            pygame_facade.draw_rectangle(550, 175, 300, 75, (127, 0, 0))
            pygame_facade.draw_rectangle(550, 300, 300, 75, (127, 0, 0))
            pygame_facade.draw_rectangle(550, 425, 300, 75, (255, 0, 0))
        if TimeSinceMovement > 0:
            TimeSinceMovement -= 1
        TimeUntilSelection -= 1
        if TimeUntilSelection <= 0:
            if MenuSelection == 0:
                return
            elif MenuSelection == 1:
                sensitivity_setting()
        pygame_facade.update_screen()
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        pygame_facade.handle_events()
        pygame_facade.clock.tick(30)


def sensitivity_setting():
    global SensitivitySelection
    global sensitivity
    global pygame_facade
    global x1
    global y1
    global x
    global y
    pygame_facade.clear_screen((63, 0, 0))
    TimeUntilSelection=300
    TimeSinceMovement=0
    while True:
        sensitivity=SensitivitySelection*20+60
        write_text("Sensitivity Selection", 700, 150)
        write_text(f"Time Until Selection: {(TimeUntilSelection-1)//30+1}", 700, 225)
        check_move()
        k = check_move()
        x1 = x
        y1 = y
        if SensitivitySelection <= 3 and k == 1 and TimeSinceMovement<=0:
            SensitivitySelection += 1
            TimeSinceMovement = 30
            TimeUntilSelection = 300
        elif SensitivitySelection >= 1 and k == 3 and TimeSinceMovement<=0:
            SensitivitySelection -= 1
            TimeSinceMovement = 30
            TimeUntilSelection = 300
        pygame_facade.draw_rectangle(100, 300, 200, 100, (127, 0, 0))
        pygame_facade.draw_rectangle(350, 300, 200, 100, (127, 0, 0))
        pygame_facade.draw_rectangle(600, 300, 200, 100, (127, 0, 0))
        pygame_facade.draw_rectangle(850, 300, 200, 100, (127, 0, 0))
        pygame_facade.draw_rectangle(1100, 300, 200, 100, (127, 0, 0))
        pygame_facade.draw_rectangle(100+SensitivitySelection*250, 300, 200, 100, (255, 0, 0))
        write_text("Very High", 200, 350)
        write_text("High", 450, 350)
        write_text("Normal", 700, 350)
        write_text("Low", 950, 350)
        write_text("Very Low", 1200, 350)
        TimeUntilSelection-=1
        if TimeUntilSelection<=0:
            return
        if TimeSinceMovement>0:
            TimeSinceMovement-=1
        pygame_facade.update_screen()
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        pygame_facade.handle_events()
        pygame_facade.clock.tick(30)
        pygame_facade.clear_screen((63, 0, 0))


menu(TimeUntilSelection, TimeSinceMovement)
pygame_facade.clear_screen((0, 0, 0))
# main game cycle
while (cap.isOpened()):
    k = check_move()
    x1 = x
    y1 = y
    pygame_facade.screen.blit(Level1Img, (0, 0))
    pygame_facade.screen.blit(PlayerImg, (Player[1] * 77 + 10, Player[0] * 77 + 5))
    for enemy in Enemies:
        pygame_facade.screen.blit(EnemyImg, (enemy[1] * 77 + 10, enemy[0] * 77 + 5))
    for rock in Rocks:
        pygame_facade.screen.blit(RockImg, (rock[1] * 77 + 10, rock[0] * 77 + 5))
    if TimeSinceMovement > 0:
        TimeSinceMovement -= 1
    elif k != None:
        PlayerMove(k, Level1, Level1Offset)
    if Player[0] == 7 and Player[1] == 11:
        break
    pygame_facade.update_screen()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    pygame_facade.handle_events()
    pygame_facade.clock.tick(30)
handsDetector.close()
