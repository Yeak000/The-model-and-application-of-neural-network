# coding: utf-8
from PIL import Image
import sys
import time
import numpy as np

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

img_PIL = Image.open('maze.jpg')#读取数据
img_PIL = np.array(img_PIL)
maze = img_PIL[48:440,50:570,0]
a = np.zeros((49,65))
for i in range(49):
    for j in range(65):
        a[i,j] = maze[i*8:(i+1)*8,j*8:(j+1)*8].sum()
aa = np.where(a>3000,255,0)
# aa = aa[24:,32:]
aa[-5,-2]=0
d = np.where(aa>10)

class Maze(tk.Tk, object):
    UNIT = 16  # pixels
    MAZE_H = 49  # grid height
    MAZE_W = 65  # grid width

    def __init__(self, end=(38, 26), path=None):
        super(Maze, self).__init__()
        self.end = end
        self.action_space = ['U', 'D', 'R', 'L']
        self.n_actions = len(self.action_space)
        self.title('迷宫')
        self.geometry('{0}x{1}'.format(self.MAZE_H * self.UNIT, self.MAZE_H * self.UNIT))  # 窗口大小
        self.min_len_s = 9999
        self.min_s = []
        self._build_maze()
        self.res = path


    # 画矩形
    # x y 格坐标
    # color 颜色
    def _draw_rect(self, x, y, color):
        center = self.UNIT / 2
        w = center - 2
        x_ = self.UNIT * x + center
        y_ = self.UNIT * y + center
        return self.canvas.create_rectangle(x_ - w, y_ - w, x_ + w, y_ + w, fill=color)

    # 初始化迷宫
    def _build_maze(self):
        h = self.MAZE_H * self.UNIT
        w = self.MAZE_W * self.UNIT
        # 初始化画布
        self.canvas = tk.Canvas(self, bg='black', height=h, width=w)
        # 画线
        for c in range(0, w, self.UNIT):
            self.canvas.create_line(c, 0, c, h)
        for r in range(0, h, self.UNIT):
            self.canvas.create_line(0, r, w, r)

        # 陷阱
        # self.hells = [self._draw_rect(3, 2, 'black'),
        #               self._draw_rect(3, 3, 'black'),
        #               self._draw_rect(3, 4, 'black'),
        #               self._draw_rect(3, 5, 'black'),
        #               self._draw_rect(4, 1, 'black'),
        #               self._draw_rect(4, 5, 'black'),
        #               self._draw_rect(1, 0, 'black'),
        #               self._draw_rect(1, 1, 'black'),
        #               self._draw_rect(1, 2, 'black'),
        #               self._draw_rect(1, 3, 'black'),
        #               self._draw_rect(1, 4, 'black')]
        self.hells = [self._draw_rect(d[1][i],d[0][i],'white') for i in range(len(d[0]))]
        self.hell_coords = []
        for hell in self.hells:
            self.hell_coords.append(self.canvas.coords(hell))

        # 奖励
        self.oval = self._draw_rect(self.end[0], self.end[1], 'yellow')
        # 玩家对象
        self.rect = self._draw_rect(63, 44, 'red')

        self.canvas.pack()  # 执行画

    # 重新初始化
    def reset(self):
        self.update()
        # time.sleep(0.01)
        self.canvas.delete(self.rect)
        self.rect = self._draw_rect(63, 44, 'red')
        self.old_s = []
        # 返回 玩家矩形的坐标
        return self.canvas.coords(self.rect)

    # 走下一步
    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if s[1] > self.UNIT:
                base_action[1] -= self.UNIT
        elif action == 1:  # down
            if s[1] < (self.MAZE_H - 1) * self.UNIT:
                base_action[1] += self.UNIT
        elif action == 2:  # right
            if s[0] < (self.MAZE_W - 1) * self.UNIT:
                base_action[0] += self.UNIT
        elif action == 3:  # left
            if s[0] > self.UNIT:
                base_action[0] -= self.UNIT

        # 根据策略移动红块
        o_s = s.copy()
        self.canvas.move(self.rect, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.rect)

        # 判断是否得到奖励或惩罚
        done = False
        if s_ == self.canvas.coords(self.oval):
            reward = 10000
            done = True
            if len(self.old_s) <= self.min_len_s:
                self.min_len_s = len(self.old_s)
                self.min_s = self.old_s
        elif s_ in self.hell_coords:
            reward = -100
            done = True
            # s_ = o_s
        # elif base_action.sum() == 0:
        #     reward = -1
        else:
            reward = -1

        self.old_s.append(o_s)
        return s_, reward, done

    def render(self):
        # time.sleep(0.001)
        self.update()

    def draw_path(self):
        road = []
        for i in self.old_s:
            road.append([int(((i[0] + i[2]) / 2 - 8) / 16), int(((i[1] + i[3]) / 2 - 8) / 16)])
            self._draw_rect(road[-1][0], road[-1][1], 'green')

    def draw_res(self):
        road = self.res
        for i in road:
            self._draw_rect(i[1], i[0], 'green')

