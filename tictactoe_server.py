import pygame
import socket
from pygame.locals import *
pygame.init()
import time
WIDTH=500
HEIGHT=500
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("0.0.0.0",1234))
s.listen(10)
window=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sever Python Game")

pygame.mixer.init()


def print_board():
    for i in d:
        print(i, ":", d[i], end=' ')
        if i == 3 or i == 6:
            print()
    print()


def show_x():
    time.sleep(0.5)
    #win.play()
    screen.fill(black)
    show_text('X win.', int(width / 2.5), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


def show_o():
    time.sleep(0.5)
    #win.play()
    screen.fill(black)
    show_text('O win.', int(width / 2.5), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


def show_Tie():
    time.sleep(0.5)
    #tie.play()
    screen.fill(black)
    show_text('Tie. Game Over', int(width / 4), int(height / 3), green, 60)
    pygame.display.update()
    time.sleep(5)
    global done
    done = False


# Check for any winning combination
def checkwin():
    # Checking Each Row for X
    if d[3] == d[1] == d[2] == 'X' or d[6] == d[4] == d[5] == 'X' or d[9] == d[7] == d[8] == 'X':
        show_x()
    # Checking Each Row for O
    elif d[3] == d[1] == d[2] == 'O' or d[6] == d[4] == d[5] == 'O' or d[9] == d[7] == d[8] == 'O':
        show_o()
    # Checking Each Column for X
    elif d[1] == d[4] == d[7] == 'X' or d[2] == d[5] == d[8] == 'X' or d[1] == d[3] == d[9] == 'X':
        show_x()
    # Checking Diagonals for X
    elif d[1] == d[5] == d[9] == 'X' or d[3] == d[5] == d[7] == 'X':
        show_x()
    # Checking Each Column for O
    elif d[3] == d[6] == d[9] == 'O' or d[1] == d[4] == d[7] == 'O' or d[2] == d[5] == d[8] == 'O':
        show_o()
    # Checking Diagonals for O
    elif d[1] == d[5] == d[9] == 'O' or d[3] == d[5] == d[7] == 'O':
        show_o()


def show_text(msg, x, y, color, s):
    fontobj = pygame.font.SysFont("times.ttf", s)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


def get_input(p, x):
    print("Player ", p, ". You are X. Please choose the box ! choose and empty box")

    if d[x] == '_':
        d[x] = p
    checkwin()
    print_board()


def drawX(box_x, box_y):
    pygame.draw.line(screen, blue, (box_x, box_y), (box_x + int(width / 3), box_y + int(height / 3)), 1)
    pygame.draw.line(screen, blue, (box_x + int(width / 3), box_y), (box_x, box_y + int(height / 3)), 1)


def drawO(box_x, box_y):
    pygame.draw.ellipse(screen, green, (box_x, box_y, int(width / 3), int(height / 3)), 1)


def checkboard():
    pygame.draw.rect(screen,white,(int(width/3),0,int(width/3),height),1)
    pygame.draw.rect(screen,white,(0,int(height/3),width,int(height/3)),1)


d = {-1:'_',1: '_', 2: '_', 3: '_', 4: '_', 5: '_', 6: '_', 7: '_', 8: '_', 9: '_'}
count = 0
# x=0
# done=0
# L=['X','O']

width = 900
height = 600
screen = pygame.display.set_mode((width, height))
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

#win = pygame.mixer.Sound('win.wav')
#tie = pygame.mixer.Sound('glass_ping.wav')

pygame.draw.rect(screen, white, (int(width / 3), 0, int(width / 3), height), 1)
pygame.draw.rect(screen, white, (0, int(height / 3), width, int(height / 3)), 1)
count = 9

client, client_address = s.accept()

print_board()
done = True
count = 0
player ='o'
turnx, turno = 'x','o'
num= -1
x,y=-300,-200
while done:
    checkwin()
    print(num, turnx, turno)
    if count == 9:
        show_Tie()

    if turnx =='x':

        for event in pygame.event.get():

            if event.type == QUIT:
                done = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos= event.pos
                x = pos[0] - pos[0] % int(width / 3)
                y = pos[1] - pos[1] % int(height / 3)
                client.sendall((str(x) + ',' + str(y)).encode())
                num = int(x / int(width / 3)) + int(y / int(height / 3)) * 3 + 1
                turnx, turno = turno, turnx
                if d[num]=='_':
                    drawX(x, y)
                    d[num]="X"

                    count += 1
                #print(x,y)
                #print('player',player)

    elif turnx == 'o':
        data = client.recv(1024).decode()

        data = data.split(',')
        # print(data)
        x = int(data[0])
        y = int(data[1])
        num = int(x / int(width / 3)) + int(y / int(height / 3)) * 3 + 1
        turnx, turno = turno, turnx
        if d[num] == '_':

            d[num] = 'O'
            drawO(x, y)

            count += 1




    # checkboard()

    checkwin()
    pygame.display.update()
pygame.quit()


