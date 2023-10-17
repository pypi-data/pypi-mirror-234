from abc import ABCMeta, abstractmethod
import time
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from collections import namedtuple
import json
import commentjson
import logging_lib


class Constant:
    # 设置常量
    DEPTH = 2         # AI 的级别
    FPS = 30          # 刷新频率
    SIZE = 30         # 棋盘每个点时间的间隔
    LINE_POINTS = 19  # 棋盘每行/每列点数
    OUTER_WIDTH = 20  # 棋盘外宽度
    BORDER_WIDTH = 4  # 边框宽度
    INSIDE_WIDTH = 4  # 边框跟实际的棋盘之间的间隔
    BORDER_LENGTH = SIZE * (LINE_POINTS - 1) \
        + INSIDE_WIDTH * 2 + BORDER_WIDTH       # 边框线的长度
    START_X = START_Y = OUTER_WIDTH \
        + int(BORDER_WIDTH / 2) + INSIDE_WIDTH  # 网格线起点（左上角）坐标
    SCREEN_HEIGHT = SIZE * (LINE_POINTS - 1) \
        + OUTER_WIDTH * 2 + BORDER_WIDTH + INSIDE_WIDTH * 2  # 游戏屏幕的高
    SCREEN_WIDTH = SCREEN_HEIGHT + 200       # 游戏屏幕的宽
    STONE_RADIUS = SIZE // 2 - 3             # 棋子半径
    STONE_INFO_RADIUS = SIZE // 2 + 3        # 棋子信息半径
    OFFSET = [(1, 0), (0, 1), (1, 1), (1, -1)]
    RIGHT_INFO_POS_X = SCREEN_HEIGHT + STONE_INFO_RADIUS * 2 + 10

    # 设置颜色
    CHECKERBOARD_COLOR = (0xE3, 0x92, 0x65)
    BLACK_COLOR = (0, 0, 0)
    WHITE_COLOR = (255, 255, 255)
    RED_COLOR = (200, 30, 30)
    BLUE_COLOR = (30, 30, 200)

    # 设置棋子
    Chessman = namedtuple('Chessman', 'Name Value Color')
    Point = namedtuple('Point', 'X Y')

    BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
    WHITE_CHESSMAN = Chessman('白子', -1, (219, 219, 219))


class Show(metaclass=ABCMeta):
    '''显示方法的抽象接口'''
    @abstractmethod
    def show(self, data):
        pass


class Config(Show):
    def __init__(self, file="config.json"):
        try:
            with open(file, encoding="utf-8") as f:
                content = f.read()
                print(f"content = {content}")
                self.config = commentjson.loads(content)
        except Exception:
            try:
                with open("back_" + file) as f:
                    self.config = json.load(f)
                with open(file, 'w') as f:
                    json.dump(self.config, f, indent=4)
            except Exception:
                print(f"缺少 back_{file} 文件。")
                exit()

    def save(self, data, file="config.json"):
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, file="config.json"):
        with open(file) as f:
            return json.load(f)

    def show(self, data):
        print(json.dumps(data, indent=4))


class Position:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = (pos_x, pos_y)
        self.occupied = 0
        self.from_count = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.blocked = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.neighbor_pos = [
            (pos_x, pos_y + 1),
            (pos_x + 1, pos_y + 1),
            (pos_x + 1, pos_y),
            (pos_x + 1, pos_y - 1),
            (pos_x, pos_y - 1),
            (pos_x - 1, pos_y - 1),
            (pos_x - 1, pos_y),
            (pos_x - 1, pos_y + 1)]


