import numpy as np
import time
import Player
import random



'''
每局游戏，先生成GeneralsGame， 然后调用generate_players, 输入id列表， 之后generate_map， 生成地图， 再generate_players_position, 生成玩家位置，就可以反复执行step了

'''



class GeneralsGame:
    def __init__(self,  
                 map_size = 10, 
                 mountain_density = 0.1, 
                 city_density = 0.05,
                 city_fairness = 5):
        self.players = [] # 所有玩家的Player类型在里面了
        self.size = map_size # 地图大小
        self.mountain_density = mountain_density # 山脉密度
        self.city_density = city_density # 城市密度
        self.city_fairness = city_fairness # 城市大小公平
        self.map = None # 记录山脉城市地形等，3层嵌套列表
        self.player_position = [] # 储存玩家generals位置
        
    def generate_players(self, players_id : list):
        '''
        生成玩家信息
        '''
        for id in players_id:
            self.players.append(Player(id)) # 创建玩家

    def generate_map(self):
        '''
        每个位置有三个变量组成，第一个表示所属阵营id（公立为0）， 第二个表示占领此格子需要的兵力, 第三个表示地块类型，有mountain、tile、 city、 general
        '''
        if not self.map: # 确保地图没有生成过
            map_origin = [[[[0, 0, 'tile']] * self.size] for _ in range(self.size)] # 生成基础地图
            for i in range(self.size):
                for j in range(self.size):
                    if random.random() < self.mountain_density: # 按照概率生成山脉
                        map_origin[i][j] = [0, 0, 'mountain']  
                        continue # 不再生成city
                    if random.random() < self.city_density: # 按照概率和公平生成城市和具体兵力
                        map_origin[i][j] = [0, int(random.uniform(45 - self.city_fairness, 45 + self.city_fairness)), 'city']  
            self.map = map_origin # 记录生成的随机地图

    def generate_players_position(self):
        '''
        生成玩家的王城地点，更新地图数据
        '''
        if (not self.player_position) and self.map: # 确保地图已生成，且玩家位置没有生成过
            for player in self.players:
                invalid = True
                while invalid:
                    i, j = random.randrange(self.size), random.randrange(self.size)
                    if self.map[i][j][2] == 'tile' :
                        # 出生地在空地并且与其他王没有重叠
                        invalid = False
                self.map[i][j] = [player.id, 0, 'general'] # 更新系统地图数据
                self.player_position.append([i, j])
                player.pass_general_position([i, j])

    def pass_player_sight(self):
        '''
        根据玩家占领的地块，给予玩家视野
        '''
        biases = [[1, 1], [1, 0], [1, -1], [0, 1], [0, 0], [0, -1], [-1, 1], [-1, 0], [-1, -1]] # 相邻具有的偏差
        for player in self.players: # 对所有玩家分享视野
            player.sight = []
            for i in range(self.size):
                for j in range(self.size): # 遍历所有地块
                    visible = False # 初始不可见
                    for bias in biases:
                        if [i + bias[0], j + bias[1]] in player.territory: # 与领土相邻则认为可见
                            visible = True
                    if visible: # 可视，就把信息如实告诉你, 并且记录视野信息，方便后期渲染
                        player.map[i][j] = self.map[i][j]
                        player.sight.append([i, j])
                    else: # 不可视要讨论
                        if (self.map[i][j][2] == 'mountain') or (self.map[i][j][2] == 'city'): # 山或者塔，统一渲染成塔
                            player.map[i][j] = [0, 0, 'mountain']  # 山
                        else:
                            player.map[i][j] = [0, 0, 'tile'] # 其余全部渲染成空地（对别人的王也是）

    def is_valid(player: Player,
                option: list): 
        '''
        判断移动是否有意义,传递移动的数据：即一个坐标+移动+移动是否半兵：例如option = [3, 4, 'up', False]
        '''
        direction_dict = {'up': [-1, 0], 'down': [1, 0], 'left': [0, -1], 'right': [0, 1]}
        cx, cy = option[0], option[1] # current
        nx, ny = cx + direction_dict[option[2]][0], cy + direction_dict[option[2]][1] # next
        if player.map[cx][cy][0] != player.id: # 不是自己的领地，你移动个屁
            return False
        if player.map[cx][cy][1] <= 1: # 连两个兵都没有，你移动个屁
            return False
        if  (nx < 0) or\
            (nx > player.map_size) or\
            (ny < 0) or\
            (ny > player.map_size) :
            return False # 都越界了，你移动个屁
        if player.map[nx][ny][2] == 'mountain':
            return False # 都移动到山上了，你移动个屁
        return True
    
    def move(self, player, option):
        self

        pass

    def step(self):
        for player in self.players:
            t = 0 # 指针
            while player.action_queue: # 执行队列非空
                option = player.action_queue.pop(0) # 取出最前端元素
                if self.is_valid(player, option): # 判断合法性
                    self.move(player, option) # 合法则执行
                    break 
            
            
            
        

    
    def main(self):
        pass
        

            

    

