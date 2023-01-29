import pandas as pd
from collections import deque
from PIL import Image
import numpy as np


class q_learning_model_maze:
    def __init__(self, actions, q_table=None, learning_rate=0.7, reward_decay=0.9, e_greedy=0.8):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.e_greedy = e_greedy
        if q_table is None:
            self.q_table = pd.DataFrame(columns=actions, dtype=np.float32)
            self.q_table_True = 0
        else:
            self.q_table = q_table
            self.q_table_True = 1
    # 检查状态是否存在
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    # 选择动作
    def choose_action(self, s):
        self.check_state_exist(s)
        if np.random.uniform() < self.e_greedy:

            state_action = self.q_table.loc[s, :]
            # state_action = state_action.reindex(
            #     np.random.permutation(state_action.index))  # 防止相同列值时取第一个列，所以打乱列的顺序
            action = np.random.choice(state_action[state_action == state_action.max()].index)
        else:
            action = np.random.choice(self.actions)
        return action

    # 更新q表
    def rl(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]  # q估计
        if s_ != 'terminal':
            q_target = r + self.reward_decay * self.q_table.loc[s_, :].max()  # q现实
        else:
            q_target = r

        self.q_table.loc[s, a] += self.learning_rate * (q_target - q_predict)

        # if r == -100:
        #     self.q_table.loc[s, a] += -100


        # for _ in range(100):
        #     rand_idx = np.random.choice(range(len(self.q_table)))
        #     _state = self.q_table.iloc[rand_idx]
        #     rand_action = np.random.choice(4)


img_PIL = Image.open('maze.jpg')#读取数据
img_PIL = np.array(img_PIL)
maze = img_PIL[48:440,50:570,0]
a = np.zeros((49,65))
for i in range(49):
    for j in range(65):
        a[i,j] = maze[i*8:(i+1)*8,j*8:(j+1)*8].sum()
aa = np.where(a>3000,1,0)
# aa = aa[24:,32:]
aa[-5,-2]=0
aa[48,63]=1
d = np.where(aa>10)
maze = aa

#四个方向
dirs = [
    lambda x,y :(x+1,y),
    lambda x,y :(x-1,y),
    lambda x,y :(x,y-1),
    lambda x,y :(x,y+1)
]

def  maze_path_queue(x1,y1,x2,y2):
    path_labe = []
    queue = deque()
    queue.append((x1,y1,-1))

    while len(queue)>0:
        curnode = queue.popleft()
        # print(curnode)
        path_labe.append(curnode)

        if curnode[0] == x2 and curnode[1] == y2:
            cur = path_labe[-1]

            path_result = []
            while cur[2] != -1:#只有起点的第三个元素才是-1
                path_result.append((cur[0],cur[1]))
                cur = path_labe[cur[2]]
            path_result.reverse()
            print(len(path_result))
            # for path in path_result:
            #     print(path)
            return path_result

        for dir in dirs:
            nextnode = dir(curnode[0],curnode[1])
            if maze[nextnode[0]][nextnode[1]] == 0:

                queue.append((nextnode[0],nextnode[1],path_labe.index(curnode)))
                maze[nextnode[0]][nextnode[1]] = 2

    else:
        print("End is wall. NO way!")