class PositionGroup:
    def __init__(self, pos_dic):
        self.candidate_pos_list = [[], []]
        self.real_candidate_list = []
        self.pos_dic = pos_dic

    def occupy(self, occupied):
        self.occupied = occupied
        for i in [0, 1]:
            if self.pos in self.candidate_pos_list[i]:
                self.candidate_pos_list[i].remove(self.pos)
        if self.pos in self.real_candidate_list:
            self.real_candidate_list.remove(self.pos)
        for i in range(8):
            if self.neighbor_pos[i][0] >= 0 \
                    and self.neighbor_pos[i][0] < Constant.LINE_POINTS \
                    and self.neighbor_pos[i][1] >= 0 \
                    and self.neighbor_pos[i][1] < Constant.LINE_POINTS:
                count_sum = self.from_count[occupied-1][i] \
                    + self.from_count[occupied-1][(i+4) % 8] + 1
                if pos_dic[self.neighbor_pos[i]].occupied == 0:
                    pos_dic[self.neighbor_pos[i]].from_count[occupied-1][i] \
                        = count_sum
                    if self.neighbor_pos[i] \
                            not in candidate_pos_list[occupied-1]:
                        candidate_pos_list[occupied-1].append(
                            self.neighbor_pos[i])
                if pos_dic[self.neighbor_pos[i]].occupied == occupied:
                    dt_x = self.neighbor_pos[i][0] - self.pos_x
                    dt_y = self.neighbor_pos[i][1] - self.pos_y
                    for j in range(2, LINE_POINTS):
                        temp_pos = (
                            self.pos_x + j * dt_x, self.pos_y + j * dt_y)
                        if temp_pos[0] < 0 \
                                or temp_pos[0] >= LINE_POINTS \
                                or temp_pos[1] < 0 \
                                or temp_pos[1] >= LINE_POINTS:
                            break
                        if pos_dic[temp_pos].occupied == occupied:
                            continue
                        if pos_dic[temp_pos].occupied == 0:
                            pos_dic[temp_pos].from_count[occupied-1][i] \
                                = count_sum
                        break
        for i in range(8):
            dt_x = self.neighbor_pos[i][0] - self.pos_x
            dt_y = self.neighbor_pos[i][1] - self.pos_y
            labE = 0
            keep_j = -1
            for j in range(1, 6):
                temp_pos = (self.pos_x + j * dt_x, self.pos_y + j * dt_y)
                if temp_pos[0] < 0 \
                        or temp_pos[0] >= LINE_POINTS \
                        or temp_pos[1] < 0 \
                        or temp_pos[1] >= LINE_POINTS:
                    keep_j = j
                    break
                if pos_dic[temp_pos].occupied == 0:
                    labE = 1
                if labE == 1 and pos_dic[temp_pos].occupied == occupied:
                    keep_j = j
                    break
            if keep_j != -1:
                for j2 in range(1, keep_j):
                    temp_pos2 = (
                        self.pos_x + j2 * dt_x, self.pos_y + j2 * dt_y)
                    if pos_dic[temp_pos2].occupied == 0:
                        pos_dic[temp_pos2].blocked[occupied % 2][i] = 1
                        pos_dic[temp_pos2].blocked[occupied % 2][(i+4) % 8] = 1
        for i in range(4):
            if self.from_count[occupied-1][i] \
                    + self.from_count[occupied-1][(i+4) % 8] >= 4:
                return occupied
        return -1


class Checkerboard:
    def __init__(self, line_points):
        self._line_points = line_points
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def _get_checkerboard(self):
        return self._checkerboard

    checkerboard = property(_get_checkerboard)

    # 判断是否可落子
    def can_drop(self, point):
        return self._checkerboard[point.Y][point.X] == 0

    def drop(self, chessman, point):
        """
        落子
        :param chessman:
        :param point:落子位置
        :return:若该子落下之后即可获胜，则返回获胜方，否则返回 None
        """
        print(f'{chessman.Name} ({point.Y}, {point.X})')
        self._checkerboard[point.Y][point.X] = chessman.Value

        if self._win(point):
            print(f'{chessman.Name}获胜')
            return chessman

    # 判断是否赢了
    def _win(self, point):
        cur_value = self._checkerboard[point.Y][point.X]
        for os in Constant.OFFSET:
            if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                return True

    def _get_count_on_direction(self, point, value, x_offset, y_offset):
        count = 1
        for step in range(1, 5):
            x = point.X + step * x_offset
            y = point.Y + step * y_offset
            if 0 <= x < self._line_points \
                    and 0 <= y < self._line_points \
                    and self._checkerboard[y][x] == value:
                count += 1
            else:
                break
        for step in range(1, 5):
            x = point.X - step * x_offset
            y = point.Y - step * y_offset
            if 0 <= x < self._line_points \
                    and 0 <= y < self._line_points \
                    and self._checkerboard[y][x] == value:
                count += 1
            else:
                break
        return count >= 5


