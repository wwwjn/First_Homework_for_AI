import numpy as np
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QLabel
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from start import Ui_MainWindow
from Play import Ui_Form
import random
import math
from queue import PriorityQueue as PQ
import resource
import time

class Firstwindow(QMainWindow,Ui_MainWindow):  # 主界面实例化
    def  __init__ (self,parent=None):
        super(Firstwindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.startEvent)
    def startEvent(self):
        self.setWindowTitle("Find Carrot!")
        self.setWindowIcon(QIcon(":/Carrot.jpg"))
        self.hide()
        self.dia=Secondwindow()
        self.dia.show()

class Secondwindow(QtWidgets.QWidget,Ui_Form):
    def __init__ (self):
        super(Secondwindow,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.AStarAlgorithm)
        self.restartButton.clicked.connect(self.restart)
        self.show()

    def AStarAlgorithm(self):
        Mapindex =self.MapSize.currentIndex() # 获取下拉框的输入
        if(Mapindex==0):
            self.label_4.setPixmap(QtGui.QPixmap(":/MapBackground8.jpg"))
            mapsize=8
        if (Mapindex==1):
            self.label_4.setPixmap(QtGui.QPixmap(":/MapBackground12.jpg"))
            mapsize = 12
        if (Mapindex==2):
            mapsize = 16
            self.label_4.setPixmap(QtGui.QPixmap(":/MapBackground16.jpg"))
        BarriorIndex=self.BarrierRatio.currentIndex()
        if(BarriorIndex==0):
            barrior=0.1
        if (BarriorIndex == 1):
            barrior = 0.15
        if (BarriorIndex == 2):
            barrior = 0.2
        if (BarriorIndex == 3):
            barrior = 0.25
        if (BarriorIndex == 4):
            barrior = 0.3
        #WallNumber=int(mapsize*mapsize*barrior) # 障碍的个数
        Map=np.zeros([mapsize,mapsize]) # 储存地图的矩阵，0代表没有树桩，1代表有树桩
        self.Labellist = []
        for i in range(0,mapsize):#生成雷区的色块
            for j in range(0,mapsize):
                a = random.random()  #产生在0到1之间的随机数
                if (a < barrior):
                    Map[i,j]=1 # 等于1表示有障碍
                    # 创建一个带有树桩图片的Label
                    self.Labellist.append(QtWidgets.QLabel(self))
                    self.Labellist[-1].setObjectName("label_"+str(i)+str(j))
                    self.Labellist[-1].setGeometry(480/mapsize*i+80 ,480/mapsize*j+60, 480/mapsize, 480/mapsize)
                    if (Mapindex == 0):
                        self.Labellist[-1].setPixmap(QPixmap(":/Wall8.jpg"))
                    if (Mapindex == 1):
                        self.Labellist[-1].setPixmap(QPixmap(":/Wall12.jpg"))
                    if (Mapindex == 2):
                        self.Labellist[-1].setPixmap(QPixmap(":/Wall16.jpg"))
                    #self.Labellist[-1].raise_()
                    self.Labellist[-1].show()
                else:
                    Map[i, j] = 0
                #产生小怪兽和胡萝卜的位置
        while(True):
            xStart=random.randrange(0,mapsize) # 小怪兽的位置
            yStart=random.randrange(0,mapsize)
            xDestin=random.randrange(0,mapsize)
            yDestion=random.randrange(0,mapsize)
            if ((math.fabs(xStart-xDestin)+math.fabs(yStart-yDestion))>mapsize
                    and Map[xStart,yStart]==0 and Map[xDestin,yDestion]==0):
                # 曼哈顿距离不能太近，且不能已经有树桩
                self.Monster=QtWidgets.QLabel(self)
                self.Monster.setObjectName("Monster")
                self.Monster.setGeometry(480/mapsize*xStart+80 ,480/mapsize*yStart+60, 480/mapsize,480/mapsize)
                self.Carrot = QtWidgets.QLabel(self)
                self.Carrot.setObjectName("Monster")
                self.Carrot.setGeometry(480 / mapsize * xDestin + 80, 480 / mapsize * yDestion + 60, 480 / mapsize,
                                         480 / mapsize)
                if (Mapindex == 0):
                    self.Monster.setPixmap(QPixmap(":/Monster8.jpg"))
                    self.Carrot.setPixmap(QPixmap(":/Carrot8.jpg"))
                if (Mapindex == 1):
                    self.Monster.setPixmap(QPixmap(":/Monster12.jpg"))
                    self.Carrot.setPixmap(QPixmap(":/Carrot12.jpg"))
                if (Mapindex == 2):
                    self.Monster.setPixmap(QPixmap(":/Monster16.jpg"))
                    self.Carrot.setPixmap(QPixmap(":/Carrot16.jpg"))
                self.Monster.show()
                self.Carrot.show()
                break
