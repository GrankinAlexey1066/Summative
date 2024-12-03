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
Player = [2, 10, 23]
Level1=[[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]
Level1Img=pygame.image.load("helltaker1.png")
Level1Offset=[1, 4]
Rocks=[[6, 6], [7, 6], [7, 8], [6, 9]]
Enemies=[[4, 7], [3, 8], [4, 9]]
PlayerImg=pygame.image.load("ht_passive.png")
EnemyImg=pygame.image.load("enemy_ht.png")
RockImg=pygame.image.load("rock_ht.png")
PlayerImg=pygame.transform.scale(PlayerImg, (70, 70))
EnemyImg=pygame.transform.scale(EnemyImg, (70, 70))
RockImg=pygame.transform.scale(RockImg, (70, 70))

def Move_Object(ObjectInfo, LevelData, LevelOffset):
    global Rocks
    global Enemies
    if ObjectInfo[1]==3:
        if LevelData[ObjectInfo[2][0]-LevelOffset[0]][ObjectInfo[2][1]-1-LevelOffset[1]]==0:
            for rock in Rocks:
                if ObjectInfo[2][0]==rock[0] and ObjectInfo[2][1]-1==rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0]==enemy[0] and ObjectInfo[2][1]-1==enemy[1]:
                    return
            if ObjectInfo[0]==1:
                Rocks[ObjectInfo[-1]]=[ObjectInfo[2][0], ObjectInfo[2][1]-1]
            else:
                Enemies[ObjectInfo[-1]]=[ObjectInfo[2][0], ObjectInfo[2][1]-1]
        elif ObjectInfo[0]==2:
            Enemies=Enemies[:ObjectInfo[-1]]+Enemies[ObjectInfo[-1]+1:]
    if ObjectInfo[1]==1:
        if LevelData[ObjectInfo[2][0]-LevelOffset[0]][ObjectInfo[2][1]+1-LevelOffset[1]]==0:
            for rock in Rocks:
                if ObjectInfo[2][0]==rock[0] and ObjectInfo[2][1]+1==rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0]==enemy[0] and ObjectInfo[2][1]+1==enemy[1]:
                    return
            if ObjectInfo[0]==1:
                Rocks[ObjectInfo[-1]]=[ObjectInfo[2][0], ObjectInfo[2][1]+1]
            else:
                Enemies[ObjectInfo[-1]]=[ObjectInfo[2][0], ObjectInfo[2][1]+1]
        elif ObjectInfo[0]==2:
            Enemies=Enemies[:ObjectInfo[-1]]+Enemies[ObjectInfo[-1]+1:]
    if ObjectInfo[1]==0:
        if LevelData[ObjectInfo[2][0]-1-LevelOffset[0]][ObjectInfo[2][1]-LevelOffset[1]]==0:
            for rock in Rocks:
                if ObjectInfo[2][0]-1==rock[0] and ObjectInfo[2][1]==rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0]-1==enemy[0] and ObjectInfo[2][1]==enemy[1]:
                    return
            if ObjectInfo[0]==1:
                Rocks[ObjectInfo[-1]]=[ObjectInfo[2][0]-1, ObjectInfo[2][1]]
            else:
                Enemies[ObjectInfo[-1]]=[ObjectInfo[2][0]-1, ObjectInfo[2][1]]
        elif ObjectInfo[0]==2:
            Enemies=Enemies[:ObjectInfo[-1]]+Enemies[ObjectInfo[-1]+1:]
    if ObjectInfo[1]==2:
        if LevelData[ObjectInfo[2][0]+1-LevelOffset[0]][ObjectInfo[2][1]-LevelOffset[1]]==0:
            for rock in Rocks:
                if ObjectInfo[2][0]+1==rock[0] and ObjectInfo[2][1]==rock[1]:
                    return
            for enemy in Enemies:
                if ObjectInfo[2][0]+1==enemy[0] and ObjectInfo[2][1]==enemy[1]:
                    return
            if ObjectInfo[0]==1:
                Rocks[ObjectInfo[-1]]=[ObjectInfo[2][0]+1, ObjectInfo[2][1]]
            else:
                Enemies[ObjectInfo[-1]]=[ObjectInfo[2][0]+1, ObjectInfo[2][1]]
        elif ObjectInfo[0]==2:
            Enemies=Enemies[:ObjectInfo[-1]]+Enemies[ObjectInfo[-1]+1:]
