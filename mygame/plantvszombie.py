import pygame
import sys
import random

#初始化pygame
pygame.init()

#全局设置
#游戏界面宽度
width = 800
#游戏界面高度
height = 640
#游戏窗口
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('孙悟空大闹桃园林')

GAMEOVER = False

#坐标点类
class Point():
    points = []
    points_row = []
    def __init__(self,h_line,w_line):
        for y in range(1,h_line):
            t_point = list()
            for x in range(w_line):
                point = (x,y)
                t_point.append(point)
            self.points.append(t_point)

#地图类
class Map():
    map_1 = 'imgs/map_1.png'
    map_2 = 'imgs/map_2.png'
    map = [map_1,map_2]
    def __init__(self,x,y,index):
        self.map_image = pygame.image.load(Map.map[index])
        self.position = (x,y)
        self.can_grow = True
    def load_map(self):
        screen.blit(self.map_image,self.position)

#植物类
class Plant():
    def __init__(self):
        self.cost = 50
#僵尸类
class Zombie(pygame.sprite.Sprite):
    #初始化僵尸
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.m = Main()
        #self.c = Collide()
        self.zombie_image = pygame.image.load('imgs/sunwukong.png')
        self.zombie_rect = self.zombie_image.get_rect()

        self.zombie_rect.x = x
        self.zombie_rect.y = y

        self.rect = self.zombie_rect
        self.rect.x = self.zombie_rect.x
        self.rect.y = self.zombie_rect.y

        self.speed = 1
        self.stop = False
        self.live = True

        self.attack = 2
        self.hp = 150
        self.value = 100
    #加载僵尸
    def load_zombie(self):
        screen.blit(self.zombie_image,(self.zombie_rect.x,self.zombie_rect.y))
    #移动僵尸
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed

            if self.rect.x <= -80:
                Main().gameOver()
    #碰到卷心菜
    def hit_cabbage(self):
        for cabbage in self.m.cabbage_list:
            crush_result = pygame.sprite.collide_rect(self,cabbage)
            if crush_result:
                self.stop = True
                self.eat_cabbage(cabbage)
                print('孙猴子被仙女迷住啦')

    #碰到豌豆射手
    def hit_peashooter(self):
        for peashooter in self.m.peashooter_list:
            crush_result = pygame.sprite.collide_rect(self,peashooter)
            if crush_result:
                self.stop = True
                self.eat_peashooter(peashooter)
                print('孙猴子开始吃桃子啦')

    #攻击卷心菜
    def eat_cabbage(self,cabbage):
        cabbage.hp -= self.attack
        if cabbage.hp <= 0:
            x = self.zombie_rect.y // 80 - 1
            y = self.zombie_rect.x // 80
            map = Main.map_list[x][y]
            cabbage.live = False
            #修改僵尸的移动状态
            self.stop = False
            #判断地图块是否可种植
            map.can_grow = True

    #攻击豌豆射手
    def eat_peashooter(self,peashooter):
        peashooter.hp -= self.attack
        if peashooter.hp <= 0:
            x = self.zombie_rect.y // 80 - 1
            y = self.zombie_rect.x // 80
            map = Main.map_list[x][y]
            peashooter.live = False
            #修改僵尸的移动状态
            self.stop = False
            #判断地图块是否可以种植
            map.can_grow = True


#卷心菜类
class Cabbage(pygame.sprite.Sprite,Plant):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.cabbage_image = pygame.image.load('imgs/xiannv.png')
        self.rect = self.cabbage_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = (x,y)
        self.hp = 150
        self.live = True
        #时间计数器
        self.time_count = 0
    def load_cabbage(self):
        screen.blit(self.cabbage_image,self.position)

    #生成金币
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 30:
            Main.money += 5
            self.time_count = 0
            print('+5')

#豌豆射手类
class Peashooter(pygame.sprite.Sprite,Plant):
    def __init__(self,x,y):
        self.peashooter_image = pygame.image.load('imgs/taoshu.png')
        self.rect = self.peashooter_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = (x,y)
        self.live = True
        self.hp = 150
        #计数器
        self.count = 0

    def load_peashooter(self):
        screen.blit(self.peashooter_image,self.position)
    #豌豆射击
    def shot(self):
        #判断是否射击
        should_fire = False
        for zombie in Main.zombie_list:
            if zombie.zombie_rect.y == self.position[1] and zombie.zombie_rect.x > self.position[0] and zombie.zombie_rect.x < 800:
                should_fire = True
        if should_fire:
            self.count += 1
            #计数到20时发射一次
            if self.count == 20:
                bullet = Bullet(self.position[0],self.position[1])
                Main.bullet_list.append(bullet)
                self.count = 0