#---------------------我爱 A*算法 --------------------------------------------

        OpenList=PQ()
        isVisited = np.zeros([mapsize, mapsize])  # 建立是否被访问过的矩阵，0表示未被访问过
        Parent=np.zeros([mapsize,mapsize,2])
        self.Waylist = []
        #parent矩阵中每个元素都是一个二维数组，记录对应位置上的父母位置，所以其大小为mapsize*mapsize*2
        f=np.zeros([mapsize,mapsize]) #用于记录代价的f
        StepCount=0  #用于记录当前的路径代价
        # 应该维护一个优先级队列
        # 先算出各点距离终点的曼哈顿距离
        Manhanttan=np.zeros([mapsize,mapsize])
        for i in range(0,mapsize):
            for j in range(0,mapsize):
                Manhanttan[i,j]=math.fabs(i-xDestin)+math.fabs(j-yDestion)
                Parent[i,j,0]=-1
                Parent[i,j,1]=-1

        xCurrent=xStart  #记录当前位置的x，y值
        yCurrent=yStart
        while(True):
            isVisited[xCurrent,yCurrent]=1  #当前结点已经被访问过
            # 检查上下左右四种可能性，如果能走的话就加入到Open表里
            StepCount=StepCount+1
            if(xCurrent!=mapsize-1):  # 要想向右走，则不能在最右侧的
                if(Map[xCurrent+1,yCurrent]==0 and isVisited[xCurrent+1,yCurrent]==0):  # 向右走一步
                    #xCurrent=xCurrent+1  现在不能更新xCurrent，四周都探测过之后统一更新
                    f[xCurrent+1,yCurrent]=Manhanttan[xCurrent+1,yCurrent]+StepCount
                    b=f[xCurrent+1,yCurrent]  # 如果有f函数相等的怎么办？
                    isVisited[xCurrent+1, yCurrent] = 1
                    Parent[xCurrent+1,yCurrent,0]=xCurrent
                    Parent[xCurrent+1,yCurrent,1]=yCurrent # 更新parent位置
                    OpenList.put((b,StepCount,1,[xCurrent+1,yCurrent]))  #加入Open表/优先级队列    xCurrent改变之后，优先级队列中的东西是否会变化:不会
            if(xCurrent!=0): # 如果想向左走，那么Current位置不能在最左侧
                if(Map[xCurrent-1,yCurrent]==0 and isVisited[xCurrent-1,yCurrent]==0):  # 向左走一步
                    #xCurrent=xCurrent-1
                    f[xCurrent-1,yCurrent]=Manhanttan[xCurrent-1,yCurrent]+StepCount
                    b2 = f[xCurrent-1,yCurrent]  # 用b2将f[xcurrent,ycurrent]复制出来
                    isVisited[xCurrent-1, yCurrent] = 1
                    Parent[xCurrent - 1, yCurrent, 0] = xCurrent
                    Parent[xCurrent - 1, yCurrent, 1] = yCurrent# 更新parent位置
                    OpenList.put((b2,StepCount,2,[xCurrent-1,yCurrent]))
                    #加入Open表/优先级队列, stepCount和后面的数字为辅助，如果总代价f相等，Openlist会比较第二个数，此时先扩展StepCount大的
            if (yCurrent!= 0):  # 如果想向上走，那么Current位置不能在最上侧边界
                if (Map[xCurrent, yCurrent-1] == 0 and isVisited[xCurrent, yCurrent-1] == 0):  # 向上走一步
                    #yCurrent = yCurrent - 1
                    f[xCurrent, yCurrent-1] = Manhanttan[xCurrent, yCurrent-1] + StepCount
                    b3 = f[xCurrent, yCurrent-1]
                    isVisited[xCurrent, yCurrent-1] = 1
                    Parent[xCurrent, yCurrent-1, 0] = xCurrent
                    Parent[xCurrent, yCurrent-1, 1] = yCurrent  # 更新parent位置
                    OpenList.put((b3,StepCount,3, [xCurrent, yCurrent-1]))  # 加入Open表/优先级队列
            if (yCurrent != mapsize-1):  # 如果想向下走，那么Current位置不能在最下侧边界
                if (Map[xCurrent, yCurrent+1] == 0 and isVisited[xCurrent, yCurrent+1] == 0):  # 向下走一步
                    #yCurrent = yCurrent + 1
                    f[xCurrent, yCurrent+1] = Manhanttan[xCurrent, yCurrent+1] + StepCount
                    b4 = f[xCurrent, yCurrent+1]
                    isVisited[xCurrent, yCurrent+1] = 1
                    Parent[xCurrent , yCurrent+1, 0] = xCurrent
                    Parent[xCurrent , yCurrent+1, 1] = yCurrent  # 更新parent位置
                    OpenList.put((b4,StepCount,4,[xCurrent, yCurrent+1]))  # 加入Open表/优先级队列
            if(not OpenList.empty()):
                C=OpenList.get()
                xCurrent=C[3][0]
                yCurrent=C[3][1]
                if(xCurrent==xDestin and yCurrent==yDestion):# 到达终点
                    break
            elif(OpenList.empty()): #open表为空，表示没有找到最短路,对xCurrent和yCurrent做标记
                xCurrent=-2
                yCurrent=-2
                break

        if(xCurrent!=-2 and yCurrent!=-2):
            xCurrent = xDestin  # 记录当前位置的x，y值
            yCurrent = yDestion
            #生成路线上的每个点
            while(True):
                x=Parent[xCurrent,yCurrent,0]
                y=Parent[xCurrent,yCurrent,1]
                xCurrent=int(x)
                yCurrent=int(y)
                if(xCurrent!=xStart or yCurrent!=yStart):

                    # 创建一个带有道路图片的Label
                    self.Waylist.append(QtWidgets.QLabel(self))
                    self.Waylist[-1].setGeometry(480 / mapsize * xCurrent + 80, 480 / mapsize * yCurrent + 60, 480 / mapsize,480 / mapsize)
                    if (Mapindex == 0):
                        self.Waylist[-1].setPixmap(QPixmap(":/Way8.jpg"))
                    if (Mapindex == 1):
                        self.Waylist[-1].setPixmap(QPixmap(":/Way12.jpg"))
                    if (Mapindex == 2):
                        self.Waylist[-1].setPixmap(QPixmap(":/Way16.jpg"))
                    self.Waylist[-1].show()
                if (xCurrent == xStart and yCurrent == yStart):
                    break
                # 产生一个提示框，提示“最优路径已显示”
            QMessageBox.information(self,"Reminder","The shortest way is shown in the map.",QMessageBox.Ok)

        else:
            # 产生一个提示框，提示“没有找到最短路径”
            QMessageBox.information(self, "Reminder", "Can't find carrot! Please restart game.", QMessageBox.Ok)

        # 把find carrot按钮关闭 然后显示Restart按钮
        self.pushButton.hide()

    def restart(self):
        for count in range(0,len(self.Labellist)):
            self.Labellist[count].close()
        for count1 in range(0, len(self.Waylist)):
            self.Waylist[count1].close()

        self.Monster.close()
        self.Carrot.close()
        self.pushButton.show()

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    ui = Firstwindow()
    ui.show()
    sys.exit(app.exec_())