def Check_Clean(k):
    global Rocks
    global Enemies
    number=0
    if k==3:
        for rock in Rocks:
            if Player[0]==rock[0] and Player[1]-1==rock[1]:
                return (1, k, rock, number)
            number+=1
        number = 0
        for enemy in Enemies:
            if Player[0]==enemy[0] and Player[1]-1==enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k==1:
        for rock in Rocks:
            if Player[0]==rock[0] and Player[1]+1==rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0]==enemy[0] and Player[1]+1==enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k==0:
        for rock in Rocks:
            if Player[0]-1==rock[0] and Player[1]==rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0]-1==enemy[0] and Player[1]==enemy[1]:
                return (2, k, enemy, number)
            number += 1
    if k==2:
        for rock in Rocks:
            if Player[0]+1==rock[0] and Player[1]==rock[1]:
                return (1, k, rock, number)
            number += 1
        number = 0
        for enemy in Enemies:
            if Player[0]+1==enemy[0] and Player[1]==enemy[1]:
                return (2, k, enemy, number)
            number += 1
    return 0
def PlayerMove(k, LevelData, LevelOffset):
    global Player
    if k==3 and LevelData[Player[0]-LevelOffset[0]][Player[1]-1-LevelOffset[1]]!=1 and Check_Clean(k)==0:
        Player[1]-=1
        return
    elif k==1 and LevelData[Player[0]-LevelOffset[0]][Player[1]+1-LevelOffset[1]]!=1 and Check_Clean(k)==0:
        Player[1]+=1
        return
    elif k==0 and LevelData[Player[0]-1-LevelOffset[0]][Player[1]-LevelOffset[1]]!=1 and Check_Clean(k)==0:
        Player[0]-=1
        return
    elif k==2 and LevelData[Player[0]+1-LevelOffset[0]][Player[1]-LevelOffset[1]]!=1 and Check_Clean(k)==0:
        Player[0]+=1
        return
    elif Check_Clean(k)!=0:
        Move_Object(Check_Clean(k), LevelData, LevelOffset)
def check_move():
    global cap
    global count
    global prev_fist
    global x1
    global y1
    global x
    global y
    sensitivity=100
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
            prev_fist = False
        else:
            if not prev_fist:
                count += 1
                prev_fist = True
        if prev_fist==True and (abs(int(x)-int(x1))>=sensitivity or abs(int(y)-int(y1))>=(sensitivity/2)):
            if int(x)-int(x1)<=-sensitivity:
                return 3
            elif int(x)-int(x1)>=sensitivity:
                return 1
            elif int(y)-int(y1)<=-(sensitivity/5*3):
                return 0
            else:
                return 2

while (cap.isOpened()):
    k=check_move()
    x1 = x
    y1 = y
    pygame_facade.screen.blit(Level1Img, (0, 0))
    pygame_facade.screen.blit(PlayerImg, (Player[1]*77+10, Player[0]*77+5))
    for enemy in Enemies:
        pygame_facade.screen.blit(EnemyImg, (enemy[1] * 77 + 10, enemy[0] * 77 + 5))
    for rock in Rocks:
        pygame_facade.screen.blit(RockImg, (rock[1] * 77 + 10, rock[0] * 77 + 5))
    if k!=None:
        PlayerMove(k, Level1, Level1Offset)
    if Player[0]==7 and Player[1]==11:
        break
    pygame_facade.update_screen()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    pygame_facade.handle_events()
    pygame_facade.clock.tick(30)
handsDetector.close()