class Computer:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman
        self._opponent = Constant.BLACK_CHESSMAN \
            if chessman == Constant.WHITE_CHESSMAN else Constant.WHITE_CHESSMAN
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def _get_point_score(self, point):
        score = 0
        for os in Constant.OFFSET:
            score += self._get_direction_score(point, os[0], os[1])
        return score

    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0   # 落子处我方连续子数
        _count = 0  # 落子处对方连续子数
        space = None   # 我方连续子中有无空格
        _space = None  # 对方连续子中有无空格
        both = 0    # 我方连续子两端有无阻挡
        _both = 0   # 对方连续子两端有无阻挡

        # 如果是 1 表示是边上是我方子，2 表示敌方子
        flag = self._get_stone_color(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # 遇到第二个空格退出
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # 遇到第二个空格退出
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    def _get_stone_color(self, point, x_offset, y_offset, next):
        '''判断指定位置处在指定方向上是我方子、对方子、空'''
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else:
                if next:
                    return self._get_stone_color(
                        Constant.Point(x, y),
                        x_offset,
                        y_offset,
                        False)
                else:
                    return 0
        else:
            return 0

    def get_opponent_drop(self, point):
        self._checkerboard[point.Y][point.X] = self._opponent.Value

    def drop(self):
        point = None
        score = 0
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(Constant.Point(i, j))
                    if _score > score:
                        score = _score
                        point = Constant.Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Constant.Point(i, j)
        self._checkerboard[point.Y][point.X] = self._my.Value
        return point

    def simu_choice(self, turn, depth, min_lim=100000):
        global candidate_pos_list
        global pos_dic
        global real_candidate_list

        ene_turn = (turn + 1) % 2
        if depth == 0:
            valu = evaluate(turn, turn)
            return (valu, (-1, -1))
        if depth == 1:
            maxi = -100000
            choici_keep = (-1, -1)
            save(candidate_pos_list, pos_dic, real_candidate_list)
            for each in real_candidate_list.copy():
                win_d = pos_dic[each].occupy(turn + 1)
                if win_d > 0:
                    # saved_list.pop()
                    return (10001, each)
                vv = evaluate(turn, ene_turn)
                if vv > maxi:
                    maxi = vv
                    choici_keep = each
                candidate_pos_list, pos_dic, real_candidate_list = load()
            # saved_list.pop()
            return (maxi, choici_keep)
        max_value = -100000
        choice_keep = (-1, -1)
        ene_turn = (turn + 1) % 2
        save(candidate_pos_list, pos_dic, real_candidate_list)
        for each in real_candidate_list.copy():
            win_d = pos_dic[each].occupy(turn + 1)
            if win_d > 0:
                # saved_list.pop()
                return (10001, each)
            for each2 in pos_dic[each].neighbor_pos:
                if each2[0] >= 0 \
                        and each2[0] < LINE_POINTS \
                        and each2[1] >= 0 \
                        and each2[1] < LINE_POINTS:
                    if pos_dic[each2].occupied == 0:
                        for each22 in pos_dic[each2].neighbor_pos:
                            if each22[0] >= 0 \
                                    and each22[0] < LINE_POINTS \
                                    and each22[1] >= 0 \
                                    and each22[1] < LINE_POINTS:
                                if pos_dic[each22].occupied == 0:
                                    if each22 not in real_candidate_list:
                                        real_candidate_list.append(each22)
            save(candidate_pos_list, pos_dic, real_candidate_list)
            min_value = 100000
            jian2 = 0
            for each3 in real_candidate_list:
                win_d2 = pos_dic[each3].occupy(ene_turn + 1)
                if win_d2 > 0:
                    min_value = -10001
                    break
                val2 = self.simu_choice(turn, depth - 2, min_value)[0]
                candidate_pos_list, pos_dic, real_candidate_list = load()
                if val2 == -1000000:
                    continue
                if val2 < max_value:
                    jian2 = 1
                    break
                if val2 < min_value:
                    min_value = val2
            # saved_list.pop()
            candidate_pos_list, pos_dic, real_candidate_list = load()
            if min_value > min_lim:
                # saved_list.pop()
                return (-1000000, (-1, -1))
            if jian2 == 1:
                continue
            if min_value != 100000 and min_value > max_value:
                max_value = min_value
                choice_keep = each
        # saved_list.pop()
        return (max_value, choice_keep)

    def AI_choice(self, turn, depth):
        ene_turn = (1 + turn) % 2
        for t in [turn, ene_turn]:
            for each in candidate_pos_list[t]:
                for i in range(4):
                    if pos_dic[each].from_count[t][i] \
                            + pos_dic[each].from_count[t][(i+4) % 8] >= 4:
                        return each
        real_candidate_list.clear()
        for i in range(2):
            for each in candidate_pos_list[i]:
                if pos_dic[each].occupied == 0:
                    if each not in real_candidate_list:
                        real_candidate_list.append(each)
                    for each2 in pos_dic[each].neighbor_pos:
                        if each2[0] >= 0 \
                                and each2[0] < LINE_POINTS \
                                and each2[1] >= 0 \
                                and each2[1] < LINE_POINTS:
                            if pos_dic[each2].occupied == 0:
                                if each2 not in real_candidate_list:
                                    real_candidate_list.append(each2)
        # print(f"(turn,depth)--{(turn,depth)}")
        s_choice = self.simu_choice(turn, depth)[1]
        # print(f"s_choice--{s_choice}")
        return s_choice


class Game:
    def __init__(self):
        self.log = logging_lib.Logger("log")
        self.chess_vec = [[], []]
        self.pos_dic = {}
        for i in range(Constant.LINE_POINTS):
            for j in range(Constant.LINE_POINTS):
                self.pos_dic[(i, j)] = Position(i, j)
                self.log.show.debug(f"{self.pos_dic[i, j]}")

    def _get_next(self, cur_runner):
        if cur_runner == Constant.BLACK_CHESSMAN:
            return Constant.WHITE_CHESSMAN
        else:
            return Constant.BLACK_CHESSMAN

    def _draw_checkerboard(self, screen, font):
        '''画棋盘'''
        # 填充棋盘背景色
        screen.fill(Constant.CHECKERBOARD_COLOR)
        # 画棋盘网格线外的边框
        pygame.draw.rect(
            screen, Constant.BLACK_COLOR,
            (
                Constant.OUTER_WIDTH, Constant.OUTER_WIDTH,
                Constant.BORDER_LENGTH, Constant.BORDER_LENGTH),
            Constant.BORDER_WIDTH)
        # 画网格线
        for i in range(Constant.LINE_POINTS):
            pygame.draw.line(
                screen, Constant.BLACK_COLOR,
                (Constant.START_Y, Constant.START_Y + Constant.SIZE * i),
                (
                    Constant.START_Y + Constant.SIZE
                    * (Constant.LINE_POINTS - 1),
                    Constant.START_Y + Constant.SIZE * i), 1)
        for j in range(Constant.LINE_POINTS):
            pygame.draw.line(
                screen, Constant.BLACK_COLOR,
                (Constant.START_X + Constant.SIZE * j, Constant.START_X),
                (
                    Constant.START_X + Constant.SIZE * j, Constant.START_X
                    + Constant.SIZE * (Constant.LINE_POINTS - 1)), 1)
        # 画星位和天元
        if Constant.LINE_POINTS in (9, 11, 13):
            left = 2
            right = Constant.LINE_POINTS - 3
        else:
            left = 3
            right = Constant.LINE_POINTS - 4
        middle = int((Constant.LINE_POINTS - 1) / 2)
        stars = (left, middle, right)
        if Constant.LINE_POINTS < 9 \
                or Constant.LINE_POINTS > 19 \
                or Constant.LINE_POINTS % 2 == 0:
            stars = ()
        for i in stars:
            for j in stars:
                if i == j == middle:
                    radius = 5
                else:
                    radius = 3
                pygame.gfxdraw.aacircle(
                    screen, Constant.START_X + Constant.SIZE * i,
                    Constant.START_Y + Constant.SIZE * j,
                    radius, Constant.BLACK_COLOR)
                pygame.gfxdraw.filled_circle(
                    screen, Constant.START_X + Constant.SIZE * i,
                    Constant.START_Y + Constant.SIZE * j, radius,
                    Constant.BLACK_COLOR)
        # 画坐标
        for i in range(Constant.LINE_POINTS):
            self.print_text(
                screen, font, Constant.OUTER_WIDTH + i * Constant.SIZE, 0,
                chr(ord('A') + i), Constant.BLUE_COLOR)
        for i in range(Constant.LINE_POINTS):
            self.print_text(
                screen, font, 0, Constant.OUTER_WIDTH + i * Constant.SIZE,
                str(i + 1) if i >= 9 else ' ' + str(i + 1),
                Constant.BLUE_COLOR)

    def _draw_chessman(self, screen, point, stone_color):
        '''画棋子'''
        pygame.gfxdraw.aacircle(
            screen, Constant.START_X + Constant.SIZE * point.X,
            Constant.START_Y + Constant.SIZE * point.Y,
            Constant.STONE_RADIUS, stone_color)
        pygame.gfxdraw.filled_circle(
            screen, Constant.START_X + Constant.SIZE * point.X,
            Constant.START_Y + Constant.SIZE * point.Y,
            Constant.STONE_RADIUS, stone_color)

    def _draw_chessman_pos(self, screen, pos, stone_color):
        pygame.gfxdraw.aacircle(
            screen, pos[0], pos[1], Constant.STONE_INFO_RADIUS, stone_color)
        pygame.gfxdraw.filled_circle(
            screen, pos[0], pos[1], Constant.STONE_INFO_RADIUS, stone_color)

    def _draw_right_info(
            self, screen, font, cur_runner, black_win_count, white_win_count):
        '''画右侧信息显示'''
        self._draw_chessman_pos(screen, (
            Constant.SCREEN_HEIGHT + Constant.STONE_INFO_RADIUS,
            Constant.START_X + Constant.STONE_INFO_RADIUS),
            cur_runner.Color)
        self._draw_chessman_pos(screen, (
            Constant.SCREEN_HEIGHT + Constant.STONE_INFO_RADIUS,
            Constant.START_X + Constant.STONE_INFO_RADIUS * 4),
            self._get_next(cur_runner).Color)

        self.print_text(
            screen, font, Constant.RIGHT_INFO_POS_X,
            Constant.START_X + 3, '玩家', Constant.BLUE_COLOR)
        self.print_text(
            screen, font, Constant.RIGHT_INFO_POS_X,
            Constant.START_X + Constant.STONE_INFO_RADIUS * 3 + 3,
            '电脑', Constant.BLUE_COLOR)

        self.print_text(
            screen, font, Constant.SCREEN_HEIGHT,
            Constant.SCREEN_HEIGHT - Constant.STONE_INFO_RADIUS * 8,
            '战况：', Constant.BLUE_COLOR)
        self.print_text(
            screen, font, Constant.SCREEN_HEIGHT,
            Constant.SCREEN_HEIGHT - int(Constant.STONE_INFO_RADIUS * 5.5) + 3,
            f'玩家：{black_win_count} 胜', Constant.BLUE_COLOR)
        self.print_text(
            screen, font, Constant.SCREEN_HEIGHT,
            Constant.SCREEN_HEIGHT - Constant.STONE_INFO_RADIUS * 3 + 3,
            f'电脑：{white_win_count} 胜', Constant.BLUE_COLOR)

    def _get_clickpoint(self, click_pos):
        '''根据鼠标点击位置，返回游戏区坐标'''
        pos_x = click_pos[0] - Constant.START_X
        pos_y = click_pos[1] - Constant.START_Y
        if pos_x < -Constant.INSIDE_WIDTH or pos_y < -Constant.INSIDE_WIDTH:
            return None
        x = pos_x // Constant.SIZE
        y = pos_y // Constant.SIZE
        if pos_x % Constant.SIZE > Constant.STONE_RADIUS:
            x += 1
        if pos_y % Constant.SIZE > Constant.STONE_RADIUS:
            y += 1
        if x >= Constant.LINE_POINTS or y >= Constant.LINE_POINTS:
            return None
        return Constant.Point(x, y)

    def evaluate(self, turn, next_turn):
        val = 0
        ene_turn = (turn + 1) % 2
        over_count1 = 0
        for each in candidate_pos_list[turn]:
            count1 = -1
            for i in range(4):
                if pos_dic[each].blocked[turn][i] == 1:
                    break
                sum1 = (
                    pos_dic[each].from_count[turn][i]
                    + pos_dic[each].from_count[turn][(i+4) % 8])
                if sum1 >= 4:
                    if next_turn == turn:
                        return 10001
                    else:
                        over_count1 += 1
                        break
                if sum1 == 1:
                    val += 1
                else:
                    val += sum1 * sum1 / 2
                count1 += sum1
            if count1 >= 2:
                count1 += 1
            if count1 > -1:
                val += count1
        over_count2 = 0
        for each in candidate_pos_list[ene_turn]:
            count2 = 1
            for i in range(4):
                if pos_dic[each].blocked[ene_turn][i] == 1:
                    continue
                sum2 = pos_dic[each].from_count[ene_turn][i] \
                    + pos_dic[each].from_count[ene_turn][(i+4) % 8]
                if sum2 >= 4:
                    if next_turn == ene_turn:
                        return -10001
                    else:
                        over_count2 += 1
                        break
                if sum2 == 1:
                    val -= 1
                else:
                    val -= sum2 * sum2 / 2
                count2 -= sum2
            if count2 <= -2:
                count2 -= 1
            if count2 < 1:
                val += count2
        if next_turn == ene_turn:
            if over_count2 >= 2:
                return -10001
            if over_count1 >= 2:
                return 10001
        if next_turn == turn:
            if over_count1 >= 2:
                return 10001
            if over_count2 >= 2:
                return -10001
        t = next_turn
        for each in candidate_pos_list[t]:
            for i in range(4):
                if pos_dic[each].from_count[t][i] \
                        + pos_dic[each].from_count[t][(i+4) % 8] == 3:
                    dt_x = pos_dic[each].neighbor_pos[i][0] - each[0]
                    dt_y = pos_dic[each].neighbor_pos[i][1] - each[1]
                    labi = 0
                    for j in range(1, LINE_POINTS):
                        temp_pos = (each[0] + j * dt_x, each[1] + j * dt_y)
                        if temp_pos[0] < 0 \
                                or temp_pos[0] >= LINE_POINTS \
                                or temp_pos[1] < 0 \
                                or temp_pos[1] >= LINE_POINTS:
                            labi = 1
                            break
                        if pos_dic[temp_pos].occupied == t + 1:
                            continue
                        if pos_dic[temp_pos].occupied == 0:
                            break
                        labi = 1
                        break
                    if labi == 0:
                        for j in range(-1, -LINE_POINTS, -1):
                            temp_pos = (each[0] + j * dt_x, each[1] + j * dt_y)
                            if temp_pos[0] < 0 \
                                    or temp_pos[0] >= LINE_POINTS \
                                    or temp_pos[1] < 0 \
                                    or temp_pos[1] >= LINE_POINTS:
                                labi = 1
                                break
                            if pos_dic[temp_pos].occupied == t + 1:
                                continue
                            if pos_dic[temp_pos].occupied == 0:
                                break
                            labi = 1
                            break
                    if labi == 0:
                        if t == turn:
                            return 10001
                        if t == ene_turn:
                            return -10001
        return val

    def print_text(self, screen, font, x, y, text, fcolor=(255, 255, 255)):
        imgText = font.render(text, True, fcolor)
        screen.blit(imgText, (x, y))

    def run(self):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((
            Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT))
        pygame.display.set_caption('五子棋')

        # 设置字体
        FONT16 = pygame.font.SysFont('SimHei', 16)
        FONT32 = pygame.font.SysFont('SimHei', 32)
        FONT72 = pygame.font.SysFont('SimHei', 72)
        FWIDTH16, FHEIGHT16 = FONT16.size('黑方获胜')
        FWIDTH32, FHEIGHT32 = FONT32.size('黑方获胜')
        FWIDTH72, FHEIGHT72 = FONT72.size('黑方获胜')

        checkerboard = Checkerboard(Constant.LINE_POINTS)
        cur_runner = Constant.BLACK_CHESSMAN
        winner = None
        computer = Computer(Constant.LINE_POINTS, Constant.WHITE_CHESSMAN)

        black_win_count = 0
        white_win_count = 0

        clock = pygame.time.Clock()
        turn = 0
        win_lab = 0
        while True:
            clock.tick(Constant.FPS)
            event = pygame.event.poll()
            if event.type == QUIT:
                pygame.quit()
                break
            elif event.type == KEYDOWN:
                if event.key == K_b:
                    if winner is not None:
                        winner = None
                        cur_runner = Constant.BLACK_CHESSMAN
                        checkerboard = Checkerboard(Constant.LINE_POINTS)
                        computer = Computer(
                            Constant.LINE_POINTS, Constant.WHITE_CHESSMAN)
                if event.key == K_w:
                    if winner is not None:
                        winner = None
                        cur_runner = Constant.WHITE_CHESSMAN
                        checkerboard = Checkerboard(Constant.LINE_POINTS)
                        computer = Computer(
                            Constant.LINE_POINTS, Constant.BLACK_CHESSMAN)
                        cur_runner = self._get_next(cur_runner)
                        computer.get_opponent_drop(click_point)
                        ai_point = computer.drop()
                        winner = checkerboard.drop(
                            cur_runner, ai_point)
                        if winner is not None:
                            white_win_count += 1
                        cur_runner = self._get_next(cur_runner)
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = self._get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(
                                    cur_runner, click_point)
                                if self.pos_dic[(
                                        click_point.Y,
                                        click_point.X)].occupied == 0:
                                    self.chess_vec[turn].append((
                                        click_point.Y, click_point.X))
                                    # win_detect = self.pos_dic[(
                                    #     click_point.Y, click_point.X)].
                                    #     occupy(turn + 1)
                                if winner is None:
                                    cur_runner = self._get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    ai_point = computer.drop()
                                    # print(f"click_point--{click_point}")
                                    # print(f"computer.drop()--{ai_point}")
                                    # ai_point = computer.AI_choice(1, DEPTH)
                                    # print(f"AI_choice()--{ai_point}")
                                    winner = checkerboard.drop(
                                        cur_runner,
                                        Constant.Point(
                                            ai_point[0], ai_point[1]))
                                    if self.pos_dic[(ai_point)].occupied == 0:
                                        self.chess_vec[turn].append((ai_point))
                                        # win_detect = pos_dic[(ai_point)] \
                                        #     .occupy(turn + 1)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = self._get_next(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print('超出棋盘区域')

            # 画棋盘
            self._draw_checkerboard(screen, FONT16)

            # 画棋盘上已有的棋子
            for i, row in enumerate(checkerboard.checkerboard):
                for j, cell in enumerate(row):
                    if cell == Constant.BLACK_CHESSMAN.Value:
                        self._draw_chessman(
                            screen, Constant.Point(j, i),
                            Constant.BLACK_CHESSMAN.Color)
                    elif cell == Constant.WHITE_CHESSMAN.Value:
                        self._draw_chessman(
                            screen, Constant.Point(j, i),
                            Constant.WHITE_CHESSMAN.Color)

            self._draw_right_info(
                screen, FONT32, cur_runner, black_win_count, white_win_count)

            if winner:
                self.print_text(
                    screen, FONT72, (Constant.SCREEN_WIDTH - FWIDTH72) // 2,
                    (Constant.SCREEN_HEIGHT - FHEIGHT72) // 2,
                    winner.Name + '获胜', Constant.RED_COLOR)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