#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.m = Main()
        pygame.sprite.Sprite.__init__(self)
        self.bullet_image = pygame.image.load('imgs/peach.png')
        self.rect = self.bullet_image.get_rect()
        self.rect.x = x + 55
        self.rect.y = y + 20
        self.speed = 10
        self.live = True
        self.stop = False
        self.attack = 10
    def move_bullet(self):
        if self.rect.x < width:
            self.rect.x += self.speed
        else:
            self.live = False

    def load_bullet(self):
        screen.blit(self.bullet_image,(self.rect.x,self.rect.y))

    #判断子弹是否打到小僵尸
    def hit_zombie(self):
        for zombie in self.m.zombie_list:
            crush_result = pygame.sprite.collide_rect(self,zombie)
            if crush_result:
                self.stop = True
                self.kill_zombie(zombie)
                print('桃子击中孙猴子啦')
    #子弹攻击小僵尸
    def kill_zombie(self,zombie):
        zombie.hp -= self.attack
        if zombie.hp <= 0:
            zombie.live = False
            Main.money += 100
            print(Main.money)

#文字说明
class Text():
    def __init__(self):
        pygame.font.init()
        self.text1 = '1 点击鼠标左键生成仙女 2 点击鼠标右键生成桃树'
        self.f = pygame.font.Font('C:/Windows/Fonts/simfang.ttf',25)

    def Draw_text(self):
        text_1 = self.f.render(self.text1,False,(255,0,0),(255,255,255))
        text_2 = self.f.render('当前仙气值{}'.format(Main.money),False,(255,0,0),(255,255,255))
        screen.blit(text_1,(10,20))
        screen.blit(text_2,(600,20))
#游戏主程序
class Main():
    p = Point(8,10)
    t = Text()
    points_list = []
    map_list = []
    zombie_list = []
    cabbage_list = []
    peashooter_list = []
    bullet_list = []
    money = 300
    #计数器，达到一定循环次数就重新初始化小僵尸
    count = 0

    #初始化坐标点
    def init_points(self):
        self.points_list = self.p.points
    #初始化地图
    def init_map(self):
        for p_r in self.points_list:
            t_map = list()
            for p in p_r:
                if((p[0] + p[1]) % 2 == 0):
                    map = Map(p[0] * 80,p[1] * 80, 0)
                else:
                    map = Map(p[0] * 80,p[1] * 80, 1)
                t_map.append(map)
            self.map_list.append(t_map)
    #加载地图
    def load_map(self):
        for t_m in self.map_list:
            for m in t_m:
                m.load_map()
    #初始化小僵尸
    def init_zombie(self):
        for i in range(1,8):
            dis = random.randint(1,7)
            zombie = Zombie(800 + dis * 200,i * 80)
            self.zombie_list.append(zombie)
    #加载小僵尸
    def load_zombie(self):
        for zombie in self.zombie_list:
            if zombie.live:
                zombie.load_zombie()
                zombie.move_zombie()
                zombie.hit_cabbage()
                zombie.hit_peashooter()
            else:
                self.zombie_list.remove(zombie)

    #鼠标左键点击加载卷心菜
    def load_cabbage(self):
        for cabbage in self.cabbage_list:
            if cabbage.live:
                cabbage.load_cabbage()
                cabbage.produce_money()
            else:
                self.cabbage_list.remove(cabbage)
    #鼠标右键点击加载豌豆射手
    def load_peashooter(self):
        for peashooter in self.peashooter_list:
            if peashooter.live:
                peashooter.load_peashooter()
                peashooter.shot()
            else:
                self.peashooter_list.remove(peashooter)
    #加载子弹
    def load_bullet(self):
        for b in self.bullet_list:
            if b.live and not b.stop:
                b.load_bullet()
                b.move_bullet()
                b.hit_zombie()
    #加载文字说明
    def load_text(self):
        self.t.Draw_text()

    #事件监听
    def events(self):
        #while True:
        for event in pygame.event.get():
            #判断用户是否点了“X”关闭程序
            if event.type == pygame.QUIT:
                #卸载所有模块
                pygame.quit()
                #终止程序，确保退出程序
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // 80
                y = event.pos[1] // 80
                map = Main.map_list[y - 1][x]
                 #判断用户是否点击了鼠标左键加载卷心菜
                if event.button == 1:
                    print(x,y)
                    if Main.money >= Plant().cost and map.can_grow:
                        cabbage = Cabbage(x * 80,y * 80)
                        self.cabbage_list.append(cabbage)
                        Main.money -= Plant().cost
                        map.can_grow = False
                    else:
                        print('仙气不够，仙女不来')
                #判断用户是否点击了鼠标右键
                elif event.button == 3:
                    if Main.money >= Plant().cost and map.can_grow:
                        peashooter = Peashooter(x * 80,y * 80)
                        self.peashooter_list.append(peashooter)
                        Main.money -= Plant().cost
                        map.can_grow = False
                    else:
                        print('仙气不够，无法种树')

    #开始游戏
    def start_game(self):
        self.init_points()
        self.init_map()
        self.init_zombie()
        while not GAMEOVER:
            screen.fill((255,255,255))
            self.load_map()
            self.load_zombie()
            self.load_cabbage()
            self.load_peashooter()
            self.load_bullet()
            self.load_text()
            self.count += 1
            if self.count == 100:
                self.init_zombie()
                self.count = 0
            self.events()
            #pygame休眠
            pygame.time.wait(10)
            pygame.display.update()
    #游戏结束
    def gameOver(self):
        print('gameover')
        global GAMEOVER
        GAMEOVER = True
#启动程序
if __name__ == '__main__':
    game = Main()
    game.start_game()

