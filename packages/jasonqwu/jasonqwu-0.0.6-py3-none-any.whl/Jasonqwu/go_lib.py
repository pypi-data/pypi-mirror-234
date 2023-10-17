import pygame
from pygame.locals import *
from sys import exit

FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
EIGHT_NEIGH = list(FOUR_NEIGH.values()) + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
DIRECTION = {pygame.K_UP: "up", pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}

ROWS = 15
SIDE = 30

LEFT_SIDE = 30
BOTTOM_SIDE = 30
SCREEN_WIDTH = LEFT_SIDE + ROWS * SIDE
SCREEN_HEIGHT = ROWS * SIDE + BOTTOM_SIDE
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
game_size=(ROWS,ROWS)
cube_height=screen_size[0]/game_size[0]
cube_width=screen_size[1]/game_size[1]
chess_vec=[[],[]]
candidate_pos_list=[[],[]]
real_candidate_list=[]
pos_dic={}

EMPTY = -1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]

def hex2rgb(color):
    b = color % 256
    color = color >> 8
    g = color % 256
    color = color >> 8
    r = color % 256
    return (r, g, b)

class Go:
    def __init__(self, title, size, fps=30):
        self.size = size
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(title)
        self.keys = {}
        self.keys_up = {}
        self.clicks = {}
        self.timer = pygame.time.Clock()
        self.fps = fps
        self.score = 0
        self.end = False
        self.fullscreen = False
        self.last_time = pygame.time.get_ticks()
        self.is_pause = False
        self.is_draw = True
        self.text_font = pygame.font.SysFont("Calibri", 20, True)
        # self.crunch_sound = pygame.mixer.Sound("xxx.wav")

    def __del__(self):
        pygame.quit()

    def bind_key(self, key, action):
        if isinstance(key, list):
            for k in key:
                self.keys[k] = action
        elif isinstance(key, int):
            self.keys[key] = action

    def bind_key_up(self, key, action):
        if isinstance(key, list):
            for k in key:
                self.keys_up[k] = action
        elif isinstance(key, int):
            self.keys_up[key] = action

    def bind_click(self, button, action):
        self.clicks[button] = action

    def pause(self, key):
        self.is_pause = not self.is_pause

    def set_fps(self, fps):
        self.fps = fps

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys.keys():
                self.keys[event.key](event.key)
            if event.key == pygame.K_F11:                           # F11全屏
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN, 32)
                else:
                    self.screen = pygame.display.set_mode(self.size, 0, 32)
        if event.type == pygame.KEYUP:
            if event.key in self.keys_up.keys():
                self.keys_up[event.key](event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.clicks.keys():
                self.clicks[event.button](*event.pos)

    def run(self):
        DEPTH=2
        for i in range(game_size[0]):
            for j in range(game_size[1]):
                a_pos=one_pos(i,j)
                pos_dic[(i,j)]=a_pos
        turn=0
        win_lab=0
        while True:
            if win_lab==0:
                l=0
                if turn==0 and pygame.mouse.get_pressed()[0]:
                    l=1
                    pos=pygame.mouse.get_pos()
                    pos_=(int(pos[1]/cube_height),int(pos[0]/cube_width))
                if turn==1:
                    l=1
                    pos_=AI_choice(1,DEPTH)
                    if pos_==-1:
                        turn=(turn+1)%2
                        l=0
                if l==1:
                    if pos_dic[pos_].occupied==0:
                        chess_vec[turn].append(pos_)
                        win_detect=pos_dic[pos_].occupy(turn+1)
                        print(evaluate(1))
                        if win_detect>0:
                            print('player',turn+1,' win')
                            win_lab=1
                        turn=(turn+1)%2
            for event in pygame.event.get():
                quit = self.handle_input(event)
            if quit:
                break
            self.timer.tick(self.fps)

            self.update(pygame.time.get_ticks())
            self.draw(pygame.time.get_ticks())

    def draw_text(self, text, color, rect=None):
        show_text = self.text_font.render(text, True, color)
        if rect is None:
            r = self.screen.get_rect()
            rect = show_text.get_rect(center=r.center)
        self.screen.blit(show_text, rect)

    def is_end(self):
        return self.end

    def update(self, current_time):
        pass

    def draw(self, current_time):
        # self.draw_score("red")
        pass
    
    def play_crunch_sound(self):
        self.crunch_sound.play()

class Gomoku(Go):
    def __init__(self, title, size, fps=15):
        super(Gomoku, self).__init__(title, size, fps)
        self.board = [[EMPTY for i in range(ROWS + 1)] for j in range(ROWS + 1)]
        self.select = (-1, -1)
        self.black = True
        self.draw_board()
        self.bind_click(1, self.click)

    def click(self, x, y):
        # print(x, y)
        if self.end:
            return
        i, j = y // SIDE, x // SIDE
        if self.board[i][j] != EMPTY or i == ROWS or j == 0:
            return
        self.board[i][j] = BLACK if self.black else WHITE
        self.draw_chess(self.board[i][j], i, j)
        self.black = not self.black

        win = self.check_win()
        if win != None:
            self.end = True
            i, j = win[0]
            winer = "Black"
            if self.board[i][j] == WHITE:
                winer = "White"
            pygame.display.set_caption("五子棋 ---- %s win!" % (winer))
            for c in win:
                i, j = c
                self.draw_chess((100, 255, 255), i, j)
                self.timer.tick(5)

    def check_win(self):
        for i in range(ROWS):
            for j in range(ROWS):
                win = self.check_chess(i, j)
                if win != None:
                    return win
        return None

    def check_chess(self, i, j):
        if self.board[i][j] == EMPTY:
            return None
        color = self.board[i][j]
        for dire in DIRE:
            x, y = i, j
            chess = []
            while self.board[x][y] == color:
                chess.append((x, y))
                x, y = x+dire[0], y+dire[1]
                if x < 0 or y < 0 or x >= ROWS or y >= ROWS:
                    break
            if len(chess) >= 5:
                return chess
        return None

    def draw_chess(self, color, i, j):
        center = (j*SIDE+SIDE//2, i*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, color, center, SIDE//2-2)
        pygame.display.update(pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE))

    def draw_board(self):
        self.screen.fill((139, 87, 66))
        for i in range(ROWS):
            start = ((i + 1)*SIDE + SIDE//2, SIDE//2)
            end = ((i + 1)*SIDE + SIDE//2, ROWS*SIDE - SIDE//2)
            pygame.draw.line(self.screen, 0x000000, start, end)
            start = (ROWS + SIDE, i*SIDE + SIDE//2)
            end = ((ROWS + 1)*SIDE - SIDE//2, i*SIDE + SIDE//2)
            pygame.draw.line(self.screen, 0x000000, start, end)
        star1 = (4*SIDE+SIDE//2, 3*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), star1, 4)
        star2 = (4*SIDE+SIDE//2, (ROWS-4)*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), star2, 4)
        star3 = ((ROWS-3)*SIDE+SIDE//2, 3*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), star3, 4)
        star4 = ((ROWS-3)*SIDE+SIDE//2, (ROWS-4)*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), star4, 4)
        center = (((ROWS + 1)//2)*SIDE+SIDE//2, (ROWS//2)*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), center, 4)
        text = "ABCDEFGHIJKLMNO"
        for i in range(15):
            self.draw_text(text[i], (0, 0, 0), ((i + 1)*SIDE+SIDE//2, (ROWS - 1)*SIDE+SIDE, 10, 10))
        for i in range(15):
            self.draw_text(str(i+1), (0, 0, 0), (SIDE//2, i*SIDE+SIDE//2, 10, 10))
        pygame.display.update()

class ShowGo(Gomoku):
    def __init__(self, title, size, fps=30):
        super(ShowGo, self).__init__(title, size, fps)
        self.bind_key(pygame.K_SPACE, self.press_space)
        self.bind_key(pygame.K_RETURN, self.press_enter)

    def press_enter(self, key):
        print("press enter.")

    def press_space(self, key):
        print("press space.")

class one_pos():
    def __init__(self,pos_x,pos_y):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.pos=(pos_x,pos_y)
        self.occupied=0
        self.from_count=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        self.blocked=[[0,0,0,0],[0,0,0,0]]
        self.neighbor_pos=[(pos_x,pos_y+1),(pos_x+1,pos_y+1),(pos_x+1,pos_y),(pos_x+1,pos_y-1),(pos_x,pos_y-1),(pos_x-1,pos_y-1),(pos_x-1,pos_y),(pos_x-1,pos_y+1)]
    def occupy(self,occupied):
        self.occupied=occupied
        for i in [0,1]:
            if self.pos in candidate_pos_list[i]:
                candidate_pos_list[i].remove(self.pos)
        if self.pos in real_candidate_list:
            real_candidate_list.remove(self.pos)
        for i in range(8):
            if self.neighbor_pos[i][0]>=0 and self.neighbor_pos[i][0]<game_size[0] and self.neighbor_pos[i][1]>=0 and self.neighbor_pos[i][1]<game_size[1]:
                count_sum=self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]+1
                if pos_dic[self.neighbor_pos[i]].occupied==0:
                    pos_dic[self.neighbor_pos[i]].from_count[occupied-1][i]=count_sum
                    if self.neighbor_pos[i] not in candidate_pos_list[occupied-1]:
                        candidate_pos_list[occupied-1].append(self.neighbor_pos[i])
                if pos_dic[self.neighbor_pos[i]].occupied==occupied:
                    dt_x=self.neighbor_pos[i][0]-self.pos_x
                    dt_y=self.neighbor_pos[i][1]-self.pos_y
                    for j in range(2,max(game_size[0],game_size[1])):
                        temp_pos=(self.pos_x+j*dt_x,self.pos_y+j*dt_y)
                        if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
                            break 
                        if pos_dic[temp_pos].occupied==occupied:
                            continue
                        if pos_dic[temp_pos].occupied==0:                           
                            pos_dic[temp_pos].from_count[occupied-1][i]=count_sum
                        break
        for i in range(4):
            if self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]>=4:
                return occupied
        return -1

def click(x, y):
    print(x, y)

def main():
    print(hex2rgb(0xfcf040))
    game = ShowGo("game", (640, 480))
    # game.bind_key(pygame.K_SPACE, press_space)
    game.bind_click(1, click)
    game.run()
    del game
    exit()

if __name__ == '__main__':
    main()