class GeneralsGame1:
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    MOUNTAIN = -1
    
    def __init__(self, size=15, players=2):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.armies = np.zeros((size, size), dtype=int)
        self.turn = 0
        self._init_board(players)
        self.move_count = {p+1: 0 for p in range(players)}
        self.last_turn_time = time.time()
        self.turn_interval = 0.7  # 秒
    
    def _init_board(self, players):
        """初始化游戏板"""
        # 设置玩家起始位置
        self.board[2][2] = self.PLAYER1
        self.board[self.size-3][self.size-3] = self.PLAYER2
        self.armies[2][2] = 0 # 这里是初始兵力1
        self.armies[self.size-3][self.size-3] = 0 # 这里是初始兵力2
        
        # 添加山脉
        for _ in range(self.size):
            x, y = np.random.randint(0, self.size, 2)
            self.board[x][y] = self.MOUNTAIN

    def move(self, player, from_pos, to_pos):
        """执行移动操作"""
        x1, y1 = from_pos
        x2, y2 = to_pos
    
        # 步数限制
        if not self.can_move(player):
            return False
        # 兵力为1不能移动
        if self.armies[x1][y1] <= 1:
            return False
        # 合法性检查
        if not self._is_valid_move(player, from_pos, to_pos):
            return False
    
        # 执行移动
        moving_army = self.armies[x1][y1] - 1
        self.armies[x1][y1] = 1
    
        # 处理目标格
        if self.board[x2][y2] == self.EMPTY:
            self.board[x2][y2] = player
            self.armies[x2][y2] = moving_army
        elif self.board[x2][y2] == player:
            # 己方地块，兵力相加（如果目标格兵力为0，直接赋值）
            if self.armies[x2][y2] > 0:
                self.armies[x2][y2] += moving_army
            else:
                self.armies[x2][y2] = moving_army
        else:  # 敌方地块
            self.armies[x2][y2] -= moving_army
            if self.armies[x2][y2] < 0:
                self.board[x2][y2] = player
                self.armies[x2][y2] = abs(self.armies[x2][y2])
    
        self.move_count[player] += 1
        return True

    
    def _is_valid_move(self, player, from_pos, to_pos):
        """验证移动是否合法"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        # 检查是否属于玩家
        if self.board[x1][y1] != player:
            return False
        
        # 检查移动距离
        if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
            return False
        
        # 检查目标不是山脉
        if self.board[x2][y2] == self.MOUNTAIN:
            return False
            
        return True
    
    def get_state(self):
        """获取游戏状态（简化版）"""
        return {
            "board": self.board.tolist(),
            "armies": self.armies.tolist(),
            "turn": self.turn,
            "move_count": self.move_count.copy()
        }
    
    def can_move(self, player):
        return self.move_count[player] < 2

    def next_turn(self):
        # 每回合主城+1
        self.armies[2][2] += 1
        self.armies[self.size-3][self.size-3] += 1
        self.turn += 1
        self.move_count = {p: 0 for p in self.move_count}
        # 每25回合所有己方地块+1
        if self.turn % 25 == 0:
            for x in range(self.size):
                for y in range(self.size):
                    if self.board[x][y] == self.PLAYER1 or self.board[x][y] == self.PLAYER2:
                        self.armies[x][y] += 1